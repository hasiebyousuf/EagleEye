# Sprint 1 Design — Foundation + IdeaEngine

_EagleEye · Designed 2026-05-16_

---

## Scope

Sprint 1 delivers a working end-to-end flow: a user signs up, creates their workspace, sets their budget, runs IdeaEngine, and receives a full interactive report. Nothing else.

**MVP success criteria:** User inputs an idea (or just a budget) → receives a full IdeaEngine report with report card, brand brief, idea variations, and pitch summary.

---

## Architecture

Two services, one monorepo, one Docker Compose file.

```
User (Browser)
      │
Next.js Frontend        ← UI, auth pages, wizard, report dashboard
      │ REST
FastAPI Backend         ← orchestration, AI, external APIs
      │
      ├── Supabase      ← Postgres, Auth, Storage
      └── Kimi 2.6      ← Moonshot AI API (AI model)
           │
           ├── Google Trends API   ← market interest data
           └── SerpAPI             ← search & shopping signals
```

**Key decisions:**
- FastAPI and Next.js run as two Docker containers via `docker-compose.yml`
- Supabase is the single source of truth for auth, data, and storage
- Kimi 2.6 is called server-side only — API key never touches the browser
- All external API calls (Google Trends, SerpAPI) are proxied through FastAPI
- `data_snapshots` table stores every raw API response — every AI claim is auditable

---

## Database Schema

```sql
workspaces
  id            uuid  PK
  owner_id      uuid  FK → auth.users
  name          text
  budget        numeric        -- total capital in USD
  currency      text           -- default 'USD'
  created_at    timestamptz

idea_reports
  id            uuid  PK
  workspace_id  uuid  FK → workspaces
  mode          text           -- 'validate' | 'generate'
  input_idea    text           -- null if mode = 'generate'
  budget        numeric        -- snapshot at run time
  status        text           -- 'pending' | 'running' | 'complete' | 'failed'
  created_at    timestamptz
  completed_at  timestamptz

report_sections
  id            uuid  PK
  report_id     uuid  FK → idea_reports
  section_type  text           -- 'report_card' | 'brand_brief' | 'variations' | 'pitch'
  content       jsonb
  created_at    timestamptz

data_snapshots
  id            uuid  PK
  report_id     uuid  FK → idea_reports
  source        text           -- 'google_trends' | 'serpapi'
  query         text
  response      jsonb
  fetched_at    timestamptz
```

**RLS policies:**
- `workspaces` — owner can SELECT/INSERT/UPDATE/DELETE their own row only
- `idea_reports` — access where workspace_id matches user's workspace
- `report_sections` + `data_snapshots` — access flows through idea_reports ownership

---

## Roles

**Sprint 1: Owner only.** One user per workspace. No invites, no member roles. Multi-user support deferred to Sprint 2.

---

## IdeaEngine — Wizard Flow

```
Step 1  Mode Select       — "I have an idea" or "Find me one"
Step 2A Idea Input        — text area for idea + optional context  (validate mode)
Step 2B skipped           — generate mode jumps straight to budget
Step 3  Budget Input      — dollar amount, covers all future spend
Step 4  Market Focus      — optional: region + category hint
Step 5  Running Screen    — live progress indicators while pipeline runs
Step 6  Report Dashboard  — destination on completion
```

---

## IdeaEngine — Backend Pipeline

`POST /idea-engine/run` triggers this sequence:

```
1. Save run → idea_reports (status: running)
2. Fetch data in parallel:
   ├── Google Trends API  → interest over time
   └── SerpAPI            → search results, shopping, news
3. Save raw responses → data_snapshots
4. Build structured prompt with data injected
5. Call Kimi 2.6 → returns JSON with all 4 sections
6. Parse response → save to report_sections (one row per section)
7. Update idea_reports (status: complete, completed_at: now)
8. Return report_id to frontend
```

---

## Kimi 2.6 Prompt Contract

**System prompt:**
> You are EagleEye's market intelligence engine. Analyze ecommerce opportunities using real market data and produce structured brand reports. Always ground your analysis in the data provided. Never invent statistics. Flag low-confidence signals explicitly.

**User message:** mode + idea + budget + market focus + raw Google Trends JSON + raw SerpAPI JSON

**Required JSON output shape:**
```json
{
  "report_card": {
    "demand_score": 0-100,
    "competition_score": 0-100,
    "margin_potential": "low|medium|high",
    "brand_angle": "string",
    "confidence_notes": "string"
  },
  "brand_brief": {
    "name": "string",
    "tagline": "string",
    "positioning": "string",
    "target_persona": "string",
    "emotional_triggers": ["string"],
    "product_list": ["string"],
    "price_points": {}
  },
  "variations": [
    { "idea": "string", "score": 0-100, "trade_offs": "string" }
  ],
  "pitch": {
    "tam": "string",
    "differentiation": "string",
    "go_to_market": "string",
    "one_liner": "string"
  }
}
```

---

## Report Dashboard Layout

```
┌──────────────────────────────────────────────────┐
│  EagleEye Report — [Idea Name]       [date]      │
├──────────────────────────────────────────────────┤
│  REPORT CARD                                     │
│  Demand ████████░░ 82   Competition ████░░ 41    │
│  Margin Potential: High  · Confidence: Medium    │
│  Brand Angle: [summary]                          │
├──────────────────────────────────────────────────┤
│  BRAND BRIEF                                     │
│  Name · Tagline · Persona · Emotional triggers   │
│  Product list · Price points                     │
├──────────────────────────────────────────────────┤
│  IDEA VARIATIONS              [expandable cards] │
├──────────────────────────────────────────────────┤
│  INVESTOR PITCH SUMMARY                          │
│  TAM · Differentiation · GTM · One-liner         │
└──────────────────────────────────────────────────┘
```

---

## Repo Structure

```
EagleEye/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── supabase.py
│   │   └── kimi.py
│   ├── routers/
│   │   ├── workspace.py
│   │   └── idea_engine.py
│   ├── services/
│   │   ├── idea_engine.py
│   │   ├── google_trends.py
│   │   └── serpapi.py
│   └── models/
│       ├── workspace.py
│       └── idea_engine.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    └── src/
        ├── app/
        │   ├── auth/login/page.tsx
        │   ├── auth/signup/page.tsx
        │   ├── onboarding/page.tsx
        │   ├── dashboard/page.tsx
        │   └── dashboard/idea-engine/
        │       ├── page.tsx
        │       └── report/[id]/page.tsx
        ├── components/
        │   ├── wizard/
        │   │   ├── WizardShell.tsx
        │   │   ├── ModeSelect.tsx
        │   │   ├── IdeaInput.tsx
        │   │   ├── BudgetInput.tsx
        │   │   ├── MarketFocus.tsx
        │   │   └── RunningScreen.tsx
        │   └── report/
        │       ├── ReportCard.tsx
        │       ├── BrandBrief.tsx
        │       ├── Variations.tsx
        │       └── PitchSummary.tsx
        ├── lib/
        │   ├── supabase.ts
        │   └── api.ts
        └── types/index.ts
```

---

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | Python 3.12 + FastAPI |
| Frontend | Next.js 14 (App Router) + TypeScript |
| Database | Supabase (Postgres + Auth + Storage) |
| AI Model | Kimi 2.6 (Moonshot AI API) |
| Data APIs | Google Trends API + SerpAPI |
| Hosting | Docker + VPS (DigitalOcean / Hetzner) |
| Language | English only |

---

## What Is Explicitly Out of Scope for Sprint 1

- Member invites / team roles
- SourcerAI, StoreBuilder, MarketingOS, DashboardHQ
- PDF export or shareable report links
- Arabic language support
- Mobile layout optimization
- Billing / subscription management
- Supplier outreach
