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
