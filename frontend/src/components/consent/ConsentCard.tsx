"use client"

import { useState } from "react"

interface ConsentCardProps {
  onApproveAll: (sources: string[]) => void
  onApproveSingle: (source: string, approved: boolean) => void
}

const dataSources = [
  {
    id: "gst",
    label: "GST Returns",
    description: "Transaction-level GST filings for the past 12 months",
    purpose: "Cash Flow & Compliance Analysis",
    icon: "📋",
  },
  {
    id: "aa",
    label: "Account Aggregator (Bank)",
    description: "Bank statement via RBI AA framework",
    purpose: "Repayment Capacity & EMI Analysis",
    icon: "🏦",
  },
  {
    id: "upi",
    label: "UPI Transactions",
    description: "Digital payment history from UPI apps",
    purpose: "Cash Flow Consistency Check",
    icon: "📱",
  },
  {
    id: "invoice",
    label: "Invoices",
    description: "B2B and B2C invoices issued and received",
    purpose: "Revenue Verification & Trend Analysis",
    icon: "🧾",
  },
  {
    id: "business",
    label: "Business Profile",
    description: "Business details, EPFO, and ownership info",
    purpose: "Identity & Business Verification",
    icon: "🏪",
  },
]

export default function ConsentCard({ onApproveAll, onApproveSingle }: ConsentCardProps) {
  const [approved, setApproved] = useState<Record<string, boolean>>({})

  const toggleSource = (id: string) => {
    const next = { ...approved, [id]: !approved[id] }
    setApproved(next)
    onApproveSingle(id, next[id])
  }

  const handleApproveAll = () => {
    const all = Object.fromEntries(dataSources.map((ds) => [ds.id, true]))
    setApproved(all)
    onApproveAll(dataSources.map((ds) => ds.id))
  }

  const allApproved = dataSources.every((ds) => approved[ds.id])

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-[#F8FAFC]">Data Sources</h2>
        <button
          onClick={handleApproveAll}
          disabled={allApproved}
          className="rounded-lg bg-[#6366F1] px-4 py-2 text-sm text-white transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {allApproved ? "All Approved" : "Approve All"}
        </button>
      </div>

      <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A]">
        {dataSources.map((ds) => (
          <div
            key={ds.id}
            className="flex items-center justify-between border-b border-[#1E1E2E] px-4 py-4 last:border-b-0"
          >
            <div className="flex items-start gap-3">
              <span className="mt-0.5 text-lg">{ds.icon}</span>
              <div>
                <p className="text-sm font-medium text-[#F8FAFC]">{ds.label}</p>
                <p className="text-xs text-[#94A3B8]">{ds.description}</p>
                <p className="mt-1 text-xs text-[#6366F1]">
                  Used for: {ds.purpose}
                </p>
              </div>
            </div>
            <button
              onClick={() => toggleSource(ds.id)}
              className={`relative h-6 w-11 rounded-full transition-colors ${
                approved[ds.id] ? "bg-[#6366F1]" : "bg-[#1E1E2E]"
              }`}
            >
              <span
                className={`absolute left-0.5 top-0.5 h-5 w-5 rounded-full bg-white transition-transform ${
                  approved[ds.id] ? "translate-x-5" : ""
                }`}
              />
            </button>
          </div>
        ))}
      </div>

      <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-4">
        <div className="flex items-center gap-2">
          <span className="text-xs text-[#94A3B8]">🔒</span>
          <span className="text-xs text-[#94A3B8]">
            Data accessed via RBI Account Aggregator framework. Your data is encrypted and used only for
            the stated purpose.
          </span>
        </div>
      </div>
    </div>
  )
}
