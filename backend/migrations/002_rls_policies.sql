-- Enable RLS on all tables
alter table workspaces      enable row level security;
alter table idea_reports    enable row level security;
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
