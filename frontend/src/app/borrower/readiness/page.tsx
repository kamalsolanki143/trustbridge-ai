"use client"

import { useState, useCallback, useEffect } from "react"
import Navbar from "../../../components/common/Navbar"
import Footer from "../../../components/common/Footer"
import ReadinessGrade from "../../../components/readiness/ReadinessGrade"
import ConfidenceBand from "../../../components/readiness/ConfidenceBand"
import CoverageMeter from "../../../components/readiness/CoverageMeter"
import RiskSignals from "../../../components/readiness/RiskSignals"
import ReasonCodes from "../../../components/readiness/ReasonCodes"
import Loader from "../../../components/common/Loader"
import type { ReadinessAssessment } from "../../../types/readiness"

const mockAssessment: ReadinessAssessment = {
  msme_id: "msme-1",
  business_name: "Sharma Textile Works",
  readiness_grade: "A-",
  score: 81,
  confidence_band: "High",
  coverage_meter: { connected: 5, total: 5, percentage: 100 },
  sub_scores: [
    { dimension: "cash_flow", score: 22, max_score: 25, weight_percent: 35 },
    { dimension: "compliance", score: 23, max_score: 25, weight_percent: 20 },
    { dimension: "repayment", score: 21, max_score: 25, weight_percent: 30 },
    { dimension: "growth", score: 15, max_score: 25, weight_percent: 15 },
  ],
  risk_signals: [
    { type: "warning", code: "SEASONAL_DEPENDENCY", message: "60% of revenue concentrated in Oct-Dec" },
    { type: "warning", code: "MODERATE_GST_GAP", message: "GST filed 11/12 months, improvement needed" },
  ],
  reason_codes: [
    { type: "positive", code: "STABLE_INFLOWS", message: "Consistent weekly inflows over 10 months" },
    { type: "positive", code: "LOW_DEBT_BURDEN", message: "Existing debt obligations are well within safe limits" },
    { type: "positive", code: "STRONG_COMPLIANCE", message: "Regular GST filings and EPFO contributions demonstrate compliance" },
  ],
  credit_ladder_outcome: "Pre-Qualified",
  ai_summary: null,
  created_at: new Date().toISOString(),
}

const subScoreLabels: Record<string, string> = {
  cash_flow: "Cash Flow",
  compliance: "Compliance",
  repayment: "Repayment",
  growth: "Growth",
}

export default function ReadinessPage() {
  const [assessment] = useState<ReadinessAssessment>(mockAssessment)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 800)
    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
        <Navbar role="borrower" />
        <main className="flex flex-1 items-center justify-center">
          <Loader text="Computing your readiness grade..." />
        </main>
        <Footer />
      </div>
    )
  }

  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="borrower" />
      <main className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-4xl">
          <div className="mb-6">
            <span className="rounded bg-[#1E1E2E] px-2 py-1 text-xs text-[#94A3B8]">Step 2 of 4</span>
            <h1 className="mt-2 text-2xl font-bold text-[#F8FAFC]">Credit Readiness</h1>
            <p className="text-sm text-[#94A3B8]">{assessment.business_name}</p>
          </div>

          <div className="grid gap-6 lg:grid-cols-3">
            <div className="flex flex-col items-center justify-center rounded-lg border border-[#1E1E2E] bg-[#12121A] p-6">
              <ReadinessGrade grade={assessment.readiness_grade} score={assessment.score} size="lg" />
              <div className="mt-4">
                <ConfidenceBand band={assessment.confidence_band} />
              </div>
            </div>

            <div className="flex flex-col items-center justify-center rounded-lg border border-[#1E1E2E] bg-[#12121A] p-6">
              <CoverageMeter
                connected={assessment.coverage_meter.connected}
                total={assessment.coverage_meter.total}
                percentage={assessment.coverage_meter.percentage}
              />
            </div>

            <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-6">
              <h3 className="mb-3 text-sm font-medium text-[#F8FAFC]">Sub-Scores</h3>
              <div className="space-y-3">
                {assessment.sub_scores.map((s) => (
                  <div key={s.dimension}>
                    <div className="flex justify-between text-xs">
                      <span className="text-[#94A3B8]">{subScoreLabels[s.dimension] || s.dimension}</span>
                      <span className="text-[#F8FAFC]">
                        {s.score}/{s.max_score}
                      </span>
                    </div>
                    <div className="mt-1 h-1.5 w-full overflow-hidden rounded-full bg-[#1E1E2E]">
                      <div
                        className="h-full rounded-full bg-[#6366F1] transition-all duration-700"
                        style={{ width: `${(s.score / s.max_score) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="mt-6 grid gap-6 lg:grid-cols-2">
            <RiskSignals signals={assessment.risk_signals} />
            <ReasonCodes codes={assessment.reason_codes} />
          </div>

          <div className="mt-6 flex justify-center">
            <button
              onClick={() => (window.location.href = "/borrower/trust-summary")}
              className="rounded-lg bg-[#6366F1] px-8 py-3 text-sm font-medium text-white transition-opacity hover:opacity-90"
            >
              View Trust Summary
            </button>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
