import type { ReasonCode } from "../../types/readiness"

interface ReasonCodesProps {
  codes: ReasonCode[]
}

const typeStyles: Record<string, string> = {
  positive: "border-[#10B981]/30 bg-[#10B981]/5 text-[#10B981]",
  neutral: "border-[#F59E0B]/30 bg-[#F59E0B]/5 text-[#F59E0B]",
  negative: "border-[#EF4444]/30 bg-[#EF4444]/5 text-[#EF4444]",
}

export default function ReasonCodes({ codes }: ReasonCodesProps) {
  if (codes.length === 0) {
    return (
      <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-4 text-center">
        <p className="text-sm text-[#94A3B8]">No reason codes available.</p>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-medium text-[#F8FAFC]">Reason Codes</h3>
      <div className="flex flex-wrap gap-2">
        {codes.map((code, i) => (
          <div
            key={i}
            className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1 ${
              typeStyles[code.type] || "border-[#1E1E2E] text-[#94A3B8]"
            }`}
          >
            <span className="text-xs">{code.code}</span>
          </div>
        ))}
      </div>
      {codes.length > 0 && (
        <div className="mt-2 space-y-1">
          {codes.map((code, i) => (
            <p key={i} className="text-xs text-[#94A3B8]">
              <span
                className={`font-medium ${
                  code.type === "positive"
                    ? "text-[#10B981]"
                    : code.type === "negative"
                      ? "text-[#EF4444]"
                      : "text-[#F59E0B]"
                }`}
              >
                {code.code}:
              </span>{" "}
              {code.message}
            </p>
          ))}
        </div>
      )}
    </div>
  )
}
