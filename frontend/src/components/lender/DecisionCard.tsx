interface DecisionCardProps {
  score: number
  grade: string
  outcome: string
  confidence: string
}

const outcomeConfig: Record<string, { label: string; color: string; bg: string }> = {
  "Pre-Qualified": { label: "Approve", color: "text-[#10B981]", bg: "bg-[#10B981]/10 border-[#10B981]/30" },
  "Starter Loan": { label: "Conditional", color: "text-[#F59E0B]", bg: "bg-[#F59E0B]/10 border-[#F59E0B]/30" },
  "Improve First": { label: "Decline", color: "text-[#EF4444]", bg: "bg-[#EF4444]/10 border-[#EF4444]/30" },
  "Manual Review": { label: "Review", color: "text-[#6366F1]", bg: "bg-[#6366F1]/10 border-[#6366F1]/30" },
}

export default function DecisionCard({ score, grade, outcome, confidence }: DecisionCardProps) {
  const config = outcomeConfig[outcome] || outcomeConfig["Manual Review"]

  return (
    <div className={`rounded-lg border p-5 ${config.bg}`}>
      <h3 className="mb-3 text-sm font-medium text-[#F8FAFC]">Decision</h3>
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-[#94A3B8]">Grade</span>
          <span className={`font-bold ${config.color}`}>{grade}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-[#94A3B8]">Score</span>
          <span className="text-[#F8FAFC]">{score}/100</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-[#94A3B8]">Confidence</span>
          <span className="text-[#F8FAFC]">{confidence}</span>
        </div>
      </div>
      <div className={`mt-4 rounded-lg border px-4 py-3 text-center text-sm font-medium ${config.bg} ${config.color}`}>
        {config.label} &mdash; {outcome}
      </div>
    </div>
  )
}
