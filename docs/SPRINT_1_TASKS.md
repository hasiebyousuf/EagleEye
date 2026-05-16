# Sprint 1 — Task Board

_EagleEye · Sprint 1: Foundation + IdeaEngine_
_Created 2026-05-16_

Reference spec: `docs/specs/2026-05-16-sprint1-design.md`

---

## Execution Sequence

```
[1] Monorepo structure
[2] Docker Compose
[3] Supabase schema + RLS
[4] FastAPI scaffold ─┐
[5] Next.js scaffold  ─┘ (parallel)
[6] Auth flow
[7] Onboarding flow ─┐
[8] Workspace routes ─┘ (parallel)
[9]  Google Trends service ─┐
[10] SerpAPI service        ├─ (parallel)
[11] Kimi 2.6 client        ─┘
[12] IdeaEngine pipeline
[13] IdeaEngine routes
[14] Wizard UI
[15] Report dashboard ─┐
[16] Main dashboard   ─┘ (parallel)
[17] Deploy to VPS
```

---

## Tasks

### Infra

| # | Task | Status |
|---|---|---|
| 1 | Set up monorepo structure | completed |
| 2 | Configure Docker Compose | completed |
| 3 | Set up Supabase project and run schema migrations | in_progress |
| 17 | Deploy to VPS with Docker Compose | pending |

---

### Backend

| # | Task | Status |
|---|---|---|
| 4 | Scaffold FastAPI backend | completed |
| 8 | Implement workspace FastAPI routes | pending |
| 9 | Build Google Trends API service | pending |
| 10 | Build SerpAPI service | pending |
| 11 | Build Kimi 2.6 client and prompt builder | pending |
| 12 | Build IdeaEngine orchestration pipeline | pending |
| 13 | Implement IdeaEngine FastAPI routes | pending |

---

### Frontend

| # | Task | Status |
|---|---|---|
| 5 | Scaffold Next.js frontend | pending |
| 14 | Build IdeaEngine wizard UI | pending |
| 15 | Build report dashboard page | pending |
| 16 | Build main dashboard (past reports listing) | pending |

---

### Full-Stack (Backend + Frontend)

| # | Task | Status |
|---|---|---|
| 6 | Build auth flow (signup, login, session) | pending |
| 7 | Build onboarding flow (workspace + budget setup) | pending |

---

## Task Details

### [1] Set up monorepo structure
Create the EagleEye monorepo layout: `/backend`, `/frontend`, `docker-compose.yml`, `.env.example` as defined in the Sprint 1 spec.

### [2] Configure Docker Compose
Write `docker-compose.yml` that runs backend (FastAPI) and frontend (Next.js) as two containers. Include env var injection and networking so frontend can reach backend.

### [3] Set up Supabase project and run schema migrations
Create Supabase project. Write and run SQL migrations for: `workspaces`, `idea_reports`, `report_sections`, `data_snapshots`. Apply RLS policies for all tables.

**Schema:**
```sql
workspaces        (id, owner_id → auth.users, name, budget, currency, created_at)
idea_reports      (id, workspace_id, mode, input_idea, budget, status, created_at, completed_at)
report_sections   (id, report_id, section_type, content jsonb, created_at)
data_snapshots    (id, report_id, source, query, response jsonb, fetched_at)
```

**RLS rules:**
- `workspaces` — owner SELECT/INSERT/UPDATE/DELETE own row only
- `idea_reports` — access where workspace_id matches user's workspace
- `report_sections` + `data_snapshots` — access flows through idea_reports ownership

### [4] Scaffold FastAPI backend
Set up `main.py`, `requirements.txt`, `Dockerfile`. Wire up `core/config.py` (env vars), `core/supabase.py` (client init), `core/kimi.py` (Kimi 2.6 client stub). Empty routers and services folders with placeholder files.

### [5] Scaffold Next.js frontend
Set up Next.js 14 with App Router and TypeScript. Install dependencies. Create folder structure: `app/`, `components/wizard/`, `components/report/`, `lib/`, `types/`. Wire up Supabase browser client in `lib/supabase.ts` and typed FastAPI client in `lib/api.ts`.

### [6] Build auth flow (signup, login, session)
Implement `auth/signup/page.tsx` and `auth/login/page.tsx` using Supabase Auth. Handle session persistence, protected route middleware, and redirect logic:
- Unauthenticated → `/auth/login`
- Authenticated, no workspace → `/onboarding`
- Authenticated, has workspace → `/dashboard`

### [7] Build onboarding flow (workspace + budget setup)
Build `onboarding/page.tsx` — two-field form: workspace name + total budget. On submit, `POST /workspace` to FastAPI which creates the `workspaces` row in Supabase. Redirect to `/dashboard` on success.

### [8] Implement workspace FastAPI routes
Build `routers/workspace.py`:
- `POST /workspace` — create workspace, owner_id from JWT
- `GET /workspace` — fetch current user's workspace

Validate Supabase JWT on every request via middleware.

### [9] Build Google Trends API service
Implement `services/google_trends.py` — takes a keyword/niche string, calls Google Trends API, returns structured JSON with interest over time data. Handle rate limits and errors gracefully.

### [10] Build SerpAPI service
Implement `services/serpapi.py` — takes a keyword/niche string, calls SerpAPI for Google Shopping results, organic results, and news. Returns structured JSON. Handle errors and missing results.

### [11] Build Kimi 2.6 client and prompt builder
Implement `core/kimi.py` — Moonshot AI API client. Build the structured system prompt and user message that injects mode, idea, budget, market focus, Google Trends data, and SerpAPI data. Enforce JSON output shape:
```json
{
  "report_card":  { demand_score, competition_score, margin_potential, brand_angle, confidence_notes },
  "brand_brief":  { name, tagline, positioning, target_persona, emotional_triggers, product_list, price_points },
  "variations":   [{ idea, score, trade_offs }],
  "pitch":        { tam, differentiation, go_to_market, one_liner }
}
```

### [12] Build IdeaEngine orchestration pipeline
Implement `services/idea_engine.py` — full pipeline:
1. Save run → `idea_reports` (status: running)
2. Fetch Google Trends + SerpAPI in parallel
3. Save raw responses → `data_snapshots`
4. Build + send Kimi 2.6 prompt
5. Parse response → save to `report_sections` (one row per section)
6. Update `idea_reports` (status: complete, completed_at: now)

### [13] Implement IdeaEngine FastAPI routes
Build `routers/idea_engine.py`:
- `POST /idea-engine/run` — triggers pipeline, returns `report_id`
- `GET /idea-engine/report/{id}` — returns full report with all sections

Auth-gated, workspace-scoped.

### [14] Build IdeaEngine wizard UI
Build all wizard components:
- `WizardShell.tsx` — step controller and shared state
- `ModeSelect.tsx` — validate vs generate
- `IdeaInput.tsx` — idea text + optional context
- `BudgetInput.tsx` — dollar input
- `MarketFocus.tsx` — optional region + category
- `RunningScreen.tsx` — polls `GET /idea-engine/report/{id}` until complete, shows live step indicators

Wire into `dashboard/idea-engine/page.tsx`.

### [15] Build report dashboard page
Build `dashboard/idea-engine/report/[id]/page.tsx` — fetches report by ID, renders:
- `ReportCard.tsx` — scores with progress bars, margin potential, confidence note
- `BrandBrief.tsx` — name, tagline, persona, triggers, product list, price points
- `Variations.tsx` — expandable cards for each variation
- `PitchSummary.tsx` — TAM, differentiation, GTM, one-liner

Handle loading and error states.

### [16] Build main dashboard (past reports listing)
Build `dashboard/page.tsx` — home screen showing:
- Workspace name + budget
- List of past IdeaEngine reports with status badges and links
- Prominent "Run IdeaEngine" CTA

### [17] Deploy to VPS with Docker Compose
Set up DigitalOcean or Hetzner VPS. Install Docker. Copy `docker-compose.yml` and `.env`. Run containers. Configure reverse proxy (Nginx or Caddy). Verify end-to-end flow works in production.

---

## Definition of Done — Sprint 1

A user can:
1. Sign up and create a workspace with their budget
2. Enter an idea (or skip and let AI generate one)
3. Receive a full interactive report: report card, brand brief, idea variations, pitch summary
4. View past reports from their dashboard

All of the above works in production on the VPS.
