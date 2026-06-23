export interface Milestone {
  title: string
  description: string
  impact: string
  timeline: string
  effort: string
}

export interface GrowthRoadmap {
  current_grade: string
  target_grade: string
  milestones: Milestone[]
  progress_percent: number
}

export interface ScenarioInput {
  gstin: string
  adjustments: Record<string, unknown>
}

export interface ScenarioResult {
  projected_score: number
  projected_grade: string
  projected_outcome: string
  delta_score: number
  improvements: string[]
}
