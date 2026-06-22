export interface RiskSignal {
  type: string
  code: string
  message: string
}

export interface ReasonCode {
  type: string
  code: string
  message: string
}

export interface SubScore {
  dimension: string
  score: number
  max_score: number
  weight_percent: number
}

export interface CoverageMeter {
  connected: number
  total: number
  percentage: number
}

export interface ReadinessAssessment {
  msme_id: string
  business_name: string
  readiness_grade: string
  score: number
  confidence_band: string
  coverage_meter: CoverageMeter
  sub_scores: SubScore[]
  risk_signals: RiskSignal[]
  reason_codes: ReasonCode[]
  credit_ladder_outcome: string
  ai_summary: string | null
  created_at: string
}

export interface ReadinessAssessRequest {
  gstin: string
  consent_token: string
  data_sources: string[]
}
