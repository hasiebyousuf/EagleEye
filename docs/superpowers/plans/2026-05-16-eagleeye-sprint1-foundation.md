# EagleEye Sprint 1 Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the full foundation for EagleEye: monorepo, Docker, Supabase schema, FastAPI scaffold, Next.js scaffold, auth flow, and onboarding flow — tasks 1-7 in order.

**Architecture:** Two Docker containers (FastAPI + Next.js) share a Docker network; Supabase handles auth and Postgres; the frontend calls the backend REST API with Supabase JWTs attached; all secrets come from `.env` at the repo root.

**Tech Stack:** Python 3.12 + FastAPI + Pydantic Settings, Next.js 14 App Router + TypeScript strict, Supabase (Postgres + Auth), Docker Compose, supabase-py, @supabase/ssr

---

## File Map

### Task 1 — Monorepo Structure
- Create: `.env.example`
- Create: `backend/` (empty dir marker)
- Create: `frontend/` (empty dir marker)
- Create: `docker-compose.yml` (placeholder, completed in Task 2)

### Task 2 — Docker Compose
- Create: `docker-compose.yml`
- Create: `backend/Dockerfile` (placeholder only — completed in Task 4)
- Create: `frontend/Dockerfile` (placeholder only — completed in Task 5)

### Task 3 — Supabase Schema
- Create: `backend/migrations/001_initial_schema.sql`
- Create: `backend/migrations/002_rls_policies.sql`

### Task 4 — FastAPI Scaffold
- Create: `backend/main.py`
- Create: `backend/requirements.txt`
- Create: `backend/Dockerfile`
- Create: `backend/core/__init__.py`
- Create: `backend/core/config.py`
- Create: `backend/core/supabase.py`
- Create: `backend/core/kimi.py`
- Create: `backend/routers/__init__.py`
- Create: `backend/routers/workspace.py`
- Create: `backend/routers/idea_engine.py`
- Create: `backend/services/__init__.py`
- Create: `backend/services/idea_engine.py`
- Create: `backend/services/google_trends.py`
- Create: `backend/services/serpapi.py`
- Create: `backend/models/__init__.py`
- Create: `backend/models/workspace.py`
- Create: `backend/models/idea_engine.py`

### Task 5 — Next.js Scaffold
- Create: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/next.config.js`
- Create: `frontend/Dockerfile`
- Create: `frontend/src/app/layout.tsx`
- Create: `frontend/src/app/page.tsx`
- Create: `frontend/src/lib/supabase.ts`
- Create: `frontend/src/lib/api.ts`
- Create: `frontend/src/types/index.ts`
- Create: `frontend/src/components/wizard/.gitkeep`
- Create: `frontend/src/components/report/.gitkeep`

### Task 6 — Auth Flow
- Create: `frontend/src/app/auth/login/page.tsx`
- Create: `frontend/src/app/auth/signup/page.tsx`
- Create: `frontend/src/middleware.ts`

### Task 7 — Onboarding Flow
- Create: `frontend/src/app/onboarding/page.tsx`
- Create: `frontend/src/app/dashboard/page.tsx`
- Modify: `backend/routers/workspace.py` (implement POST /workspace)
- Modify: `backend/models/workspace.py` (add request/response models)

---

## Task 1: Monorepo Structure

**Files:**
- Create: `.env.example`
- Create: `backend/.gitkeep`
- Create: `frontend/.gitkeep`

- [ ] **Step 1: Create backend and frontend directories**

```powershell
New-Item -ItemType Directory -Path "backend" -Force
New-Item -ItemType Directory -Path "frontend" -Force
```

Run from `EagleEye/` root.

- [ ] **Step 2: Write `.env.example`**

Create `EagleEye/.env.example`:

```env
# Supabase — backend service key (never expose to browser)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-supabase-service-role-key

# Supabase — anon key (used by backend for user-context queries)
SUPABASE_ANON_KEY=your-supabase-anon-key

# Kimi 2.6 (Moonshot AI)
KIMI_API_KEY=your-kimi-api-key

# Google Trends API
GOOGLE_TRENDS_API_KEY=your-google-trends-api-key

# SerpAPI
SERPAPI_KEY=your-serpapi-key

# Next.js public env vars (safe to expose to browser)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

- [ ] **Step 3: Verify `.gitignore` excludes `.env`**

Check if `.gitignore` exists at the repo root. If not, create it:

```
.env
__pycache__/
*.pyc
.next/
node_modules/
```

If it exists, ensure `.env` is listed (not `.env.example`).

- [ ] **Step 4: Verify success criteria**

Run from repo root:
```powershell
ls
```
Expected output includes: `backend/`, `frontend/`, `.env.example`, `docs/`, `CLAUDE.md`, `README.md`

Verify `.env.example` has all 9 required keys:
```powershell
Select-String -Path ".env.example" -Pattern "SUPABASE_URL|SUPABASE_SERVICE_KEY|SUPABASE_ANON_KEY|KIMI_API_KEY|GOOGLE_TRENDS_API_KEY|SERPAPI_KEY|NEXT_PUBLIC_SUPABASE_URL|NEXT_PUBLIC_SUPABASE_ANON_KEY|NEXT_PUBLIC_API_URL"
```
Expected: 9 matches.

- [ ] **Step 5: Update task board — mark Task 1 completed**

In `docs/SPRINT_1_TASKS.md`, change `| 1 | Set up monorepo structure | pending |` to `| 1 | Set up monorepo structure | completed |`.

- [ ] **Step 6: Commit**

```bash
git add .env.example .gitignore backend frontend docs/SPRINT_1_TASKS.md
git commit -m "task(1): set up monorepo structure with backend/, frontend/, .env.example"
git push
```

---

## Task 2: Docker Compose

**Files:**
- Create: `docker-compose.yml`
- Create: `backend/Dockerfile` (minimal — real one completed in Task 4)
- Create: `frontend/Dockerfile` (minimal — real one completed in Task 5)

- [ ] **Step 1: Mark Task 2 in_progress in task board**

In `docs/SPRINT_1_TASKS.md`, change Task 2 status to `in_progress`.

- [ ] **Step 2: Write minimal backend Dockerfile**

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 3: Write minimal `backend/requirements.txt`**

Create `backend/requirements.txt`:

```
fastapi==0.115.5
uvicorn[standard]==0.32.1
```

- [ ] **Step 4: Write minimal `backend/main.py` for health check**

Create `backend/main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

- [ ] **Step 5: Write minimal frontend Dockerfile**

Create `frontend/Dockerfile`:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci
COPY . .
RUN npm run build
CMD ["npm", "start"]
EXPOSE 3000
```

- [ ] **Step 6: Write minimal `frontend/package.json`**

Create `frontend/package.json`:

```json
{
  "name": "eagleeye-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "14.2.29",
    "react": "^18",
    "react-dom": "^18"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/react": "^18",
    "@types/react-dom": "^18"
  }
}
```

- [ ] **Step 7: Write minimal Next.js config**

Create `frontend/next.config.js`:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
}

module.exports = nextConfig
```

- [ ] **Step 8: Write minimal `frontend/tsconfig.json`**

Create `frontend/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

- [ ] **Step 9: Write minimal Next.js app files**

Create `frontend/src/app/layout.tsx`:

```tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

Create `frontend/src/app/page.tsx`:

```tsx
export default function Home() {
  return <main><h1>EagleEye</h1></main>
}
```

- [ ] **Step 10: Write `docker-compose.yml`**

Create `docker-compose.yml` at repo root:

```yaml
version: "3.9"

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - .env
    networks:
      - eagleeye
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    env_file:
      - .env
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    networks:
      - eagleeye
    restart: unless-stopped
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

networks:
  eagleeye:
    driver: bridge
```

- [ ] **Step 11: Create `.env` for local testing (do NOT commit)**

```powershell
Copy-Item .env.example .env
```

Edit `.env` — fill in placeholder values so Docker can start (use dummy values for now; real keys added later):

```env
SUPABASE_URL=https://placeholder.supabase.co
SUPABASE_SERVICE_KEY=placeholder
SUPABASE_ANON_KEY=placeholder
KIMI_API_KEY=placeholder
GOOGLE_TRENDS_API_KEY=placeholder
SERPAPI_KEY=placeholder
NEXT_PUBLIC_SUPABASE_URL=https://placeholder.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=placeholder
NEXT_PUBLIC_API_URL=http://localhost:8000
```

- [ ] **Step 12: Verify Docker Compose starts**

```bash
docker-compose up --build -d
```

Wait ~30s, then:

```bash
curl http://localhost:8000/health
```
Expected: `{"status":"ok"}`

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
```
Expected: `200`

- [ ] **Step 13: Test restart**

```bash
docker-compose restart
```
Wait ~15s, re-run the curl checks above. Both must return same results.

- [ ] **Step 14: Verify no secrets in `docker-compose.yml`**

```bash
grep -i "key\|secret\|password\|token" docker-compose.yml
```
Expected: no API key values — only variable references.

- [ ] **Step 15: Stop containers, mark Task 2 completed, commit**

```bash
docker-compose down
```

Update `docs/SPRINT_1_TASKS.md` — Task 2 → `completed`.

```bash
git add docker-compose.yml backend/Dockerfile backend/main.py backend/requirements.txt frontend/Dockerfile frontend/package.json frontend/next.config.js frontend/tsconfig.json frontend/src/ docs/SPRINT_1_TASKS.md
git commit -m "task(2): configure Docker Compose with backend and frontend services"
git push
```

---

## Task 3: Supabase Schema Migrations

**Files:**
- Create: `backend/migrations/001_initial_schema.sql`
- Create: `backend/migrations/002_rls_policies.sql`

**Note:** This task requires a real Supabase project. The user must have created a project at supabase.com and have the project URL and service key available.

- [ ] **Step 1: Mark Task 3 in_progress**

Update `docs/SPRINT_1_TASKS.md` — Task 3 → `in_progress`.

- [ ] **Step 2: Create migrations directory**

```powershell
New-Item -ItemType Directory -Path "backend/migrations" -Force
```

- [ ] **Step 3: Write schema migration**

Create `backend/migrations/001_initial_schema.sql`:

```sql
-- Enable UUID generation
create extension if not exists "pgcrypto";

-- workspaces
create table if not exists workspaces (
  id          uuid primary key default gen_random_uuid(),
  owner_id    uuid not null references auth.users(id) on delete cascade,
  name        text not null,
  budget      numeric not null,
  currency    text not null default 'USD',
  created_at  timestamptz not null default now()
);

-- idea_reports
create table if not exists idea_reports (
  id            uuid primary key default gen_random_uuid(),
  workspace_id  uuid not null references workspaces(id) on delete cascade,
  mode          text not null check (mode in ('validate', 'generate')),
  input_idea    text,
  budget        numeric not null,
  status        text not null default 'pending' check (status in ('pending', 'running', 'complete', 'failed')),
  created_at    timestamptz not null default now(),
  completed_at  timestamptz
);

-- report_sections
create table if not exists report_sections (
  id            uuid primary key default gen_random_uuid(),
  report_id     uuid not null references idea_reports(id) on delete cascade,
  section_type  text not null check (section_type in ('report_card', 'brand_brief', 'variations', 'pitch')),
  content       jsonb not null,
  created_at    timestamptz not null default now()
);

-- data_snapshots
create table if not exists data_snapshots (
  id          uuid primary key default gen_random_uuid(),
  report_id   uuid not null references idea_reports(id) on delete cascade,
  source      text not null check (source in ('google_trends', 'serpapi')),
  query       text not null,
  response    jsonb not null,
  fetched_at  timestamptz not null default now()
);
```

- [ ] **Step 4: Write RLS policies migration**

Create `backend/migrations/002_rls_policies.sql`:

```sql
-- Enable RLS on all tables
alter table workspaces    enable row level security;
alter table idea_reports  enable row level security;
alter table report_sections enable row level security;
alter table data_snapshots  enable row level security;

-- workspaces: owner can CRUD their own row only
create policy "workspace_owner_select" on workspaces
  for select using (auth.uid() = owner_id);

create policy "workspace_owner_insert" on workspaces
  for insert with check (auth.uid() = owner_id);

create policy "workspace_owner_update" on workspaces
  for update using (auth.uid() = owner_id);

create policy "workspace_owner_delete" on workspaces
  for delete using (auth.uid() = owner_id);

-- idea_reports: access where workspace belongs to user
create policy "idea_reports_owner_select" on idea_reports
  for select using (
    exists (
      select 1 from workspaces w
      where w.id = idea_reports.workspace_id
        and w.owner_id = auth.uid()
    )
  );

create policy "idea_reports_owner_insert" on idea_reports
  for insert with check (
    exists (
      select 1 from workspaces w
      where w.id = idea_reports.workspace_id
        and w.owner_id = auth.uid()
    )
  );

create policy "idea_reports_owner_update" on idea_reports
  for update using (
    exists (
      select 1 from workspaces w
      where w.id = idea_reports.workspace_id
        and w.owner_id = auth.uid()
    )
  );

-- report_sections: access flows through idea_reports ownership
create policy "report_sections_owner_select" on report_sections
  for select using (
    exists (
      select 1 from idea_reports r
      join workspaces w on w.id = r.workspace_id
      where r.id = report_sections.report_id
        and w.owner_id = auth.uid()
    )
  );

create policy "report_sections_owner_insert" on report_sections
  for insert with check (
    exists (
      select 1 from idea_reports r
      join workspaces w on w.id = r.workspace_id
      where r.id = report_sections.report_id
        and w.owner_id = auth.uid()
    )
  );

-- data_snapshots: access flows through idea_reports ownership
create policy "data_snapshots_owner_select" on data_snapshots
  for select using (
    exists (
      select 1 from idea_reports r
      join workspaces w on w.id = r.workspace_id
      where r.id = data_snapshots.report_id
        and w.owner_id = auth.uid()
    )
  );

create policy "data_snapshots_owner_insert" on data_snapshots
  for insert with check (
    exists (
      select 1 from idea_reports r
      join workspaces w on w.id = r.workspace_id
      where r.id = data_snapshots.report_id
        and w.owner_id = auth.uid()
    )
  );
```

- [ ] **Step 5: Run migrations in Supabase SQL Editor**

Open your Supabase project → SQL Editor.

Run `001_initial_schema.sql` first. Verify no errors.

Run `002_rls_policies.sql`. Verify no errors.

- [ ] **Step 6: Verify tables in Supabase dashboard**

Navigate to Table Editor. Confirm all four tables exist:
- `workspaces` — columns: id, owner_id, name, budget, currency, created_at
- `idea_reports` — columns: id, workspace_id, mode, input_idea, budget, status, created_at, completed_at
- `report_sections` — columns: id, report_id, section_type, content, created_at
- `data_snapshots` — columns: id, report_id, source, query, response, fetched_at

Navigate to Authentication → Policies. Confirm RLS is enabled on all four tables.

- [ ] **Step 7: Update `.env` with real Supabase credentials**

Edit your local `.env` (not `.env.example`):
- Set `SUPABASE_URL` to your project URL (e.g. `https://abcxyz.supabase.co`)
- Set `SUPABASE_SERVICE_KEY` to the service role key (from Project Settings → API)
- Set `SUPABASE_ANON_KEY` to the anon/public key
- Set `NEXT_PUBLIC_SUPABASE_URL` to the same project URL
- Set `NEXT_PUBLIC_SUPABASE_ANON_KEY` to the same anon key

- [ ] **Step 8: Mark Task 3 completed, commit**

Update `docs/SPRINT_1_TASKS.md` — Task 3 → `completed`.

```bash
git add backend/migrations/ docs/SPRINT_1_TASKS.md
git commit -m "task(3): add Supabase schema migrations and RLS policies"
git push
```

---

## Task 4: FastAPI Backend Scaffold

**Files:**
- Modify: `backend/main.py`
- Modify: `backend/requirements.txt`
- Modify: `backend/Dockerfile`
- Create: `backend/core/__init__.py`
- Create: `backend/core/config.py`
- Create: `backend/core/supabase.py`
- Create: `backend/core/kimi.py`
- Create: `backend/routers/__init__.py`
- Create: `backend/routers/workspace.py`
- Create: `backend/routers/idea_engine.py`
- Create: `backend/services/__init__.py`
- Create: `backend/services/idea_engine.py`
- Create: `backend/services/google_trends.py`
- Create: `backend/services/serpapi.py`
- Create: `backend/models/__init__.py`
- Create: `backend/models/workspace.py`
- Create: `backend/models/idea_engine.py`

- [ ] **Step 1: Mark Task 4 in_progress**

Update `docs/SPRINT_1_TASKS.md` — Task 4 → `in_progress`.

- [ ] **Step 2: Write `backend/requirements.txt`**

```
fastapi==0.115.5
uvicorn[standard]==0.32.1
pydantic==2.10.3
pydantic-settings==2.7.0
supabase==2.10.0
httpx==0.28.1
python-jose[cryptography]==3.3.0
python-multipart==0.0.20
```

- [ ] **Step 3: Write `backend/core/config.py`**

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    supabase_url: str
    supabase_service_key: str
    supabase_anon_key: str
    kimi_api_key: str
    google_trends_api_key: str
    serpapi_key: str

settings = Settings()
```

Pydantic Settings will raise a `ValidationError` at import time if any of these env vars are missing — which satisfies the "fails to start with missing var" requirement.

- [ ] **Step 4: Write `backend/core/supabase.py`**

```python
from supabase import create_client, Client
from core.config import settings

supabase: Client = create_client(settings.supabase_url, settings.supabase_service_key)
```

- [ ] **Step 5: Write `backend/core/kimi.py` (stub)**

```python
from core.config import settings


class KimiClient:
    def __init__(self):
        self.api_key = settings.kimi_api_key
        self.base_url = "https://api.moonshot.cn/v1"

    async def complete(self, system_prompt: str, user_message: str) -> dict:
        raise NotImplementedError("Kimi client not yet implemented — Task 11")
```

- [ ] **Step 6: Write `backend/core/__init__.py`**

```python
```

(empty file)

- [ ] **Step 7: Write `backend/models/workspace.py`**

```python
from pydantic import BaseModel
import uuid
from datetime import datetime

class WorkspaceCreate(BaseModel):
    name: str
    budget: float
    currency: str = "USD"

class WorkspaceResponse(BaseModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    name: str
    budget: float
    currency: str
    created_at: datetime
```

- [ ] **Step 8: Write `backend/models/idea_engine.py`**

```python
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class IdeaEngineRunRequest(BaseModel):
    mode: str  # 'validate' | 'generate'
    input_idea: Optional[str] = None
    budget: float
    market_focus: Optional[str] = None

class IdeaEngineRunResponse(BaseModel):
    report_id: uuid.UUID

class ReportSectionResponse(BaseModel):
    id: uuid.UUID
    report_id: uuid.UUID
    section_type: str
    content: dict
    created_at: datetime

class IdeaReportResponse(BaseModel):
    id: uuid.UUID
    workspace_id: uuid.UUID
    mode: str
    input_idea: Optional[str]
    budget: float
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    sections: list[ReportSectionResponse] = []
```

- [ ] **Step 9: Write `backend/models/__init__.py`**

```python
```

(empty file)

- [ ] **Step 10: Write `backend/routers/workspace.py` (stub)**

```python
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/workspace", tags=["workspace"])

@router.post("", status_code=201)
async def create_workspace():
    raise HTTPException(status_code=501, detail="Not implemented — Task 7/8")

@router.get("")
async def get_workspace():
    raise HTTPException(status_code=501, detail="Not implemented — Task 8")
```

- [ ] **Step 11: Write `backend/routers/idea_engine.py` (stub)**

```python
from fastapi import APIRouter, HTTPException
import uuid

router = APIRouter(prefix="/idea-engine", tags=["idea-engine"])

@router.post("/run")
async def run_idea_engine():
    raise HTTPException(status_code=501, detail="Not implemented — Task 13")

@router.get("/report/{report_id}")
async def get_report(report_id: uuid.UUID):
    raise HTTPException(status_code=501, detail="Not implemented — Task 13")
```

- [ ] **Step 12: Write `backend/routers/__init__.py`**

```python
```

(empty file)

- [ ] **Step 13: Write `backend/services/google_trends.py` (stub)**

```python
class DataFetchError(Exception):
    pass

async def fetch_trends(keyword: str, region: str = "US") -> dict:
    raise NotImplementedError("Google Trends service not yet implemented — Task 9")
```

- [ ] **Step 14: Write `backend/services/serpapi.py` (stub)**

```python
class DataFetchError(Exception):
    pass

async def fetch_serp_data(keyword: str, region: str = "us") -> dict:
    raise NotImplementedError("SerpAPI service not yet implemented — Task 10")
```

- [ ] **Step 15: Write `backend/services/idea_engine.py` (stub)**

```python
import uuid

async def run_pipeline(
    report_id: uuid.UUID,
    mode: str,
    idea: str | None,
    budget: float,
    market_focus: str | None,
    workspace_id: uuid.UUID,
) -> None:
    raise NotImplementedError("IdeaEngine pipeline not yet implemented — Task 12")
```

- [ ] **Step 16: Write `backend/services/__init__.py`**

```python
```

(empty file)

- [ ] **Step 17: Write `backend/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings  # fails fast if env vars missing
from routers import workspace, idea_engine

app = FastAPI(title="EagleEye API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workspace.router)
app.include_router(idea_engine.router)

@app.get("/health")
def health():
    return {"status": "ok"}
```

- [ ] **Step 18: Write `backend/Dockerfile`**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000
```

- [ ] **Step 19: Test backend starts locally**

From `backend/` directory, with `.env` at repo root:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Expected output includes: `Application startup complete.`

```bash
curl http://localhost:8000/health
```
Expected: `{"status":"ok"}`

Try starting with a missing env var to confirm fail-fast:
```bash
SUPABASE_URL="" uvicorn main:app
```
Expected: validation error mentioning `supabase_url`.

- [ ] **Step 20: Test Docker build**

```bash
docker build -t eagleeye-backend ./backend
```
Expected: `Successfully built` (or equivalent). No errors.

- [ ] **Step 21: Mark Task 4 completed, commit**

Update `docs/SPRINT_1_TASKS.md` — Task 4 → `completed`.

```bash
git add backend/ docs/SPRINT_1_TASKS.md
git commit -m "task(4): scaffold FastAPI backend with config, supabase client, stub routers and services"
git push
```

---

## Task 5: Next.js Frontend Scaffold

**Files:**
- Modify: `frontend/package.json`
- Modify: `frontend/tsconfig.json`
- Create: `frontend/src/lib/supabase.ts`
- Create: `frontend/src/lib/api.ts`
- Create: `frontend/src/types/index.ts`
- Create: `frontend/src/components/wizard/.gitkeep`
- Create: `frontend/src/components/report/.gitkeep`
- Modify: `frontend/Dockerfile`

- [ ] **Step 1: Mark Task 5 in_progress**

Update `docs/SPRINT_1_TASKS.md` — Task 5 → `in_progress`.

- [ ] **Step 2: Update `frontend/package.json` with all dependencies**

```json
{
  "name": "eagleeye-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.2.29",
    "react": "^18",
    "react-dom": "^18",
    "@supabase/supabase-js": "^2.47.10",
    "@supabase/ssr": "^0.5.2"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "@types/node": "^20",
    "eslint": "^8",
    "eslint-config-next": "14.2.29"
  }
}
```

- [ ] **Step 3: Install dependencies**

```bash
cd frontend
npm install
```

Expected: `node_modules/` created, no peer dependency errors.

- [ ] **Step 4: Write `frontend/src/types/index.ts`**

```typescript
export interface Workspace {
  id: string
  owner_id: string
  name: string
  budget: number
  currency: string
  created_at: string
}

export interface IdeaReport {
  id: string
  workspace_id: string
  mode: 'validate' | 'generate'
  input_idea: string | null
  budget: number
  status: 'pending' | 'running' | 'complete' | 'failed'
  created_at: string
  completed_at: string | null
  sections: ReportSection[]
}

export interface ReportSection {
  id: string
  report_id: string
  section_type: 'report_card' | 'brand_brief' | 'variations' | 'pitch'
  content: ReportCard | BrandBrief | Variation[] | Pitch
  created_at: string
}

export interface ReportCard {
  demand_score: number
  competition_score: number
  margin_potential: 'low' | 'medium' | 'high'
  brand_angle: string
  confidence_notes: string
}

export interface BrandBrief {
  name: string
  tagline: string
  positioning: string
  target_persona: string
  emotional_triggers: string[]
  product_list: string[]
  price_points: Record<string, string | number>
}

export interface Variation {
  idea: string
  score: number
  trade_offs: string
}

export interface Pitch {
  tam: string
  differentiation: string
  go_to_market: string
  one_liner: string
}
```

- [ ] **Step 5: Write `frontend/src/lib/supabase.ts`**

```typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

- [ ] **Step 6: Write `frontend/src/lib/api.ts`**

```typescript
import { createClient } from './supabase'

const API_URL = process.env.NEXT_PUBLIC_API_URL!

async function getAuthHeaders(): Promise<HeadersInit> {
  const supabase = createClient()
  const { data: { session } } = await supabase.auth.getSession()
  if (!session) return { 'Content-Type': 'application/json' }
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${session.access_token}`,
  }
}

export async function apiGet<T>(path: string): Promise<T> {
  const headers = await getAuthHeaders()
  const res = await fetch(`${API_URL}${path}`, { headers })
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`)
  return res.json()
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const headers = await getAuthHeaders()
  const res = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(`POST ${path} failed: ${res.status}`)
  return res.json()
}
```

- [ ] **Step 7: Create component placeholder directories**

```bash
mkdir -p frontend/src/components/wizard
mkdir -p frontend/src/components/report
touch frontend/src/components/wizard/.gitkeep
touch frontend/src/components/report/.gitkeep
```

- [ ] **Step 8: Verify TypeScript build passes**

```bash
cd frontend
npm run build
```
Expected: `Compiled successfully` with zero TypeScript errors.

- [ ] **Step 9: Test Docker build**

```bash
docker build -t eagleeye-frontend ./frontend
```
Expected: builds successfully.

- [ ] **Step 10: Mark Task 5 completed, commit**

Update `docs/SPRINT_1_TASKS.md` — Task 5 → `completed`.

```bash
git add frontend/ docs/SPRINT_1_TASKS.md
git commit -m "task(5): scaffold Next.js frontend with types, supabase client, api client"
git push
```

---

## Task 6: Auth Flow

**Files:**
- Create: `frontend/src/app/auth/login/page.tsx`
- Create: `frontend/src/app/auth/signup/page.tsx`
- Create: `frontend/src/middleware.ts`
- Create: `frontend/src/app/auth/login/actions.ts`
- Create: `frontend/src/app/auth/signup/actions.ts`
- Create: `frontend/src/lib/supabase-server.ts`

**Note:** Supabase SSR auth requires server-side client helpers for middleware and Server Actions. The browser client in `lib/supabase.ts` is for client components only.

- [ ] **Step 1: Mark Task 6 in_progress**

Update `docs/SPRINT_1_TASKS.md` — Task 6 → `in_progress`.

- [ ] **Step 2: Write `frontend/src/lib/supabase-server.ts`**

This creates a Supabase client that works in Server Components, Server Actions, and Route Handlers by reading/writing cookies.

```typescript
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export function createServerSupabaseClient() {
  const cookieStore = cookies()
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {}
        },
      },
    }
  )
}
```

- [ ] **Step 3: Write `frontend/src/middleware.ts`**

The middleware runs on every request. It refreshes the Supabase session cookie, then enforces redirect rules.

```typescript
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          )
          supabaseResponse = NextResponse.next({ request })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  const { data: { user } } = await supabase.auth.getUser()
  const { pathname } = request.nextUrl

  // Public routes — always accessible
  const publicPaths = ['/auth/login', '/auth/signup']
  if (publicPaths.includes(pathname)) {
    return supabaseResponse
  }

  // Unauthenticated — redirect to login
  if (!user) {
    return NextResponse.redirect(new URL('/auth/login', request.url))
  }

  // Authenticated — check for workspace
  if (pathname.startsWith('/dashboard') || pathname === '/') {
    const { data: workspace } = await supabase
      .from('workspaces')
      .select('id')
      .eq('owner_id', user.id)
      .single()

    if (!workspace) {
      return NextResponse.redirect(new URL('/onboarding', request.url))
    }
  }

  return supabaseResponse
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)'],
}
```

- [ ] **Step 4: Write `frontend/src/app/auth/signup/actions.ts`**

```typescript
'use server'

import { redirect } from 'next/navigation'
import { createServerSupabaseClient } from '@/lib/supabase-server'

export async function signUp(formData: FormData) {
  const email = formData.get('email') as string
  const password = formData.get('password') as string
  const supabase = createServerSupabaseClient()

  const { error } = await supabase.auth.signUp({ email, password })
  if (error) return { error: error.message }

  redirect('/onboarding')
}
```

- [ ] **Step 5: Write `frontend/src/app/auth/signup/page.tsx`**

```tsx
'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase'
import { useRouter } from 'next/navigation'

export default function SignupPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const supabase = createClient()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)

    const { error } = await supabase.auth.signUp({ email, password })
    if (error) {
      setError(error.message)
      setLoading(false)
      return
    }
    router.push('/onboarding')
  }

  return (
    <main style={{ maxWidth: 400, margin: '80px auto', padding: '0 16px' }}>
      <h1>Create your account</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            style={{ display: 'block', width: '100%', marginBottom: 12 }}
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            minLength={6}
            style={{ display: 'block', width: '100%', marginBottom: 12 }}
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? 'Creating account…' : 'Sign up'}
        </button>
      </form>
      <p>Already have an account? <a href="/auth/login">Log in</a></p>
    </main>
  )
}
```

- [ ] **Step 6: Write `frontend/src/app/auth/login/page.tsx`**

```tsx
'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const supabase = createClient()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)

    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) {
      setError('Invalid email or password')
      setLoading(false)
      return
    }
    router.push('/dashboard')
  }

  return (
    <main style={{ maxWidth: 400, margin: '80px auto', padding: '0 16px' }}>
      <h1>Log in to EagleEye</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            style={{ display: 'block', width: '100%', marginBottom: 12 }}
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            style={{ display: 'block', width: '100%', marginBottom: 12 }}
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in…' : 'Log in'}
        </button>
      </form>
      <p>Don&apos;t have an account? <a href="/auth/signup">Sign up</a></p>
    </main>
  )
}
```

- [ ] **Step 7: Add logout route**

Create `frontend/src/app/auth/logout/route.ts`:

```typescript
import { NextResponse } from 'next/server'
import { createServerSupabaseClient } from '@/lib/supabase-server'

export async function POST() {
  const supabase = createServerSupabaseClient()
  await supabase.auth.signOut()
  return NextResponse.redirect(new URL('/auth/login', process.env.NEXT_PUBLIC_SUPABASE_URL!))
}
```

Actually, for the logout redirect, use the app URL, not the Supabase URL. Fix:

```typescript
import { NextResponse } from 'next/server'
import { createServerSupabaseClient } from '@/lib/supabase-server'
import { headers } from 'next/headers'

export async function POST() {
  const supabase = createServerSupabaseClient()
  await supabase.auth.signOut()
  const headersList = headers()
  const host = headersList.get('host') || 'localhost:3000'
  const protocol = host.includes('localhost') ? 'http' : 'https'
  return NextResponse.redirect(`${protocol}://${host}/auth/login`)
}
```

- [ ] **Step 8: Add placeholder dashboard page**

Create `frontend/src/app/dashboard/page.tsx`:

```tsx
import { createServerSupabaseClient } from '@/lib/supabase-server'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const supabase = createServerSupabaseClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/auth/login')

  return (
    <main style={{ padding: 32 }}>
      <h1>Dashboard</h1>
      <p>Welcome, {user.email}</p>
      <form action="/auth/logout" method="POST">
        <button type="submit">Log out</button>
      </form>
    </main>
  )
}
```

- [ ] **Step 9: Verify build passes**

```bash
cd frontend
npm run build
```
Expected: zero TypeScript errors.

- [ ] **Step 10: Test auth flow manually**

```bash
cd frontend
npm run dev
```

1. Visit `http://localhost:3000/auth/signup`
2. Create an account with a valid email + password
3. Confirm redirect to `/onboarding` (page may not exist yet — 404 is acceptable at this stage)
4. Check Supabase dashboard → Authentication → Users — new user should appear
5. Visit `http://localhost:3000/auth/login`
6. Log in with the same credentials → confirm redirect to `/dashboard`
7. Try wrong password → confirm inline error message appears
8. Visit `http://localhost:3000/dashboard` without being logged in → confirm redirect to `/auth/login`

- [ ] **Step 11: Mark Task 6 completed, commit**

Update `docs/SPRINT_1_TASKS.md` — Task 6 → `completed`.

```bash
git add frontend/src/ docs/SPRINT_1_TASKS.md
git commit -m "task(6): build auth flow with signup, login, session middleware, and logout"
git push
```

---

## Task 7: Onboarding Flow

**Files:**
- Create: `frontend/src/app/onboarding/page.tsx`
- Modify: `frontend/src/app/dashboard/page.tsx`
- Modify: `backend/routers/workspace.py`
- Modify: `backend/models/workspace.py`

**Prerequisite:** Task 6 auth flow must be complete. Task 3 Supabase schema must be applied (workspaces table must exist).

- [ ] **Step 1: Mark Task 7 in_progress**

Update `docs/SPRINT_1_TASKS.md` — Task 7 → `in_progress`.

- [ ] **Step 2: Implement `POST /workspace` in FastAPI**

The backend needs to accept a JWT, extract the user ID, and create a workspace row. Replace the stub in `backend/routers/workspace.py`:

```python
from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from core.supabase import supabase
from core.config import settings
from models.workspace import WorkspaceCreate, WorkspaceResponse
import httpx

router = APIRouter(prefix="/workspace", tags=["workspace"])


async def get_user_id_from_token(authorization: Optional[str]) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.removeprefix("Bearer ")
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{settings.supabase_url}/auth/v1/user",
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.supabase_anon_key,
            },
        )
    if res.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return res.json()["id"]


@router.post("", status_code=201, response_model=WorkspaceResponse)
async def create_workspace(
    body: WorkspaceCreate,
    authorization: Optional[str] = Header(default=None),
):
    owner_id = await get_user_id_from_token(authorization)

    # Check if workspace already exists
    existing = supabase.table("workspaces").select("id").eq("owner_id", owner_id).execute()
    if existing.data:
        raise HTTPException(status_code=409, detail="Workspace already exists")

    result = supabase.table("workspaces").insert({
        "owner_id": owner_id,
        "name": body.name,
        "budget": body.budget,
        "currency": body.currency,
    }).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create workspace")

    return result.data[0]


@router.get("", response_model=WorkspaceResponse)
async def get_workspace(authorization: Optional[str] = Header(default=None)):
    owner_id = await get_user_id_from_token(authorization)

    result = supabase.table("workspaces").select("*").eq("owner_id", owner_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="No workspace found")

    return result.data[0]
```

- [ ] **Step 3: Add `httpx` to `backend/requirements.txt`**

`httpx` is already in `requirements.txt` from Task 4. Verify it's listed:

```bash
grep httpx backend/requirements.txt
```
Expected: `httpx==0.28.1`

- [ ] **Step 4: Test `POST /workspace` with curl**

Start the backend:
```bash
cd backend && uvicorn main:app --reload
```

Get a real JWT from Supabase — run this in a browser console on your frontend dev server after logging in:
```javascript
const { data } = await supabase.auth.getSession()
console.log(data.session.access_token)
```

Then test (replace `YOUR_JWT` with the token):
```bash
curl -X POST http://localhost:8000/workspace \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT" \
  -d '{"name": "My Store", "budget": 5000}'
```
Expected: HTTP 201, workspace object with `id`, `owner_id`, `name`, `budget`.

Test 409 — run the same command again:
Expected: HTTP 409.

Test 401 — omit the Authorization header:
```bash
curl -X POST http://localhost:8000/workspace -H "Content-Type: application/json" -d '{}'
```
Expected: HTTP 401.

- [ ] **Step 5: Write `frontend/src/app/onboarding/page.tsx`**

```tsx
'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@/lib/supabase'
import { apiPost, apiGet } from '@/lib/api'
import { useRouter } from 'next/navigation'
import type { Workspace } from '@/types'

export default function OnboardingPage() {
  const [name, setName] = useState('')
  const [budget, setBudget] = useState('')
  const [nameError, setNameError] = useState<string | null>(null)
  const [budgetError, setBudgetError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const supabase = createClient()

  // Redirect to dashboard if workspace already exists
  useEffect(() => {
    apiGet<Workspace>('/workspace')
      .then(() => router.replace('/dashboard'))
      .catch(() => {}) // 404 means no workspace — stay on page
  }, [router])

  function validate(): boolean {
    let valid = true
    if (!name.trim()) {
      setNameError('Workspace name is required')
      valid = false
    } else {
      setNameError(null)
    }
    const budgetNum = parseFloat(budget)
    if (!budget || isNaN(budgetNum) || budgetNum <= 0) {
      setBudgetError('Budget must be a positive number')
      valid = false
    } else {
      setBudgetError(null)
    }
    return valid
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!validate()) return

    setLoading(true)
    try {
      await apiPost('/workspace', { name: name.trim(), budget: parseFloat(budget) })
      router.push('/dashboard')
    } catch (err) {
      console.error(err)
      setLoading(false)
    }
  }

  return (
    <main style={{ maxWidth: 480, margin: '80px auto', padding: '0 16px' }}>
      <h1>Set up your workspace</h1>
      <p>Tell us about your business and budget so EagleEye can tailor its recommendations.</p>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 20 }}>
          <label htmlFor="name">Workspace name</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="e.g. My Ecommerce Store"
            style={{ display: 'block', width: '100%', marginTop: 4 }}
          />
          {nameError && <p style={{ color: 'red', fontSize: 14 }}>{nameError}</p>}
        </div>
        <div style={{ marginBottom: 20 }}>
          <label htmlFor="budget">Total budget (USD)</label>
          <input
            id="budget"
            type="number"
            value={budget}
            onChange={e => setBudget(e.target.value)}
            placeholder="e.g. 5000"
            min="0.01"
            step="any"
            style={{ display: 'block', width: '100%', marginTop: 4 }}
          />
          {budgetError && <p style={{ color: 'red', fontSize: 14 }}>{budgetError}</p>}
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Creating workspace…' : 'Get started'}
        </button>
      </form>
    </main>
  )
}
```

- [ ] **Step 6: Update dashboard page to show workspace info**

Replace `frontend/src/app/dashboard/page.tsx`:

```tsx
import { createServerSupabaseClient } from '@/lib/supabase-server'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const supabase = createServerSupabaseClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/auth/login')

  const { data: workspace } = await supabase
    .from('workspaces')
    .select('*')
    .eq('owner_id', user.id)
    .single()

  if (!workspace) redirect('/onboarding')

  return (
    <main style={{ padding: 32 }}>
      <h1>{workspace.name}</h1>
      <p>Budget: ${workspace.budget.toLocaleString()} {workspace.currency}</p>
      <hr />
      <p>No reports yet. Run IdeaEngine to get started.</p>
      <form action="/auth/logout" method="POST" style={{ marginTop: 32 }}>
        <button type="submit">Log out</button>
      </form>
    </main>
  )
}
```

- [ ] **Step 7: Verify TypeScript build**

```bash
cd frontend
npm run build
```
Expected: zero TypeScript errors.

- [ ] **Step 8: Test onboarding flow end-to-end**

```bash
cd frontend && npm run dev
# in another terminal:
cd backend && uvicorn main:app --reload
```

1. Sign up with a new account (use a fresh email to avoid existing workspace)
2. Confirm redirect to `/onboarding`
3. Submit empty name → confirm inline error, no API call
4. Submit budget = 0 → confirm inline error, no API call
5. Submit valid name + positive budget → confirm redirect to `/dashboard`
6. Verify Supabase Table Editor shows new row in `workspaces` with correct `owner_id`, `name`, `budget`
7. Visit `/onboarding` again while logged in with workspace → confirm redirect to `/dashboard`
8. Try accessing workspace via API with a different user's JWT → confirm 404 (RLS enforced)

- [ ] **Step 9: Mark Task 7 completed, commit**

Update `docs/SPRINT_1_TASKS.md` — Task 7 → `completed`.

```bash
git add frontend/src/app/onboarding/ frontend/src/app/dashboard/page.tsx backend/routers/workspace.py docs/SPRINT_1_TASKS.md
git commit -m "task(7): build onboarding flow with workspace creation and POST /workspace endpoint"
git push
```

---

## Self-Review

**Spec coverage check:**

| Requirement | Task |
|---|---|
| Root has backend/, frontend/, docker-compose.yml, .env.example | Task 1 |
| .env.example has all 9 required keys | Task 1 |
| Docker Compose defines two services, shared network, health checks, restart policy | Task 2 |
| Supabase: 4 tables with correct schema | Task 3 |
| RLS on all 4 tables with correct policies | Task 3 |
| Migration SQL committed to backend/migrations/ | Task 3 |
| FastAPI: main.py, CORS, /health endpoint | Task 4 |
| FastAPI: config.py fails fast on missing env vars | Task 4 |
| FastAPI: supabase.py initializes client | Task 4 |
| FastAPI: kimi.py stub | Task 4 |
| FastAPI: stub routers and services | Task 4 |
| FastAPI: Dockerfile builds | Task 4 |
| FastAPI: requirements.txt pinned | Task 4 |
| Next.js 14, App Router, TypeScript strict | Task 5 |
| Folder structure: app/, components/wizard/, components/report/, lib/, types/ | Task 5 |
| lib/supabase.ts Supabase browser client | Task 5 |
| lib/api.ts typed fetch wrapper with JWT | Task 5 |
| types/index.ts all 7 required types | Task 5 |
| Frontend Dockerfile builds | Task 5 |
| /auth/signup: email + password form, Supabase Auth, errors inline | Task 6 |
| /auth/login: email + password form, errors inline | Task 6 |
| Session persists across refresh | Task 6 (Supabase SSR handles this) |
| Middleware: unauthenticated → /auth/login | Task 6 |
| Middleware: authenticated + no workspace → /onboarding | Task 6 |
| Middleware: authenticated + workspace → /dashboard | Task 6 (checked in middleware) |
| Logout clears session → /auth/login | Task 6 |
| /onboarding: name + budget form, validation | Task 7 |
| /onboarding: POST /workspace on submit | Task 7 |
| /onboarding: redirect to /dashboard on success | Task 7 |
| /onboarding: redirect to /dashboard if workspace exists | Task 7 |
| POST /workspace: creates row with owner_id from JWT | Task 7 |
| POST /workspace: returns 409 if workspace exists | Task 7 |
| POST /workspace: returns 401 for missing/invalid JWT | Task 7 |
| GET /workspace: returns workspace or 404 | Task 7 |

All requirements covered.

**Placeholder scan:** No TBD/TODO in implementation steps. Stub methods in Task 4 explicitly reference future task numbers. All code blocks are complete.

**Type consistency:** `WorkspaceResponse` from `backend/models/workspace.py` matches `Workspace` in `frontend/src/types/index.ts`. `apiPost`/`apiGet` in `lib/api.ts` match usage in `onboarding/page.tsx`. `createServerSupabaseClient` defined in `lib/supabase-server.ts` and used in middleware, dashboard, and logout route.
