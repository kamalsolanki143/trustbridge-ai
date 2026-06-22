import type { ScenarioResult as ScenarioResultType } from "../../types/recommendation"

interface ScenarioResultProps {
  result: ScenarioResultType
}

const outcomeColors: Record<string, string> = {
  "Pre-Qualified": "text-[#10B981]",
  "Starter Loan": "text-[#F59E0B]",
  "Improve First": "text-[#EF4444]",
  "Manual Review": "text-[#6366F1]",
}

export default function ScenarioResult({ result }: ScenarioResultProps) {
  const deltaColor = result.delta_score >= 0 ? "text-[#10B981]" : "text-[#EF4444]"

  return (
    <div className="space-y-4 rounded-lg border border-[#1E1E2E] bg-[#12121A] p-5">
      <h3 className="text-sm font-medium text-[#F8FAFC]">Simulation Result</h3>

      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-lg bg-[#0A0A0F] p-3">
          <p className="text-xs text-[#94A3B8]">Projected Score</p>
          <p className={`text-2xl font-bold ${deltaColor}`}>{result.projected_score}</p>
        </div>
        <div className="rounded-lg bg-[#0A0A0F] p-3">
          <p className="text-xs text-[#94A3B8]">Delta</p>
          <p className={`text-2xl font-bold ${deltaColor}`}>
            {result.delta_score > 0 ? "+" : ""}
            {result.delta_score}
          </p>
        </div>
        <div className="rounded-lg bg-[#0A0A0F] p-3">
          <p className="text-xs text-[#94A3B8]">Projected Grade</p>
          <p className={`text-2xl font-bold ${outcomeColors[result.projected_outcome] || "text-[#F8FAFC]"}`}>
            {result.projected_grade}
          </p>
        </div>
        <div className="rounded-lg bg-[#0A0A0F] p-3">
          <p className="text-xs text-[#94A3B8]">Outcome</p>
          <p className={`text-sm font-bold ${outcomeColors[result.projected_outcome] || "text-[#F8FAFC]"}`}>
            {result.projected_outcome}
          </p>
        </div>
      </div>

      {result.improvements.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-medium text-[#94A3B8]">Improvements Needed</p>
          {result.improvements.map((imp, i) => (
            <div key={i} className="flex items-start gap-2 text-xs text-[#F8FAFC]">
              <span className="text-[#6366F1]">&#9654;</span>
              {imp}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
