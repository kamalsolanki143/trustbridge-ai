import type { ReadinessAssessment } from "./readiness"

export interface LenderApplication {
  id: string
  msme_id: string
  business_name: string
  gstin: string
  owner_name: string
  city: string
  state: string
  latest_assessment: ReadinessAssessment | null
  submitted_at: string
}

export interface PolicyLayer {
  id: string
  name: string
  min_score: number
  min_confidence: string
  max_emi_burden: number
  min_turnover: number
  loan_types: string[]
  is_active: boolean
}

export interface ManualReviewItem {
  id: string
  msme_id: string
  business_name: string
  gstin: string
  score: number
  grade: string
  reason: string
  flag_type: string
  status: string
  reviewed_by: string | null
  created_at: string
}

export interface LenderDashboardStats {
  total_assessed: number
  pre_qualified_percent: number
  avg_score: number
  starter_loan_count: number
  improve_first_count: number
  manual_review_count: number
}
