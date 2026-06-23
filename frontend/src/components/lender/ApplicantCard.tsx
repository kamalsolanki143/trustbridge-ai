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
  "Manual Review": "text-[#6366F1] bg-[#6366F1]/10",
}

export default function ApplicantCard({ id, businessName, gstin, ownerName, city, grade, score, outcome }: ApplicantCardProps) {
  return (
    <Link
      href={`/lender/applications/${id}`}
      className="block rounded-lg border border-[#1E1E2E] bg-[#12121A] p-4 transition-colors hover:border-[#6366F1]/50"
    >
      <div className="flex items-start justify-between">
        <div>
          <h4 className="text-sm font-medium text-[#F8FAFC]">{businessName}</h4>
          <p className="text-xs text-[#94A3B8]">{ownerName} &middot; {city}</p>
          <p className="text-xs text-[#4A4A5A]">GSTIN: {gstin}</p>
        </div>
        <div className="text-right">
          {grade && (
            <p className={`text-lg font-bold ${gradeColors[grade] || "text-[#94A3B8]"}`}>
              {grade}
            </p>
          )}
          {score !== null && (
            <p className="text-xs text-[#94A3B8]">{score}/100</p>
          )}
        </div>
      </div>
      {outcome && (
        <div className="mt-3">
          <span
            className={`rounded-full px-2 py-0.5 text-xs ${
              outcomeStyles[outcome] || "text-[#94A3B8] bg-[#1E1E2E]"
            }`}
          >
            {outcome}
          </span>
        </div>
      )}
    </Link>
  )
}
