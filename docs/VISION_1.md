# EagleEye — Vision 1

_Captured from founder scoping session — 2026-05-16_

---

## Who Is This For

Anyone on earth who wants to start their own ecommerce business. They arrive with one of two things:

- An idea + some money
- Just money — no idea yet

No experience required. No team. No existing store. EagleEye takes them from zero to a running business.

---

## What EagleEye Is

A unified platform that replaces a full agency. Everything a person needs to go from spark to sale — idea validation, supplier sourcing, store building, and marketing — in one system.

**The moat:** No stitching together 6 tools. One platform, one context, one flow.

**The biggest risk to design around:** Data quality. If the AI gives confident but wrong market signals, the whole premise breaks. Every data-backed claim must be traceable to a real source.

---

## Core User Flows

### Entry Point A — User Has an Idea
User arrives with a niche or product concept. EagleEye challenges it:
- Validates demand with real market data
- Analyzes the psychological and branding opportunity behind it
- Scores it, surfaces variations, and produces a brand brief

### Entry Point B — User Has Money, No Idea
User sets a budget. EagleEye generates an idea:
- AI researches trending niches and demand signals
- Filters opportunities to fit the budget
- Produces a ranked set of ideas with full psychological and market backing

Both entry points feed into the same pipeline.

---

## The Pipeline (Full Vision)

```
[Budget Input at Onboarding]
         ↓
  [ IdeaEngine ]  ← Phase 1 MVP
  Validate or generate a niche idea
  Output: report card + brand brief + variations + pitch summary
         ↓
  [ SourcerAI ]   ← Phase 2
  Find and vet suppliers within budget
  Agent reaches out to suppliers via API/MCP where possible
         ↓
  [ StoreBuilder ]  ← Phase 2
  Scaffold a custom Next.js storefront
  Product listings, payment, shipping config
         ↓
  [ MarketingOS ]  ← Phase 3
  Ad campaigns (Meta, TikTok, Google)
  Email flows, content calendar
         ↓
  [ DashboardHQ ]  ← Phase 3
  Unified analytics across all modules
  Shipment tracking, ROAS, store performance
```

---

## IdeaEngine (MVP Module)

### Two Modes
| Mode | Trigger | What Happens |
|---|---|---|
| Validate | User has an idea | AI challenges it with real data and builds a brand brief around it |
| Generate | User has no idea | AI surfaces niche opportunities filtered by budget and data |

### Psychological Branding Layer
Every idea output includes:
- **Buyer persona** — who buys this, what pain or desire drives them
- **Brand identity** — AI-generated name, tone, positioning, origin story
- **Pricing psychology** — what price feels right to this buyer, anchoring strategy
- **Competitor positioning gaps** — what emotional angle competitors aren't owning

### IdeaEngine Output (all four)
1. **Report card** — demand score, competition score, margin potential, brand angle
2. **Brand brief** — name, positioning, persona, product list, price points (feeds StoreBuilder)
3. **Idea variations** — 3-5 alternatives ranked with trade-offs
4. **Investor pitch summary** — TAM, differentiation, go-to-market angle

---

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | Python + FastAPI |
| Frontend | Next.js (React) |
| Database | Supabase (Postgres + Auth + Storage) |
| AI Model | Kimi 2.6 (Moonshot AI) |
| Hosting | Docker + VPS (DigitalOcean / Hetzner) |
| Language | English only |

---

## Platform Architecture Principles

- **Multi-tenant** — each user/team has an isolated workspace; data never bleeds across accounts
- **Budget-constrained from day one** — set at onboarding, every recommendation stays inside it
- **Interface** — hybrid: chat to explore and initiate, structured dashboard to review results and act
- **AI UX** — streaming / async / step-by-step TBD based on what Kimi 2.6 and data APIs support
- **Supplier outreach** — via API or MCP if the platform supports it; otherwise a technical decision deferred to Phase 2
- **Store** — custom-built Next.js storefront, not Shopify

---

## Business Model

SaaS subscription — monthly and annual plans. Tiers TBD (likely Starter / Growth / Agency based on usage or seats).

---

## Phased Roadmap

### Phase 1 — Foundation + IdeaEngine (Sprint 1 focus)
- Auth + multi-tenant workspace
- Budget onboarding
- Kimi 2.6 integration
- IdeaEngine: both modes, psychological layer, full output
- **MVP success:** user inputs idea or budget → receives full report + brand brief

### Phase 2 — SourcerAI + StoreBuilder
- Supplier discovery filtered by budget
- Agent-driven outreach via API/MCP where possible
- Custom Next.js storefront scaffold with product listings

### Phase 3 — MarketingOS + DashboardHQ
- Ad campaign setup and management
- Email flows and content automation
- Unified analytics panel

---

## What We Are Not Building (Yet)
- Shopify integration
- Arabic language support
- Mobile app
- Logistics / fulfillment (far scope, not detailed now)
- Supplier outreach without API support (deferred)
