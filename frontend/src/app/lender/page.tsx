"use client"

import { useState, useEffect } from "react"
import Navbar from "../../components/common/Navbar"
import Footer from "../../components/common/Footer"
import Loader from "../../components/common/Loader"
import ApplicantCard from "../../components/lender/ApplicantCard"

interface Applicant {
  id: string
  business_name: string
  gstin: string
  owner_name: string
  city: string
  grade: string
  score: number
  outcome: string
  date: string
}

const allApplicants: Applicant[] = [
  { id: "msme-1", business_name: "Sharma Textile Works", gstin: "19AABCS1429B1ZX", owner_name: "Rajesh Sharma", city: "Kolkata", grade: "A-", score: 81, outcome: "Pre-Qualified", date: "2026-06-20" },
  { id: "msme-2", business_name: "Patel Hardware Suppliers", gstin: "24AAACP3415G1ZK", owner_name: "Amit Patel", city: "Ahmedabad", grade: "B", score: 62, outcome: "Starter Loan", date: "2026-06-19" },
  { id: "msme-3", business_name: "Khan Catering Services", gstin: "27AAAFK2314H1ZM", owner_name: "Imran Khan", city: "Mumbai", grade: "C+", score: 41, outcome: "Improve First", date: "2026-06-18" },
  { id: "msme-4", business_name: "Desai Electronics", gstin: "27AAACD1234E1ZX", owner_name: "Priya Desai", city: "Pune", grade: "B", score: 65, outcome: "Starter Loan", date: "2026-06-17" },
  { id: "msme-5", business_name: "Singh Logistics", gstin: "09AAACS5678L1ZT", owner_name: "Gurpreet Singh", city: "Delhi", grade: "A", score: 85, outcome: "Pre-Qualified", date: "2026-06-16" },
]

const outcomeFilterOptions = ["All", "Pre-Qualified", "Starter Loan", "Improve First", "Manual Review"]

export default function LenderDashboard() {
  const [loading, setLoading] = useState(true)
  const [filterOutcome, setFilterOutcome] = useState("All")
  const [search, setSearch] = useState("")

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 600)
    return () => clearTimeout(timer)
  }, [])

  const filtered = allApplicants.filter((a) => {
    const matchesOutcome = filterOutcome === "All" || a.outcome === filterOutcome
    const matchesSearch =
      !search ||
      a.business_name.toLowerCase().includes(search.toLowerCase()) ||
      a.gstin.toLowerCase().includes(search.toLowerCase())
    return matchesOutcome && matchesSearch
  })

  const stats = {
    total: allApplicants.length,
    preQualified: allApplicants.filter((a) => a.outcome === "Pre-Qualified").length,
    avgScore: Math.round(allApplicants.reduce((s, a) => s + a.score, 0) / allApplicants.length),
    starterLoan: allApplicants.filter((a) => a.outcome === "Starter Loan").length,
    improveFirst: allApplicants.filter((a) => a.outcome === "Improve First").length,
  }

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
        <Navbar role="lender" />
        <main className="flex flex-1 items-center justify-center">
          <Loader text="Loading dashboard..." />
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
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-[#F8FAFC]">Lender Dashboard</h1>
            <p className="mt-1 text-sm text-[#94A3B8]">IDBI Bank &mdash; MSME Credit Assessment Portal</p>
          </div>

          <div className="mb-6 grid gap-4 sm:grid-cols-4">
            {[
              { label: "Total Assessed", value: stats.total },
              { label: "Pre-Qualified", value: `${Math.round((stats.preQualified / stats.total) * 100)}%` },
              { label: "Avg Score", value: stats.avgScore },
              { label: "Starter Loans", value: stats.starterLoan },
            ].map((stat) => (
              <div key={stat.label} className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-4">
                <p className="text-xs text-[#94A3B8]">{stat.label}</p>
                <p className="mt-1 text-2xl font-bold text-[#F8FAFC]">{stat.value}</p>
              </div>
            ))}
          </div>

          <div className="mb-4 flex items-center gap-4">
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by business name or GSTIN..."
              className="flex-1 rounded-lg border border-[#1E1E2E] bg-[#12121A] px-4 py-2 text-sm text-[#F8FAFC] placeholder-[#4A4A5A] outline-none focus:border-[#6366F1]"
            />
            <div className="flex gap-2">
              {outcomeFilterOptions.map((opt) => (
                <button
                  key={opt}
                  onClick={() => setFilterOutcome(opt)}
                  className={`rounded-lg px-3 py-2 text-xs transition-colors ${
                    filterOutcome === opt
                      ? "bg-[#6366F1] text-white"
                      : "bg-[#1E1E2E] text-[#94A3B8] hover:text-[#F8FAFC]"
                  }`}
                >
                  {opt}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-3">
            {filtered.map((applicant) => (
              <ApplicantCard
                key={applicant.id}
                id={applicant.id}
                businessName={applicant.business_name}
                gstin={applicant.gstin}
                ownerName={applicant.owner_name}
                city={applicant.city}
                grade={applicant.grade}
                score={applicant.score}
                outcome={applicant.outcome}
              />
            ))}
            {filtered.length === 0 && (
              <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-8 text-center">
                <p className="text-sm text-[#94A3B8]">No applicants match your filters.</p>
              </div>
            )}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
