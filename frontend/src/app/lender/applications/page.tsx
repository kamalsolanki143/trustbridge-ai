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
      <main className="flex-1 px-6 py-10">
        <div className="mx-auto max-w-3xl">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-white tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
              Applications
            </h1>
            <p className="mt-1.5 text-sm text-slate-300">
              Browse submitted MSME credit assessment applications
            </p>
          </div>

          <div className="space-y-4">
            {[
              { name: "Sharma Textile Works", gstin: "19AABCS1429B1ZX", owner: "Rajesh Sharma", city: "Kolkata", grade: "A-", score: 81, outcome: "Pre-Qualified" },
              { name: "Patel Hardware Suppliers", gstin: "24AAACP3415G1ZK", owner: "Amit Patel", city: "Ahmedabad", grade: "B", score: 62, outcome: "Starter Loan" },
              { name: "Khan Catering Services", gstin: "27AAAFK2314H1ZM", owner: "Imran Khan", city: "Mumbai", grade: "C+", score: 41, outcome: "Improve First" },
              { name: "Desai Electronics", gstin: "27AAACD1234E1ZX", owner: "Priya Desai", city: "Pune", grade: "B", score: 65, outcome: "Starter Loan" },
              { name: "Singh Logistics", gstin: "09AAACS5678L1ZT", owner: "Gurpreet Singh", city: "Delhi", grade: "A", score: 85, outcome: "Pre-Qualified" }
            ].map((app, i) => (
              <ApplicantCard
                key={app.gstin}
                id={`msme-${i + 1}`}
                businessName={app.name}
                gstin={app.gstin}
                ownerName={app.owner}
                city={app.city}
                grade={app.grade}
                score={app.score}
                outcome={app.outcome}
              />
            ))}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
