import Link from "next/link"

interface ApplicantCardProps {
  id: string
  businessName: string
  gstin: string
  ownerName: string
  city: string
  grade: string | null
  score: number | null
  outcome: string | null
}

const gradeColors: Record<string, string> = {
  "A+": "text-[#10B981]", "A": "text-[#10B981]", "A-": "text-[#10B981]",
  "B": "text-[#F59E0B]", "B-": "text-[#F59E0B]",
  "C+": "text-[#EF4444]", "C": "text-[#EF4444]", "D": "text-[#EF4444]",
}

const outcomeStyles: Record<string, string> = {
  "Pre-Qualified": "text-[#10B981] bg-[#10B981]/10",
  "Starter Loan": "text-[#F59E0B] bg-[#F59E0B]/10",
  "Improve First": "text-[#EF4444] bg-[#EF4444]/10",
  "Manual Review": "text-[#00C9A7] bg-[#00C9A7]/10",
}

export default function ApplicantCard({ id, businessName, gstin, ownerName, city, grade, score, outcome }: ApplicantCardProps) {
  return (
    <Link
      href={`/lender/applications/${id}`}
      className="block rounded-xl border border-[#1E1E2E] bg-[#12121A] p-5 transition-all duration-300 hover:border-[#00C9A7]/50 hover:scale-[1.01] hover:shadow-md"
    >
      <div className="flex items-start justify-between">
        <div>
          <h4 className="text-sm font-semibold text-white">{businessName}</h4>
          <p className="text-xs text-slate-300">{ownerName} &middot; {city}</p>
          <p className="text-xs text-slate-400 mt-1">GSTIN: {gstin}</p>
        </div>
        <div className="text-right">
          {grade && (
            <p className={`text-lg font-bold ${gradeColors[grade] || "text-slate-300"}`}>
              {grade}
            </p>
          )}
          {score !== null && (
            <p className="text-xs text-slate-400">{score}/100</p>
          )}
        </div>
      </div>
      {outcome && (
        <div className="mt-3">
          <span
            className={`rounded-full px-2.5 py-1 text-xs font-medium ${
              outcomeStyles[outcome] || "text-slate-300 bg-[#1E1E2E]"
            }`}
          >
            {outcome}
          </span>
        </div>
      )}
    </Link>
  )
}
