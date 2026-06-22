interface ConfidenceBandProps {
  band: string
}

const bandStyles: Record<string, { color: string; bg: string; label: string }> = {
  High: {
    color: "text-[#10B981]",
    bg: "bg-[#10B981]/10 border-[#10B981]/30",
    label: "High Confidence",
  },
  Medium: {
    color: "text-[#F59E0B]",
    bg: "bg-[#F59E0B]/10 border-[#F59E0B]/30",
    label: "Medium Confidence",
  },
  Low: {
    color: "text-[#EF4444]",
    bg: "bg-[#EF4444]/10 border-[#EF4444]/30",
    label: "Low Confidence",
  },
}

export default function ConfidenceBand({ band }: ConfidenceBandProps) {
  const style = bandStyles[band] || bandStyles.Low

  return (
    <div className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 ${style.bg}`}>
      <span className={`h-2 w-2 rounded-full ${style.color.replace("text-", "bg-")}`} />
      <span className={`text-xs font-medium ${style.color}`}>{style.label}</span>
    </div>
  )
}
