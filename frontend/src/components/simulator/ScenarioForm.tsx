"use client"

import { useState } from "react"

interface ScenarioFormProps {
  onRun: (adjustments: Record<string, number>) => void
  loading?: boolean
}

export default function ScenarioForm({ onRun, loading }: ScenarioFormProps) {
  const [adjustments, setAdjustments] = useState({
    monthly_inflow_increase: 0,
    gst_filing_improvement: 0,
    emi_reduction: 0,
    revenue_growth_boost: 0,
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onRun(adjustments)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-1.5">
          <label className="text-xs font-medium text-[#94A3B8]">
            Monthly Inflow Increase (₹)
          </label>
          <input
            type="number"
            value={adjustments.monthly_inflow_increase}
            onChange={(e) =>
              setAdjustments({ ...adjustments, monthly_inflow_increase: Number(e.target.value) })
            }
            className="w-full rounded-lg border border-[#1E1E2E] bg-[#0A0A0F] px-3 py-2 text-sm text-[#F8FAFC] outline-none focus:border-[#6366F1]"
          />
        </div>

        <div className="space-y-1.5">
          <label className="text-xs font-medium text-[#94A3B8]">
            GST Filing Months Added
          </label>
          <input
            type="number"
            min={0}
            max={12}
            value={adjustments.gst_filing_improvement}
            onChange={(e) =>
              setAdjustments({ ...adjustments, gst_filing_improvement: Number(e.target.value) })
            }
            className="w-full rounded-lg border border-[#1E1E2E] bg-[#0A0A0F] px-3 py-2 text-sm text-[#F8FAFC] outline-none focus:border-[#6366F1]"
          />
        </div>

        <div className="space-y-1.5">
          <label className="text-xs font-medium text-[#94A3B8]">
            EMI Burden Reduction (%)
          </label>
          <input
            type="number"
            min={0}
            max={100}
            value={adjustments.emi_reduction}
            onChange={(e) =>
              setAdjustments({ ...adjustments, emi_reduction: Number(e.target.value) })
            }
            className="w-full rounded-lg border border-[#1E1E2E] bg-[#0A0A0F] px-3 py-2 text-sm text-[#F8FAFC] outline-none focus:border-[#6366F1]"
          />
        </div>

        <div className="space-y-1.5">
          <label className="text-xs font-medium text-[#94A3B8]">
            Revenue Growth Boost (%)
          </label>
          <input
            type="number"
            value={adjustments.revenue_growth_boost}
            onChange={(e) =>
              setAdjustments({ ...adjustments, revenue_growth_boost: Number(e.target.value) })
            }
            className="w-full rounded-lg border border-[#1E1E2E] bg-[#0A0A0F] px-3 py-2 text-sm text-[#F8FAFC] outline-none focus:border-[#6366F1]"
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full rounded-lg bg-[#6366F1] px-4 py-2.5 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Running Simulation..." : "Run Simulation"}
      </button>
    </form>
  )
}
