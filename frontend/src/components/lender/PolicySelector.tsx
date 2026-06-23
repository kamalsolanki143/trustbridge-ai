"use client"

import { useState } from "react"

interface PolicyLayer {
  id: string
  name: string
  min_score: number
  min_confidence: string
  max_emi_burden: number
  min_turnover: number
  loan_types: string[]
  is_active: boolean
}

interface PolicySelectorProps {
  policies: PolicyLayer[]
  onSelect: (policy: PolicyLayer) => void
}

export default function PolicySelector({ policies, onSelect }: PolicySelectorProps) {
  const [selected, setSelected] = useState<string | null>(null)

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-medium text-[#F8FAFC]">Policy Layers</h3>
      {policies.map((policy) => (
        <button
          key={policy.id}
          onClick={() => {
            setSelected(policy.id)
            onSelect(policy)
          }}
          className={`w-full rounded-lg border p-4 text-left transition-colors ${
            selected === policy.id
              ? "border-[#6366F1] bg-[#6366F1]/5"
              : "border-[#1E1E2E] bg-[#12121A] hover:border-[#6366F1]/50"
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-[#F8FAFC]">{policy.name}</span>
            {policy.is_active && (
              <span className="rounded bg-[#10B981]/10 px-2 py-0.5 text-xs text-[#10B981]">
                Active
              </span>
            )}
          </div>
          <div className="mt-2 grid grid-cols-2 gap-2 text-xs text-[#94A3B8]">
            <span>Min Score: {policy.min_score}</span>
            <span>Min Confidence: {policy.min_confidence}</span>
            <span>Max EMI: {policy.max_emi_burden}%</span>
            <span>Min Turnover: ₹{policy.min_turnover.toLocaleString()}</span>
          </div>
          <div className="mt-2 flex flex-wrap gap-1">
            {policy.loan_types.map((loan) => (
              <span
                key={loan}
                className="rounded bg-[#1E1E2E] px-2 py-0.5 text-xs text-[#94A3B8]"
              >
                {loan}
              </span>
            ))}
          </div>
        </button>
      ))}
    </div>
  )
}
