"use client"

import { useState, useEffect } from "react"
import Navbar from "../../../components/common/Navbar"
import Footer from "../../../components/common/Footer"
import Loader from "../../../components/common/Loader"
import ApplicantCard from "../../../components/lender/ApplicantCard"
import ReadinessGrade from "../../../components/readiness/ReadinessGrade"
import ConfidenceBand from "../../../components/readiness/ConfidenceBand"
import RiskSignals from "../../../components/readiness/RiskSignals"
import RecommendationCard from "../../../components/trust_summary/RecommendationCard"

const applicantDetail = {
  id: "msme-1",
  business_name: "Sharma Textile Works",
  gstin: "19AABCS1429B1ZX",
  owner_name: "Rajesh Sharma",
  city: "Kolkata",
  grade: "A-",
  score: 81,
  confidence: "High",
  outcome: "Pre-Qualified",
  risk_signals: [
    { type: "warning", code: "SEASONAL_DEPENDENCY", message: "60% of revenue concentrated in Oct-Dec" },
  ],
}

export default function ApplicationsPage() {
  const [loading, setLoading] = useState(true)
  const [selectedId, setSelectedId] = useState<string | null>(null)

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 500)
    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
        <Navbar role="lender" />
        <main className="flex flex-1 items-center justify-center">
          <Loader text="Loading applications..." />
        </main>
        <Footer />
      </div>
    )
  }

  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="lender" />
      <main className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-5xl">
          <h1 className="mb-6 text-2xl font-bold text-[#F8FAFC]">Applications</h1>

          {!selectedId ? (
            <div className="space-y-3">
              {["Sharma Textile Works", "Patel Hardware Suppliers", "Khan Catering Services"].map(
                (name, i) => (
                  <button
                    key={name}
                    onClick={() => setSelectedId(`msme-${i + 1}`)}
                    className="w-full text-left"
                  >
                    <ApplicantCard
                      id={`msme-${i + 1}`}
                      businessName={name}
                      gstin={["19AABCS1429B1ZX", "24AAACP3415G1ZK", "27AAAFK2314H1ZM"][i]}
                      ownerName={["Rajesh Sharma", "Amit Patel", "Imran Khan"][i]}
                      city={["Kolkata", "Ahmedabad", "Mumbai"][i]}
                      grade={["A-", "B", "C+"][i]}
                      score={[81, 62, 41][i]}
                      outcome={["Pre-Qualified", "Starter Loan", "Improve First"][i]}
                    />
                  </button>
                )
              )}
            </div>
          ) : (
            <div>
              <button
                onClick={() => setSelectedId(null)}
                className="mb-4 text-sm text-[#6366F1] transition-colors hover:text-[#818CF8]"
              >
                &larr; Back to applications
              </button>

              <div className="grid gap-6 lg:grid-cols-3">
                <div className="flex flex-col items-center justify-center rounded-lg border border-[#1E1E2E] bg-[#12121A] p-6">
                  <ReadinessGrade grade={applicantDetail.grade} score={applicantDetail.score} size="lg" />
                  <div className="mt-4">
                    <ConfidenceBand band={applicantDetail.confidence} />
                  </div>
                </div>

                <div className="lg:col-span-2 space-y-4">
                  <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-5">
                    <h3 className="mb-2 text-sm font-medium text-[#F8FAFC]">{applicantDetail.business_name}</h3>
                    <div className="space-y-1 text-xs text-[#94A3B8]">
                      <p>GSTIN: {applicantDetail.gstin}</p>
                      <p>Owner: {applicantDetail.owner_name}</p>
                      <p>Location: {applicantDetail.city}</p>
                    </div>
                  </div>

                  <RecommendationCard
                    assessment={{
                      msme_id: applicantDetail.id,
                      business_name: applicantDetail.business_name,
                      readiness_grade: applicantDetail.grade,
                      score: applicantDetail.score,
                      confidence_band: applicantDetail.confidence,
                      coverage_meter: { connected: 5, total: 5, percentage: 100 },
                      sub_scores: [],
                      risk_signals: applicantDetail.risk_signals,
                      reason_codes: [],
                      credit_ladder_outcome: applicantDetail.outcome,
                      ai_summary: null,
                      created_at: new Date().toISOString(),
                    }}
                  />

                  <RiskSignals signals={applicantDetail.risk_signals} />
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  )
}
