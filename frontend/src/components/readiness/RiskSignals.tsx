"use client"

import { useState } from "react"
import type { RiskSignal } from "../../types/readiness"

interface RiskSignalsProps {
  signals: RiskSignal[]
}

export default function RiskSignals({ signals }: RiskSignalsProps) {
  const [expanded, setExpanded] = useState(false)
  const visible = expanded ? signals : signals.slice(0, 3)

  if (signals.length === 0) {
    return (
      <div className="rounded-lg border border-[#10B981]/30 bg-[#10B981]/5 p-4">
        <p className="text-sm text-[#10B981]">No risk signals detected</p>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-medium text-[#F8FAFC]">
        Risk Signals ({signals.length})
      </h3>
      {visible.map((signal, i) => (
        <div
          key={i}
          className={`rounded-lg border p-3 ${
            signal.type === "critical"
              ? "border-[#EF4444]/30 bg-[#EF4444]/5"
              : "border-[#F59E0B]/30 bg-[#F59E0B]/5"
          }`}
        >
          <div className="flex items-start gap-2">
            <span className="mt-0.5 text-sm">
              {signal.type === "critical" ? "🔴" : "🟡"}
            </span>
            <div>
              <p className="text-sm text-[#F8FAFC]">{signal.message}</p>
              <p className="mt-0.5 text-xs text-[#94A3B8]">{signal.code}</p>
            </div>
          </div>
        </div>
      ))}
      {signals.length > 3 && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-xs text-[#6366F1] transition-colors hover:text-[#818CF8]"
        >
          {expanded ? "Show less" : `Show ${signals.length - 3} more`}
        </button>
      )}
    </div>
  )
}
