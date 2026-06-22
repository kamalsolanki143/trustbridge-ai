interface ConsentTraceEntry {
  source: string
  accessed_at: string
  purpose: string
  data_used: string[]
}

interface ConsentTraceProps {
  entries: ConsentTraceEntry[]
}

export default function ConsentTrace({ entries }: ConsentTraceProps) {
  if (entries.length === 0) {
    return (
      <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-6 text-center">
        <p className="text-sm text-[#94A3B8]">No consent trace available yet.</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-medium text-[#F8FAFC]">Consent Trace</h3>
      <div className="space-y-2">
        {entries.map((entry, i) => (
          <div
            key={i}
            className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-4"
          >
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium capitalize text-[#F8FAFC]">
                {entry.source}
              </span>
              <span className="text-xs text-[#94A3B8]">
                {new Date(entry.accessed_at).toLocaleString()}
              </span>
            </div>
            <p className="mt-1 text-xs text-[#6366F1]">Purpose: {entry.purpose}</p>
            <div className="mt-2 flex flex-wrap gap-1">
              {entry.data_used.map((d) => (
                <span
                  key={d}
                  className="rounded bg-[#1E1E2E] px-2 py-0.5 text-xs text-[#94A3B8]"
                >
                  {d}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
