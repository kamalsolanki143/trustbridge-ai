"use client"

import { useState } from "react"

interface ManualReviewItem {
  id: string
  business_name: string
  gstin: string
  score: number
  grade: string
  reason: string
  flag_type: string
  status: string
}

interface ManualReviewCardProps {
  item: ManualReviewItem
  onSubmit: (id: string, decision: string, notes: string) => void
}

export default function ManualReviewCard({ item, onSubmit }: ManualReviewCardProps) {
  const [notes, setNotes] = useState("")
  const [submitting, setSubmitting] = useState(false)

  const handleDecision = async (decision: string) => {
    setSubmitting(true)
    await onSubmit(item.id, decision, notes)
    setSubmitting(false)
  }

  return (
    <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-5">
      <div className="flex items-start justify-between">
        <div>
          <h4 className="text-sm font-medium text-[#F8FAFC]">{item.business_name}</h4>
          <p className="text-xs text-[#94A3B8]">GSTIN: {item.gstin}</p>
        </div>
        <span
          className={`rounded-full px-2 py-0.5 text-xs font-medium ${
            item.flag_type === "critical"
              ? "bg-[#EF4444]/10 text-[#EF4444]"
              : "bg-[#F59E0B]/10 text-[#F59E0B]"
          }`}
        >
          {item.flag_type}
        </span>
      </div>

      <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-[#94A3B8]">
        <span>Score: {item.score}</span>
        <span>Grade: {item.grade}</span>
        <span className="col-span-2">Reason: {item.reason}</span>
      </div>

      {item.status === "pending" && (
        <div className="mt-4 space-y-3">
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Review notes..."
            className="w-full rounded-lg border border-[#1E1E2E] bg-[#0A0A0F] px-3 py-2 text-sm text-[#F8FAFC] placeholder-[#4A4A5A] outline-none focus:border-[#6366F1]"
            rows={2}
          />
          <div className="flex gap-2">
            <button
              onClick={() => handleDecision("approve")}
              disabled={submitting}
              className="flex-1 rounded-lg bg-[#10B981] px-4 py-2 text-sm text-white transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              Approve
            </button>
            <button
              onClick={() => handleDecision("reject")}
              disabled={submitting}
              className="flex-1 rounded-lg bg-[#EF4444] px-4 py-2 text-sm text-white transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              Reject
            </button>
            <button
              onClick={() => handleDecision("escalate")}
              disabled={submitting}
              className="flex-1 rounded-lg bg-[#F59E0B] px-4 py-2 text-sm text-white transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              Escalate
            </button>
          </div>
        </div>
      )}

      {item.status !== "pending" && (
        <div className="mt-3 rounded bg-[#1E1E2E] px-3 py-2 text-xs text-[#94A3B8]">
          Status: {item.status}
        </div>
      )}
    </div>
  )
}
