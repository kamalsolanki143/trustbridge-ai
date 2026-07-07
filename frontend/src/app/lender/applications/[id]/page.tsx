"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import Navbar from "../../../../components/common/Navbar"
import Footer from "../../../../components/common/Footer"
import Loader from "../../../../components/common/Loader"
import ReadinessGrade from "../../../../components/readiness/ReadinessGrade"
import ConfidenceBand from "../../../../components/readiness/ConfidenceBand"
import RiskSignals from "../../../../components/readiness/RiskSignals"
import RecommendationCard from "../../../../components/trust_summary/RecommendationCard"

interface ApplicantDetail {
  id: string
  business_name: string
  gstin: string
  owner_name: string
  city: string
  grade: string
  score: number
  confidence: "High" | "Medium" | "Low"
  outcome: string
  risk_signals: Array<{ type: string; code: string; message: string }>
}

const applicantsData: Record<string, ApplicantDetail> = {
  "msme-1": {
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
  },
  "msme-2": {
    id: "msme-2",
    business_name: "Patel Hardware Suppliers",
    gstin: "24AAACP3415G1ZK",
    owner_name: "Amit Patel",
    city: "Ahmedabad",
    grade: "B",
    score: 62,
    confidence: "Medium",
    outcome: "Starter Loan",
    risk_signals: [
      { type: "warning", code: "MODERATE_GST_GAP", message: "GST filed 10/12 months, improvement needed" },
    ],
  },
  "msme-3": {
    id: "msme-3",
    business_name: "Khan Catering Services",
    gstin: "27AAAFK2314H1ZM",
    owner_name: "Imran Khan",
    city: "Mumbai",
    grade: "C+",
    score: 41,
    confidence: "Low",
    outcome: "Improve First",
    risk_signals: [
      { type: "danger", code: "HIGH_LEVERAGE", message: "High monthly debt payments relative to inflows" },
    ],
  },
  "msme-4": {
    id: "msme-4",
    business_name: "Desai Electronics",
    gstin: "27AAACD1234E1ZX",
    owner_name: "Priya Desai",
    city: "Pune",
    grade: "B",
    score: 65,
    confidence: "Medium",
    outcome: "Starter Loan",
    risk_signals: [],
  },
  "msme-5": {
    id: "msme-5",
    business_name: "Singh Logistics",
    gstin: "09AAACS5678L1ZT",
    owner_name: "Gurpreet Singh",
    city: "Delhi",
    grade: "A",
    score: 85,
    confidence: "High",
    outcome: "Pre-Qualified",
    risk_signals: [],
  },
}

export default function ApplicationDetailPage({ params }: { params: { id: string } }) {
  const [loading, setLoading] = useState(true)
  const detail = applicantsData[params.id] || applicantsData["msme-1"]

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 500)
    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
        <Navbar role="lender" />
        <main className="flex flex-1 items-center justify-center">
          <Loader text="Loading applicant profile..." />
        </main>
        <Footer />
      </div>
    )
  }

  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="lender" />
      <main className="flex-1 px-6 py-10">
        <div className="mx-auto max-w-5xl">
          <div className="mb-6">
            <Link
              href="/lender"
              className="inline-flex items-center gap-1 text-sm font-medium text-[#00C9A7] transition-all hover:opacity-80"
            >
              &larr; Back to Dashboard
            </Link>
          </div>

          <div className="mb-8">
            <h1 className="text-3xl font-bold text-white tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
              Applicant Profile
            </h1>
            <p className="mt-1.5 text-sm text-slate-300">
              Detailed credit readiness analysis and signals
            </p>
          </div>

          <div className="grid gap-6 lg:grid-cols-3">
            <div className="flex flex-col items-center justify-center rounded-xl border border-[#1E1E2E] bg-[#12121A] p-8 shadow-sm">
              <ReadinessGrade grade={detail.grade} score={detail.score} size="lg" />
              <div className="mt-5">
                <ConfidenceBand band={detail.confidence} />
              </div>
            </div>

            <div className="lg:col-span-2 space-y-6">
              <div className="rounded-xl border border-[#1E1E2E] bg-[#12121A] p-6 shadow-sm">
                <h3 className="mb-3 text-lg font-semibold text-white" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                  {detail.business_name}
                </h3>
                <div className="grid gap-4 sm:grid-cols-3 text-xs">
                  <div>
                    <p className="text-slate-400 font-mono uppercase tracking-wider">GSTIN</p>
                    <p className="mt-1 text-white font-mono font-medium">{detail.gstin}</p>
                  </div>
                  <div>
                    <p className="text-slate-400 font-mono uppercase tracking-wider">Owner</p>
                    <p className="mt-1 text-white font-medium">{detail.owner_name}</p>
                  </div>
                  <div>
                    <p className="text-slate-400 font-mono uppercase tracking-wider">Location</p>
                    <p className="mt-1 text-white font-medium">{detail.city}</p>
                  </div>
                </div>
              </div>

              <RecommendationCard
                assessment={{
                  msme_id: detail.id,
                  business_name: detail.business_name,
                  readiness_grade: detail.grade,
                  score: detail.score,
                  confidence_band: detail.confidence,
                  coverage_meter: { connected: 5, total: 5, percentage: 100 },
                  sub_scores: [],
                  risk_signals: detail.risk_signals,
                  reason_codes: [],
                  credit_ladder_outcome: detail.outcome,
                  ai_summary: null,
                  created_at: new Date().toISOString(),
                }}
              />

              {detail.risk_signals.length > 0 && (
                <RiskSignals signals={detail.risk_signals} />
              )}
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
