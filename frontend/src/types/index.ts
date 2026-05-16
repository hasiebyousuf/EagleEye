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
