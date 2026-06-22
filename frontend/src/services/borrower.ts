import { api } from "./api"
import type {
  MSME,
  ConsentRecord,
  ConsentGrantRequest,
} from "../types/borrower"
import type {
  ReadinessAssessment,
  ReadinessAssessRequest,
} from "../types/readiness"

export async function getMSME(gstin: string): Promise<MSME> {
  return api.get<MSME>(`/api/borrower/${gstin}`)
}

export async function grantConsent(data: ConsentGrantRequest): Promise<ConsentRecord> {
  return api.post<ConsentRecord>("/api/consent/grant", data)
}

export async function assessReadiness(data: ReadinessAssessRequest): Promise<ReadinessAssessment> {
  return api.post<ReadinessAssessment>("/api/readiness/assess", data)
}

export async function getReadiness(msmeId: string): Promise<ReadinessAssessment> {
  return api.get<ReadinessAssessment>(`/api/readiness/${msmeId}`)
}

export async function getReadinessHistory(gstin: string): Promise<{ assessments: ReadinessAssessment[] }> {
  return api.get<{ assessments: ReadinessAssessment[] }>(`/api/readiness/history/${gstin}`)
}
