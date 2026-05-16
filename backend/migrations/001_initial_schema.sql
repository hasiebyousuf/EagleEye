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
