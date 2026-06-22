"use client"

import { useState } from "react"
import Navbar from "../../../components/common/Navbar"
import Footer from "../../../components/common/Footer"
import ScenarioForm from "../../../components/simulator/ScenarioForm"
import ScenarioResultComponent from "../../../components/simulator/ScenarioResult"
import type { ScenarioResult } from "../../../types/recommendation"

export default function LenderSimulatorPage() {
  const [result, setResult] = useState<ScenarioResult | null>(null)
  const [loading, setLoading] = useState(false)

  const handleRun = (adjustments: Record<string, number>) => {
    setLoading(true)
    setTimeout(() => {
      const baseScore = 55
      const delta =
        (adjustments.monthly_inflow_increase || 0) * 0.003 +
        (adjustments.gst_filing_improvement || 0) * 1.8 +
        (adjustments.emi_reduction || 0) * 0.4 +
        (adjustments.revenue_growth_boost || 0) * 0.5

      const newScore = Math.min(100, Math.round(baseScore + delta))

      let newGrade = "C+"
      if (newScore >= 80) newGrade = "A-"
      else if (newScore >= 70) newGrade = "B"
      else if (newScore >= 60) newGrade = "B-"
      else if (newScore >= 50) newGrade = "C+"

      const newOutcome = newScore >= 75 ? "Pre-Qualified" : newScore >= 50 ? "Starter Loan" : "Improve First"

      setResult({
        projected_score: newScore,
        projected_grade: newGrade,
        projected_outcome: newOutcome,
        delta_score: Math.round(delta),
        improvements: [
          `Increase monthly inflow by ₹${adjustments.monthly_inflow_increase || 0}`,
          `Improve GST filing by ${adjustments.gst_filing_improvement || 0} months`,
          `${adjustments.emi_reduction > 0 ? `Reduce EMI burden by ${adjustments.emi_reduction}%` : "Maintain current EMI burden"}`,
          `${adjustments.revenue_growth_boost > 0 ? `Boost revenue growth by ${adjustments.revenue_growth_boost}%` : "Maintain current growth trajectory"}`,
        ],
      })
      setLoading(false)
    }, 1500)
  }

  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="lender" />
      <main className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-2xl">
          <h1 className="mb-2 text-2xl font-bold text-[#F8FAFC]">Lender Simulator</h1>
          <p className="mb-6 text-sm text-[#94A3B8]">
            Simulate &ldquo;what-if&rdquo; scenarios to see how borrower improvements affect credit outcomes
          </p>

          <div className="space-y-6">
            <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-6">
              <ScenarioForm onRun={handleRun} loading={loading} />
            </div>
            {result && <ScenarioResultComponent result={result} />}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
