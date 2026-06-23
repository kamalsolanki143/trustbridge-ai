"use client"

import { useState, useEffect } from "react"
import Navbar from "../../../components/common/Navbar"
import Footer from "../../../components/common/Footer"
import TrustSummaryCard from "../../../components/trust_summary/TrustSummaryCard"
import TrustSummaryPDF from "../../../components/trust_summary/TrustSummaryPDF"
import RecommendationCard from "../../../components/trust_summary/RecommendationCard"
import Loader from "../../../components/common/Loader"
import DataSourceCard from "../../../components/consent/DataSourceCard"
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
  risk_signals: [],
  reason_codes: [],
  credit_ladder_outcome: "Pre-Qualified",
  ai_summary:
    "Sharma Textile Works demonstrates strong credit readiness with robust cash flow, regular GST compliance, and minimal debt burden. The business shows consistent revenue growth and stable operations. Based on the analysis, the applicant is well-positioned for a standard loan product. Recommended loan approach: Working capital term loan up to ₹15L with standard terms.",
  created_at: new Date().toISOString(),
}

const connectedSources = [
  { sourceType: "gst", label: "GST Returns", connected: true },
  { sourceType: "aa", label: "Bank Statements (AA)", connected: true },
  { sourceType: "upi", label: "UPI Transactions", connected: true },
  { sourceType: "invoice", label: "Invoices", connected: true },
  { sourceType: "business", label: "Business Profile", connected: true },
]

export default function TrustSummaryPage() {
  const [assessment] = useState<ReadinessAssessment>(mockAssessment)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 600)
    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
        <Navbar role="borrower" />
        <main className="flex flex-1 items-center justify-center">
          <Loader text="Generating your trust summary..." />
        </main>
        <Footer />
      </div>
    )
  }

  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="borrower" />
      <main className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-3xl">
          <div className="mb-6">
            <span className="rounded bg-[#1E1E2E] px-2 py-1 text-xs text-[#94A3B8]">Step 3 of 4</span>
            <h1 className="mt-2 text-2xl font-bold text-[#F8FAFC]">Trust Summary</h1>
            <p className="text-sm text-[#94A3B8]">{assessment.business_name}</p>
          </div>

          <div className="space-y-6">
            <RecommendationCard assessment={assessment} />

            <TrustSummaryCard assessment={assessment} />

            <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-5">
              <h3 className="mb-3 text-sm font-medium text-[#F8FAFC]">Verified Data Sources</h3>
              <div className="space-y-2">
                {connectedSources.map((ds) => (
                  <DataSourceCard key={ds.sourceType} {...ds} />
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between">
              <TrustSummaryPDF assessment={assessment} />
              <button
                onClick={() => (window.location.href = "/borrower/roadmap")}
                className="rounded-lg bg-[#6366F1] px-6 py-2.5 text-sm font-medium text-white transition-opacity hover:opacity-90"
              >
                View Growth Roadmap
              </button>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
