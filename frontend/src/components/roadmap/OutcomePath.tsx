interface OutcomePathProps {
  currentGrade: string
  targetGrade: string
}

const gradeOrder = ["D", "C", "C+", "B-", "B", "A-", "A", "A+"]

export default function OutcomePath({ currentGrade, targetGrade }: OutcomePathProps) {
  const currentIdx = gradeOrder.indexOf(currentGrade)
  const targetIdx = gradeOrder.indexOf(targetGrade)

  return (
    <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-5">
      <h3 className="mb-4 text-sm font-medium text-[#F8FAFC]">Grade Journey</h3>
      <div className="flex items-center gap-2">
        {gradeOrder.map((grade, i) => {
          const isReached = i <= currentIdx
          const isTarget = i === targetIdx
          const isInPath = i > currentIdx && i < targetIdx

          return (
            <div key={grade} className="flex items-center">
              <div
                className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-bold transition-colors ${
                  isReached
                    ? "bg-[#10B981] text-white"
                    : isTarget
                      ? "bg-[#6366F1] text-white ring-2 ring-[#6366F1]/50"
                      : isInPath
                        ? "bg-[#1E1E2E] text-[#94A3B8]"
                        : "bg-[#1E1E2E] text-[#4A4A5A]"
                }`}
              >
                {grade}
              </div>
              {i < gradeOrder.length - 1 && (
                <div
                  className={`h-0.5 w-4 ${
                    i < currentIdx ? "bg-[#10B981]" : "bg-[#1E1E2E]"
                  }`}
                />
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
