"use client"

import type { ReadinessAssessment } from "../../types/readiness"

interface TrustSummaryPDFProps {
  assessment: ReadinessAssessment
}

export default function TrustSummaryPDF({ assessment }: TrustSummaryPDFProps) {
  const handleExport = () => {
    const content = `
TRUST BRIDGE AI — CREDIT READINESS SUMMARY
============================================
Business: ${assessment.business_name}
Grade: ${assessment.readiness_grade} (${assessment.score}/100)
Confidence: ${assessment.confidence_band}
Outcome: ${assessment.credit_ladder_outcome}
Coverage: ${assessment.coverage_meter.percentage}%

SUB-SCORES:
${assessment.sub_scores.map((s) => `  ${s.dimension}: ${s.score}/${s.max_score}`).join("\n")}

AI SUMMARY:
${assessment.ai_summary || "N/A"}

Generated: ${new Date(assessment.created_at).toLocaleString()}
    `.trim()

    const blob = new Blob([content], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `trust-summary-${assessment.msme_id.slice(0, 8)}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <button
      onClick={handleExport}
      className="flex items-center gap-2 rounded-lg border border-[#1E1E2E] bg-[#12121A] px-4 py-2 text-sm text-[#94A3B8] transition-colors hover:border-[#6366F1] hover:text-[#6366F1]"
    >
      <span>📄</span>
      Export Summary
    </button>
  )
}
