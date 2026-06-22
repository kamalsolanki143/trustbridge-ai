"use client"

import { useState } from "react"
import Navbar from "../../../components/common/Navbar"
import Footer from "../../../components/common/Footer"
import ScenarioForm from "../../../components/simulator/ScenarioForm"
import ScenarioResultComponent from "../../../components/simulator/ScenarioResult"
import type { ScenarioResult } from "../../../types/recommendation"

export default function OutcomeSimulatorPage() {
  const [result, setResult] = useState<ScenarioResult | null>(null)
  const [loading, setLoading] = useState(false)

  const handleRun = (adjustments: Record<string, number>) => {
    setLoading(true)
    setTimeout(() => {
      const delta =
        (adjustments.monthly_inflow_increase || 0) * 0.005 +
        (adjustments.gst_filing_improvement || 0) * 1.5 +
        (adjustments.emi_reduction || 0) * 0.3 +
        (adjustments.revenue_growth_boost || 0) * 0.6

      const newScore = Math.min(100, Math.round(62 + delta))
      const newGrade = newScore >= 70 ? "A-" : newScore >= 60 ? "B" : "B-"
      const newOutcome = newScore >= 75 ? "Pre-Qualified" : "Starter Loan"

      setResult({
        projected_score: newScore,
        projected_grade: newGrade,
        projected_outcome: newOutcome,
        delta_score: Math.round(delta),
        improvements: [
          `${adjustments.monthly_inflow_increase > 0 ? `Increase monthly inflow by ₹${adjustments.monthly_inflow_increase}` : "No change in inflow"}`,
          `${adjustments.gst_filing_improvement > 0 ? `File ${adjustments.gst_filing_improvement} more GST months` : "No change in GST filings"}`,
          `${adjustments.emi_reduction > 0 ? `Reduce EMI burden by ${adjustments.emi_reduction}%` : "No change in EMI burden"}`,
          `${adjustments.revenue_growth_boost > 0 ? `Boost revenue growth by ${adjustments.revenue_growth_boost}%` : "No change in revenue growth"}`,
        ],
      })
      setLoading(false)
    }, 1500)
  }

  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="borrower" />
      <main className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-2xl">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-[#F8FAFC]">Outcome Simulator</h1>
            <p className="mt-1 text-sm text-[#94A3B8]">
              Adjust key metrics to see how they affect your credit readiness score
            </p>
          </div>

          <div className="space-y-6">
            <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-6">
              <h2 className="mb-4 text-sm font-medium text-[#F8FAFC]">Adjust Variables</h2>
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
