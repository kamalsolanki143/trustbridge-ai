"use client"

import { useState } from "react"
import Navbar from "../../../components/common/Navbar"
import Footer from "../../../components/common/Footer"
import ManualReviewCard from "../../../components/lender/ManualReviewCard"

const mockReviews = [
  {
    id: "review-1",
    business_name: "Khan Catering Services",
    gstin: "27AAAFK2314H1ZM",
    score: 41,
    grade: "C+",
    reason: "High EMI burden (51%) and 4 bounced payments. Low GST compliance (6/12 months).",
    flag_type: "critical",
    status: "pending",
  },
  {
    id: "review-2",
    business_name: "Patel Hardware Suppliers",
    gstin: "24AAACP3415G1ZK",
    score: 62,
    grade: "B",
    reason: "Elevated EMI burden (38%) with 2 bounced payments. Moderate compliance concerns.",
    flag_type: "warning",
    status: "pending",
  },
]

export default function ManualReviewPage() {
  const [reviews, setReviews] = useState(mockReviews)

  const handleSubmit = async (id: string, decision: string, notes: string) => {
    setReviews((prev) =>
      prev.map((r) => (r.id === id ? { ...r, status: `${decision}ed` } : r))
    )
  }

  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="lender" />
      <main className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-3xl">
          <h1 className="mb-2 text-2xl font-bold text-[#F8FAFC]">Manual Review</h1>
          <p className="mb-6 text-sm text-[#94A3B8]">
            Review applications flagged by the engine for human decision
          </p>

          <div className="space-y-4">
            {reviews.map((review) => (
              <ManualReviewCard key={review.id} item={review} onSubmit={handleSubmit} />
            ))}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
