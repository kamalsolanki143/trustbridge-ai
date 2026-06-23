import { api } from "./api"
import type { LenderApplication, LenderDashboardStats, ManualReviewItem } from "../types/lender"
import type { ReadinessAssessment } from "../types/readiness"

export async function getLenderDashboard(): Promise<LenderDashboardStats> {
  return api.get<LenderDashboardStats>("/api/lender/stats")
}

export async function getApplications(): Promise<LenderApplication[]> {
  return api.get<LenderApplication[]>("/api/lender/applications")
}

export async function getApplicationDetail(msmeId: string): Promise<ReadinessAssessment> {
  return api.get<ReadinessAssessment>(`/api/lender/applications/${msmeId}`)
}

export async function getManualReviews(): Promise<ManualReviewItem[]> {
  return api.get<ManualReviewItem[]>("/api/lender/manual-reviews")
}

export async function submitReview(
  reviewId: string,
  decision: string,
  notes: string
): Promise<void> {
  return api.post<void>(`/api/lender/manual-reviews/${reviewId}`, {
    decision,
    notes,
  })
}
