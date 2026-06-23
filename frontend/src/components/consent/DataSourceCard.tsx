interface DataSourceCardProps {
  sourceType: string
  label: string
  connected: boolean
  icon?: string
}

const sourceIcons: Record<string, string> = {
  gst: "📋",
  aa: "🏦",
  upi: "📱",
  invoice: "🧾",
  business: "🏪",
}

export default function DataSourceCard({ sourceType, label, connected, icon }: DataSourceCardProps) {
  const displayIcon = icon || sourceIcons[sourceType] || "🔗"

  return (
    <div
      className={`rounded-lg border px-4 py-3 ${
        connected
          ? "border-[#10B981]/30 bg-[#10B981]/5"
          : "border-[#1E1E2E] bg-[#12121A]"
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-lg">{displayIcon}</span>
          <div>
            <p className="text-sm font-medium text-[#F8FAFC]">{label}</p>
            <p className="text-xs text-[#94A3B8] capitalize">{sourceType}</p>
          </div>
        </div>
        <span
          className={`h-2 w-2 rounded-full ${
            connected ? "bg-[#10B981]" : "bg-[#EF4444]"
          }`}
        />
      </div>
    </div>
  )
}
