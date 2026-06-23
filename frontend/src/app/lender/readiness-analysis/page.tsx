"use client"

import { useState } from "react"
import Navbar from "../../../components/common/Navbar"
import Footer from "../../../components/common/Footer"
import ReadinessGrade from "../../../components/readiness/ReadinessGrade"
import ConfidenceBand from "../../../components/readiness/ConfidenceBand"
import CoverageMeter from "../../../components/readiness/CoverageMeter"
import RiskSignals from "../../../components/readiness/RiskSignals"
import ReasonCodes from "../../../components/readiness/ReasonCodes"

const samples = [
  {
    id: "msme-1",
    name: "Sharma Textile Works",
    grade: "A-",
    score: 81,
    confidence: "High",
    coverage: { connected: 5, total: 5, percentage: 100 },
    subScores: [
      { dim: "Cash Flow", score: 22, max: 25 },
      { dim: "Compliance", score: 23, max: 25 },
      { dim: "Repayment", score: 21, max: 25 },
      { dim: "Growth", score: 15, max: 25 },
    ],
    riskSignals: [{ type: "warning", code: "SEASONAL_DEPENDENCY", message: "60% of revenue concentrated in Oct-Dec" }],
    reasonCodes: [
      { type: "positive", code: "STABLE_INFLOWS", message: "Consistent weekly inflows over 10 months" },
      { type: "positive", code: "STRONG_COMPLIANCE", message: "Regular GST filings" },
    ],
  },
  {
    id: "msme-2",
    name: "Patel Hardware Suppliers",
    grade: "B",
    score: 62,
    confidence: "Medium",
    coverage: { connected: 4, total: 5, percentage: 80 },
    subScores: [
      { dim: "Cash Flow", score: 16, max: 25 },
      { dim: "Compliance", score: 14, max: 25 },
      { dim: "Repayment", score: 18, max: 25 },
      { dim: "Growth", score: 14, max: 25 },
    ],
    riskSignals: [
      { type: "warning", code: "ELEVATED_EMI", message: "EMI burden at 38% of inflows" },
      { type: "warning", code: "BOUNCE_HISTORY", message: "2 bounced payment(s) on record" },
    ],
    reasonCodes: [
      { type: "positive", code: "STABLE_GROWTH", message: "Business is stable with modest growth" },
      { type: "negative", code: "MODERATE_COMPLIANCE", message: "GST filing gaps detected" },
    ],
  },
  {
    id: "msme-3",
    name: "Khan Catering Services",
    grade: "C+",
    score: 41,
    confidence: "Low",
    coverage: { connected: 3, total: 5, percentage: 60 },
    subScores: [
      { dim: "Cash Flow", score: 10, max: 25 },
      { dim: "Compliance", score: 8, max: 25 },
      { dim: "Repayment", score: 12, max: 25 },
      { dim: "Growth", score: 11, max: 25 },
    ],
    riskSignals: [
      { type: "critical", code: "HIGH_EMI_BURDEN", message: "EMI burden at 51% of inflows" },
      { type: "critical", code: "MULTIPLE_BOUNCES", message: "4 bounced payments detected" },
      { type: "critical", code: "LOW_GST_COMPLIANCE", message: "GST filed only 6/12 months" },
    ],
    reasonCodes: [
      { type: "negative", code: "WEAK_CASH_FLOW", message: "Irregular or low cash flow" },
      { type: "negative", code: "WEAK_REPAYMENT", message: "High EMI burden or bounced payments" },
    ],
  },
]

export default function ReadinessAnalysisPage() {
  const [selected, setSelected] = useState(samples[0])

  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="lender" />
      <main className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-6xl">
          <h1 className="mb-6 text-2xl font-bold text-[#F8FAFC]">Readiness Analysis</h1>

          <div className="mb-6 flex gap-2">
            {samples.map((s) => (
              <button
                key={s.id}
                onClick={() => setSelected(s)}
                className={`rounded-lg px-4 py-2 text-sm transition-colors ${
                  selected.id === s.id
                    ? "bg-[#6366F1] text-white"
                    : "bg-[#1E1E2E] text-[#94A3B8] hover:text-[#F8FAFC]"
                }`}
              >
                {s.name}
              </button>
            ))}
          </div>

          <div className="grid gap-6 lg:grid-cols-4">
            <div className="flex flex-col items-center justify-center rounded-lg border border-[#1E1E2E] bg-[#12121A] p-6">
              <ReadinessGrade grade={selected.grade} score={selected.score} size="lg" />
              <div className="mt-4">
                <ConfidenceBand band={selected.confidence} />
              </div>
            </div>

            <div className="flex flex-col items-center justify-center rounded-lg border border-[#1E1E2E] bg-[#12121A] p-6">
              <CoverageMeter
                connected={selected.coverage.connected}
                total={selected.coverage.total}
                percentage={selected.coverage.percentage}
              />
            </div>

            <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-6 lg:col-span-2">
              <h3 className="mb-3 text-sm font-medium text-[#F8FAFC]">Sub-Scores</h3>
              <div className="space-y-3">
                {selected.subScores.map((s) => (
                  <div key={s.dim}>
                    <div className="flex justify-between text-xs">
                      <span className="text-[#94A3B8]">{s.dim}</span>
                      <span className="text-[#F8FAFC]">{s.score}/{s.max}</span>
                    </div>
                    <div className="mt-1 h-1.5 w-full overflow-hidden rounded-full bg-[#1E1E2E]">
                      <div
                        className="h-full rounded-full bg-[#6366F1] transition-all"
                        style={{ width: `${(s.score / s.max) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="mt-6 grid gap-6 lg:grid-cols-2">
            <RiskSignals signals={selected.riskSignals} />
            <ReasonCodes codes={selected.reasonCodes} />
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
