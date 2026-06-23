import type { ReadinessAssessment } from "../../types/readiness"

interface RecommendationCardProps {
  assessment: ReadinessAssessment
}

const outcomeConfig: Record<string, { label: string; color: string; bg: string; icon: string }> = {
  "Pre-Qualified": {
    label: "Pre-Qualified",
    color: "text-[#10B981]",
    bg: "bg-[#10B981]/10 border-[#10B981]/30",
    icon: "✅",
  },
  "Starter Loan": {
    label: "Starter Loan Eligible",
    color: "text-[#F59E0B]",
    bg: "bg-[#F59E0B]/10 border-[#F59E0B]/30",
    icon: "🟡",
  },
  "Improve First": {
    label: "Improve First",
    color: "text-[#EF4444]",
    bg: "bg-[#EF4444]/10 border-[#EF4444]/30",
    icon: "❌",
  },
  "Manual Review": {
    label: "Manual Review Required",
    color: "text-[#6366F1]",
    bg: "bg-[#6366F1]/10 border-[#6366F1]/30",
    icon: "🔍",
  },
}

const actionMessages: Record<string, string> = {
  "Pre-Qualified":
    "Proceed with full loan application. The business meets all criteria for streamlined processing.",
  "Starter Loan":
    "Eligible for a starter/product-trial loan. Consider lower ticket size with enhanced monitoring.",
  "Improve First":
    "Does not meet minimum thresholds yet. Follow the Growth Roadmap to strengthen the profile.",
  "Manual Review":
    "Anomaly flags or missing data require human underwriter review before proceeding.",
}

export default function RecommendationCard({ assessment }: RecommendationCardProps) {
  const config = outcomeConfig[assessment.credit_ladder_outcome] || outcomeConfig["Manual Review"]
  const message = actionMessages[assessment.credit_ladder_outcome] || "Review pending."

  return (
    <div className={`rounded-lg border p-5 ${config.bg}`}>
      <div className="flex items-center gap-3">
        <span className="text-2xl">{config.icon}</span>
        <div>
          <p className={`text-lg font-semibold ${config.color}`}>{config.label}</p>
          <p className="mt-1 text-sm text-[#94A3B8]">{message}</p>
        </div>
      </div>
    </div>
  )
}
