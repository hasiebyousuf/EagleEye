# Sprint 1 — Functional Requirements & Success Criteria

_EagleEye · Sprint 1: Foundation + IdeaEngine_
_Created 2026-05-16_

Each task below lists what it must do (functional requirements) and how we know it's done (success criteria). A task is not complete until every success criterion passes.

---

## Task 1 — Set Up Monorepo Structure

### Functional Requirements
- Root of EagleEye repo contains `/backend`, `/frontend`, `docker-compose.yml`, and `.env.example`
- `.env.example` documents every environment variable required by both services with a description and placeholder value
- No code lives at the root level — all application code is inside `/backend` or `/frontend`

### Success Criteria
- [ ] `ls` at repo root shows `backend/`, `frontend/`, `docker-compose.yml`, `.env.example`, `docs/`, `CLAUDE.md`, `README.md`
- [ ] `.env.example` contains entries for: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_ANON_KEY`, `KIMI_API_KEY`, `GOOGLE_TRENDS_API_KEY`, `SERPAPI_KEY`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `NEXT_PUBLIC_API_URL`
- [ ] No `.env` file committed to the repo (only `.env.example`)

---

## Task 2 — Configure Docker Compose

### Functional Requirements
- `docker-compose.yml` defines two services: `backend` (FastAPI, port 8000) and `frontend` (Next.js, port 3000)
- Both services share an internal Docker network so frontend can reach backend at `http://backend:8000`
- Environment variables are injected from a `.env` file at the root
- Both services have a health check defined
- Both services have a restart policy (`unless-stopped`)

### Success Criteria
- [ ] `docker-compose up --build` starts both services without errors
- [ ] `curl http://localhost:8000/health` returns `{"status": "ok"}`
- [ ] `curl http://localhost:3000` returns the Next.js app HTML
- [ ] Stopping and restarting with `docker-compose restart` brings both services back up
- [ ] No hardcoded secrets inside `docker-compose.yml`

---

## Task 3 — Set Up Supabase Project and Run Schema Migrations

### Functional Requirements
- Supabase project created with Postgres database
- Four tables created: `workspaces`, `idea_reports`, `report_sections`, `data_snapshots`
- All columns match the spec exactly (types, nullability, foreign keys)
- Row Level Security (RLS) enabled on all four tables
- Three RLS policies applied:
  - `workspaces`: owner can SELECT / INSERT / UPDATE / DELETE their own row only
  - `idea_reports`: user can access rows where `workspace_id` belongs to their workspace
  - `report_sections` + `data_snapshots`: access flows through `idea_reports` ownership
- Migration SQL files saved to `/backend/migrations/` and committed to the repo

### Success Criteria
- [ ] All four tables exist in Supabase with correct columns and types
- [ ] RLS is enabled on all four tables (visible in Supabase dashboard)
- [ ] User A cannot query User B's `workspaces` row — returns empty result, not an error
- [ ] User A cannot query `idea_reports` belonging to User B's workspace
- [ ] `report_sections` and `data_snapshots` are inaccessible if the parent `idea_reports` row is not owned by the requesting user
- [ ] Migration SQL files are committed under `/backend/migrations/`

---

## Task 4 — Scaffold FastAPI Backend

### Functional Requirements
- FastAPI app initialises in `main.py` with CORS configured to accept requests from the frontend origin
- `core/config.py` loads all env vars using Pydantic Settings — app fails to start if required vars are missing
- `core/supabase.py` initialises the Supabase Python client using the service key
- `core/kimi.py` contains a stub Kimi 2.6 client (method signatures only, not yet implemented)
- `routers/` and `services/` contain placeholder files with empty functions and correct signatures
- `Dockerfile` builds the backend image successfully
- `requirements.txt` pins all dependencies with versions

### Success Criteria
- [ ] `uvicorn main:app --reload` starts without errors
- [ ] `GET /health` returns `{"status": "ok"}` with HTTP 200
- [ ] Starting with a missing required env var raises a clear startup error naming the missing variable
- [ ] `docker build -t eagleeye-backend ./backend` completes without errors
- [ ] All modules (`core/`, `routers/`, `services/`, `models/`) import without errors

---

## Task 5 — Scaffold Next.js Frontend

### Functional Requirements
- Next.js 14 app with App Router and TypeScript strict mode enabled
- Folder structure matches spec: `app/`, `components/wizard/`, `components/report/`, `lib/`, `types/`
- `lib/supabase.ts` exports an initialised Supabase browser client
- `lib/api.ts` exports a typed fetch wrapper that prefixes all calls with `NEXT_PUBLIC_API_URL` and attaches the Supabase JWT to every request
- `types/index.ts` defines TypeScript types for: `Workspace`, `IdeaReport`, `ReportSection`, `ReportCard`, `BrandBrief`, `Variation`, `Pitch`
- `Dockerfile` builds the frontend image successfully

### Success Criteria
- [ ] `npm run dev` starts without errors on port 3000
- [ ] `npm run build` completes with zero TypeScript errors
- [ ] `lib/supabase.ts` and `lib/api.ts` export their clients without runtime errors
- [ ] All types in `types/index.ts` match the database schema and API response shapes
- [ ] `docker build -t eagleeye-frontend ./frontend` completes without errors

---

## Task 6 — Build Auth Flow (Signup, Login, Session)

### Functional Requirements
- `/auth/signup` page: email + password form, submits to Supabase Auth, shows validation errors inline
- `/auth/login` page: email + password form, submits to Supabase Auth, shows invalid credentials error
- Session persists across page refresh using Supabase session storage
- Middleware enforces three redirect rules:
  - Unauthenticated user visiting any protected route → `/auth/login`
  - Authenticated user with no workspace → `/onboarding`
  - Authenticated user with workspace → `/dashboard`
- Logout clears session and redirects to `/auth/login`

### Success Criteria
- [ ] Signing up with a valid email + password creates a user in Supabase `auth.users`
- [ ] After signup, user is redirected to `/onboarding`
- [ ] Logging in with correct credentials creates a session and redirects to `/dashboard`
- [ ] Logging in with wrong credentials shows an inline error message
- [ ] Refreshing the page while logged in keeps the user logged in
- [ ] Visiting `/dashboard` while logged out redirects to `/auth/login`
- [ ] Visiting `/dashboard` while logged in but with no workspace redirects to `/onboarding`
- [ ] Logging out clears the session and redirects to `/auth/login`

---

## Task 7 — Build Onboarding Flow (Workspace + Budget Setup)

### Functional Requirements
- `/onboarding` page shows two fields: workspace name (text) and total budget (number in USD)
- Form validates: workspace name is required and non-empty; budget must be a positive number greater than zero
- On valid submit, frontend calls `POST /workspace` via `lib/api.ts`
- On success, user is redirected to `/dashboard`
- If a user already has a workspace and visits `/onboarding`, they are redirected to `/dashboard`

### Success Criteria
- [ ] Submitting a valid form creates a row in `workspaces` with correct `owner_id`, `name`, and `budget`
- [ ] Submitting with an empty workspace name shows a validation error and does not call the API
- [ ] Submitting with budget = 0 or negative shows a validation error and does not call the API
- [ ] After successful submission, user lands on `/dashboard`
- [ ] Visiting `/onboarding` when a workspace already exists redirects to `/dashboard`
- [ ] The created workspace is only accessible by the owner (RLS enforced)

---

## Task 8 — Implement Workspace FastAPI Routes

### Functional Requirements
- `POST /workspace`: creates a new workspace row with `owner_id` extracted from the Supabase JWT; returns the created workspace object
- `GET /workspace`: returns the authenticated user's workspace; returns 404 if none exists
- Every route validates the Supabase JWT via middleware — missing or invalid JWT returns 401
- A user cannot create more than one workspace (returns 409 if one already exists)

### Success Criteria
- [ ] `POST /workspace` with valid JWT and body creates workspace and returns it with HTTP 201
- [ ] `GET /workspace` with valid JWT returns the user's workspace with HTTP 200
- [ ] `GET /workspace` when no workspace exists returns HTTP 404
- [ ] Any request without `Authorization: Bearer <token>` header returns HTTP 401
- [ ] Any request with an expired or invalid JWT returns HTTP 401
- [ ] `POST /workspace` when a workspace already exists returns HTTP 409
- [ ] User A's JWT cannot retrieve User B's workspace via `GET /workspace`

---

## Task 9 — Build Google Trends API Service

### Functional Requirements
- `services/google_trends.py` exposes a function `fetch_trends(keyword: str, region: str = "US") -> dict`
- Calls the Google Trends API and returns interest-over-time data for the keyword
- Handles API errors (rate limit, timeout, invalid key) by raising a descriptive `DataFetchError`
- Handles empty results (unknown keyword) by returning an empty list, not raising an error
- Response is structured as: `{ "keyword": str, "region": str, "interest_over_time": [{"date": str, "value": int}] }`

### Success Criteria
- [ ] `fetch_trends("wireless earbuds")` returns a non-empty `interest_over_time` array
- [ ] `fetch_trends("xkzqwjfhdsjakl")` returns `interest_over_time: []` without raising an error
- [ ] API timeout raises `DataFetchError` with a message describing the failure
- [ ] Invalid API key raises `DataFetchError` on initialisation, not silently at call time
- [ ] Return value always matches the defined structure regardless of input

---

## Task 10 — Build SerpAPI Service

### Functional Requirements
- `services/serpapi.py` exposes a function `fetch_serp_data(keyword: str, region: str = "us") -> dict`
- Calls SerpAPI and returns: shopping results, organic search results, and news results
- Each result type is returned as an array — empty array if no results, not an error
- Handles API errors by raising `DataFetchError`
- Response structure: `{ "keyword": str, "shopping": [...], "organic": [...], "news": [...] }`

### Success Criteria
- [ ] `fetch_serp_data("wireless earbuds")` returns at least one non-empty result array
- [ ] Obscure keyword returns arrays that may be empty but does not raise an error
- [ ] API failure raises `DataFetchError` with a clear message
- [ ] Response always contains all three keys (`shopping`, `organic`, `news`) even if some are empty arrays
- [ ] Invalid API key raises `DataFetchError`

---

## Task 11 — Build Kimi 2.6 Client and Prompt Builder

### Functional Requirements
- `core/kimi.py` authenticates with the Moonshot AI API using `KIMI_API_KEY`
- `build_prompt(mode, idea, budget, market_focus, trends_data, serp_data) -> dict` constructs the full system + user message
- System prompt instructs Kimi to: ground all analysis in provided data, never invent statistics, flag low-confidence signals explicitly
- User message injects all input data in a structured format
- Response is parsed and validated against the required 4-section JSON schema
- If Kimi returns malformed JSON or missing keys, raises `AIResponseError`

### Success Criteria
- [ ] A valid call to Kimi 2.6 returns a JSON object with exactly these keys: `report_card`, `brand_brief`, `variations`, `pitch`
- [ ] `report_card` contains: `demand_score` (int 0-100), `competition_score` (int 0-100), `margin_potential` (low/medium/high), `brand_angle` (str), `confidence_notes` (str)
- [ ] `brand_brief` contains: `name`, `tagline`, `positioning`, `target_persona`, `emotional_triggers` (list), `product_list` (list), `price_points` (dict)
- [ ] `variations` is a list of 3-5 objects each with `idea`, `score`, `trade_offs`
- [ ] `pitch` contains: `tam`, `differentiation`, `go_to_market`, `one_liner`
- [ ] Malformed or incomplete response raises `AIResponseError` with detail on what's missing
- [ ] Invalid API key raises `AIResponseError` on first call

---

## Task 12 — Build IdeaEngine Orchestration Pipeline

### Functional Requirements
- `services/idea_engine.py` exposes `run_pipeline(report_id, mode, idea, budget, market_focus, workspace_id)`
- Step 1: Update `idea_reports.status` to `running`
- Step 2: Fetch Google Trends and SerpAPI data in parallel (using `asyncio.gather`)
- Step 3: Save both raw API responses to `data_snapshots` (one row per source)
- Step 4: Build Kimi 2.6 prompt with all data injected
- Step 5: Call Kimi 2.6 and parse JSON response
- Step 6: Save 4 rows to `report_sections` (one per section type)
- Step 7: Update `idea_reports.status` to `complete` and set `completed_at`
- If any step fails: update `idea_reports.status` to `failed`, log the error, do not crash the server

### Success Criteria
- [ ] After a successful run: `idea_reports.status = 'complete'`
- [ ] After a successful run: exactly 4 rows exist in `report_sections` for the report
- [ ] After a successful run: exactly 2 rows exist in `data_snapshots` for the report (one Google Trends, one SerpAPI)
- [ ] Steps 2 (data fetch) run in parallel — total fetch time is less than the sum of both individual fetch times
- [ ] If Kimi call fails: `idea_reports.status = 'failed'`, error is logged, server does not crash
- [ ] If a data fetch fails: `idea_reports.status = 'failed'`, error is logged, Kimi is not called

---

## Task 13 — Implement IdeaEngine FastAPI Routes

### Functional Requirements
- `POST /idea-engine/run`: accepts `{ mode, input_idea (optional), budget, market_focus (optional) }`; creates `idea_reports` row with status `pending`; triggers pipeline as a FastAPI `BackgroundTask` (non-blocking); returns `{ report_id }` immediately
- `GET /idea-engine/report/{id}`: returns the full report including `idea_reports` metadata and all `report_sections`; returns 404 if not found; returns 403 if the report belongs to a different user's workspace
- Both routes are auth-gated via JWT middleware
- `mode` must be `validate` or `generate` — invalid value returns 422
- If `mode = validate`, `input_idea` is required — missing value returns 422

### Success Criteria
- [ ] `POST /idea-engine/run` returns `{ report_id }` within 300ms (pipeline runs in background)
- [ ] After posting, `idea_reports` row exists with `status = 'pending'` or `'running'`
- [ ] `GET /idea-engine/report/{id}` returns all 4 sections once pipeline completes
- [ ] `GET /idea-engine/report/{id}` with non-existent ID returns HTTP 404
- [ ] `GET /idea-engine/report/{id}` with another user's report ID returns HTTP 403
- [ ] `POST` without auth returns HTTP 401
- [ ] `POST` with `mode = validate` and no `input_idea` returns HTTP 422
- [ ] `POST` with invalid `mode` value returns HTTP 422

---

## Task 14 — Build IdeaEngine Wizard UI

### Functional Requirements
- `WizardShell.tsx` manages current step index and all wizard state; renders the correct step component
- `ModeSelect.tsx`: two options — "I have an idea" (validate) and "Find me one" (generate); selection advances to next step
- `IdeaInput.tsx`: text area for idea + optional context field; shown only in validate mode; "Next" button disabled until idea field has content
- `BudgetInput.tsx`: dollar input field; must be a positive number; "Next" disabled until valid
- `MarketFocus.tsx`: optional region dropdown + optional category text field; has a "Skip and Run" option
- `RunningScreen.tsx`: calls `POST /idea-engine/run` on mount; polls `GET /idea-engine/report/{id}` every 3 seconds; shows four labelled progress steps with animated indicators; on `status = complete` redirects to `/dashboard/idea-engine/report/[id]`; on `status = failed` shows error message with retry option
- Wizard is wired into `dashboard/idea-engine/page.tsx`

### Success Criteria
- [ ] User completes wizard in validate mode: all 5 steps appear in correct order
- [ ] User completes wizard in generate mode: IdeaInput step is skipped
- [ ] Clicking "Next" on IdeaInput with empty idea field does nothing
- [ ] Clicking "Next" on BudgetInput with 0 or negative value does nothing
- [ ] RunningScreen shows 4 progress indicators while polling
- [ ] On pipeline completion, user is automatically redirected to the report page
- [ ] On pipeline failure, error message is shown with a "Try Again" button that restarts the wizard
- [ ] Navigating away from the wizard mid-flow and returning resets the wizard to step 1

---

## Task 15 — Build Report Dashboard Page

### Functional Requirements
- `dashboard/idea-engine/report/[id]/page.tsx` fetches the report using `GET /idea-engine/report/{id}` via `lib/api.ts`
- `ReportCard.tsx`: renders `demand_score` and `competition_score` as labelled progress bars (0-100); displays `margin_potential` as a badge (low/medium/high with colour coding); displays `brand_angle` and `confidence_notes` as text
- `BrandBrief.tsx`: renders all brand brief fields — name (large heading), tagline, positioning, target persona, emotional triggers (tag chips), product list (bulleted), price points (table)
- `Variations.tsx`: renders each variation as an expandable card showing idea, score bar, and trade-offs; collapsed by default, click to expand
- `PitchSummary.tsx`: renders TAM, differentiation, go-to-market, and one-liner in a clean structured layout
- Loading state shown while report is fetching
- Error state shown if report is not found or access is denied

### Success Criteria
- [ ] All four sections render correctly with real data from a completed report
- [ ] `demand_score: 82` renders as a progress bar filled to 82%
- [ ] `margin_potential: high` renders as a green badge; `medium` as yellow; `low` as red
- [ ] Each variation card is collapsed by default and expands on click
- [ ] Visiting a report ID that does not exist shows a "Report not found" message
- [ ] Visiting another user's report ID shows an "Access denied" message
- [ ] While the report is loading, a skeleton or spinner is shown in place of each section

---

## Task 16 — Build Main Dashboard (Past Reports Listing)

### Functional Requirements
- `dashboard/page.tsx` fetches the user's workspace via `GET /workspace` and their past reports via `GET /idea-engine/reports` (list endpoint)
- Displays workspace name and budget prominently at the top
- Lists all past `idea_reports` ordered by `created_at` descending
- Each report row shows: mode (validate/generate), status badge, date created, and a link to the report (only if status = complete)
- Empty state shown when no reports exist yet
- Prominent "Run IdeaEngine" button that navigates to `/dashboard/idea-engine`

### Success Criteria
- [ ] Dashboard loads and displays workspace name and budget correctly
- [ ] All past reports are listed in descending order by date
- [ ] Status badges show correct state: `pending` (grey), `running` (blue/animated), `complete` (green), `failed` (red)
- [ ] Clicking a completed report navigates to `/dashboard/idea-engine/report/[id]`
- [ ] Pending or failed reports do not have a clickable link
- [ ] When no reports exist, an empty state message is shown with a CTA to run IdeaEngine
- [ ] "Run IdeaEngine" button navigates to the wizard

---

## Task 17 — Deploy to VPS with Docker Compose

### Functional Requirements
- VPS provisioned (DigitalOcean or Hetzner) with Docker and Docker Compose installed
- `docker-compose.yml` runs in production mode with production env vars in `.env`
- Reverse proxy (Nginx or Caddy) routes:
  - Port 80/443 → frontend (Next.js on port 3000)
  - `/api/*` → backend (FastAPI on port 8000)
- Both containers configured with `restart: unless-stopped`
- HTTPS configured (SSL certificate via Let's Encrypt or Caddy auto-TLS)
- Production `.env` contains all real API keys — never committed to the repo

### Success Criteria
- [ ] Frontend is accessible at the production URL and returns the app
- [ ] `GET https://[domain]/api/health` returns `{"status": "ok"}`
- [ ] Full end-to-end flow works in production: signup → onboarding → wizard → report renders
- [ ] Rebooting the VPS brings both containers back up automatically
- [ ] No API keys or secrets are present anywhere in the git repo
- [ ] HTTPS is active — HTTP redirects to HTTPS

---

## Sprint 1 — Definition of Done

Sprint 1 is complete when a user can:

1. Sign up with email and password
2. Create a workspace with their name and budget
3. Run IdeaEngine in either mode (validate an idea or generate one)
4. See live progress while the pipeline runs
5. View a full interactive report: report card, brand brief, idea variations, pitch summary
6. Return to the dashboard and see their past reports

All of the above must work end-to-end in the production environment on the VPS.
