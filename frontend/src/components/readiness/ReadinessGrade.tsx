interface ReadinessGradeProps {
  grade: string
  score: number
  size?: "sm" | "md" | "lg"
}

const gradeColors: Record<string, string> = {
  "A+": "text-[#10B981] border-[#10B981]",
  "A": "text-[#10B981] border-[#10B981]",
  "A-": "text-[#10B981] border-[#10B981]",
  "B": "text-[#F59E0B] border-[#F59E0B]",
  "B-": "text-[#F59E0B] border-[#F59E0B]",
  "C+": "text-[#EF4444] border-[#EF4444]",
  "C": "text-[#EF4444] border-[#EF4444]",
  "D": "text-[#EF4444] border-[#EF4444]",
}

export default function ReadinessGrade({ grade, score, size = "md" }: ReadinessGradeProps) {
  const color = gradeColors[grade] || "text-[#94A3B8] border-[#94A3B8]"
  const dimensions = size === "lg" ? "h-28 w-28 text-4xl" : size === "sm" ? "h-16 w-16 text-xl" : "h-24 w-24 text-3xl"

  return (
    <div className="flex flex-col items-center gap-2">
      <div
        className={`flex items-center justify-center rounded-full border-2 ${color} ${dimensions} bg-[#12121A]`}
      >
        <span className="font-bold">{grade}</span>
      </div>
      <span className={`text-sm font-medium ${color}`}>{score}/100</span>
    </div>
  )
}
