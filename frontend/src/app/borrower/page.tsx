"use client"

import { useState } from "react"
import Navbar from "../../components/common/Navbar"
import Footer from "../../components/common/Footer"
import ApplicantCard from "../../components/lender/ApplicantCard"

const sampleMSMEs = [
  {
    id: "msme-1",
    business_name: "Sharma Textile Works",
    gstin: "19AABCS1429B1ZX",
    owner_name: "Rajesh Sharma",
    city: "Kolkata",
    grade: "A-",
    score: 81,
    outcome: "Pre-Qualified",
  },
  {
    id: "msme-2",
    business_name: "Patel Hardware Suppliers",
    gstin: "24AAACP3415G1ZK",
    owner_name: "Amit Patel",
    city: "Ahmedabad",
    grade: "B",
    score: 62,
    outcome: "Starter Loan",
  },
  {
    id: "msme-3",
    business_name: "Khan Catering Services",
    gstin: "27AAAFK2314H1ZM",
    owner_name: "Imran Khan",
    city: "Mumbai",
    grade: "C+",
    score: 41,
    outcome: "Improve First",
  },
]

export default function BorrowerDashboard() {
  const [gstinInput, setGstinInput] = useState("")

  const handleStart = () => {
    const msme = sampleMSMEs.find((m) => m.gstin === gstinInput)
    if (msme) {
      window.location.href = `/borrower/consent?gstin=${msme.gstin}`
    }
  }

  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="borrower" />
      <main className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-3xl">
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-[#F8FAFC]">Borrower Dashboard</h1>
            <p className="mt-1 text-sm text-[#94A3B8]">
              Check your credit readiness, give consent, and see your growth roadmap
            </p>
          </div>

          <div className="mb-8 rounded-lg border border-[#1E1E2E] bg-[#12121A] p-6">
            <h2 className="text-sm font-medium text-[#F8FAFC]">Start Your Assessment</h2>
            <p className="mt-1 text-xs text-[#94A3B8]">
              Enter your GSTIN to begin the credit readiness process
            </p>
            <div className="mt-4 flex gap-3">
              <input
                value={gstinInput}
                onChange={(e) => setGstinInput(e.target.value)}
                placeholder="Enter GSTIN (e.g., 19AABCS1429B1ZX)"
                className="flex-1 rounded-lg border border-[#1E1E2E] bg-[#0A0A0F] px-4 py-2.5 text-sm text-[#F8FAFC] placeholder-[#4A4A5A] outline-none focus:border-[#6366F1]"
              />
              <button
                onClick={handleStart}
                disabled={!gstinInput}
                className="rounded-lg bg-[#6366F1] px-6 py-2.5 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
              >
                Continue
              </button>
            </div>
          </div>

          <div>
            <h2 className="mb-3 text-sm font-medium text-[#F8FAFC]">Sample Profiles</h2>
            <div className="space-y-3">
              {sampleMSMEs.map((msme) => (
                <ApplicantCard
                  key={msme.id}
                  id={msme.id}
                  businessName={msme.business_name}
                  gstin={msme.gstin}
                  ownerName={msme.owner_name}
                  city={msme.city}
                  grade={msme.grade}
                  score={msme.score}
                  outcome={msme.outcome}
                />
              ))}
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
