"use client"

export default function Footer() {
  return (
    <footer className="border-t border-[#1C1D2E] bg-[#07080F]">
      <div className="mx-auto max-w-7xl px-6 py-16">
        <div className="grid gap-10 md:grid-cols-4">
          {/* Section 1 */}
          <div className="flex flex-col justify-between">
            <div>
              <div className="flex items-baseline gap-1">
                <span className="text-xl font-bold tracking-tight text-white" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                  TrustBridge
                </span>
                <span className="text-xl font-bold tracking-tight text-[#00C9A7]" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                  AI
                </span>
              </div>
              <p className="mt-3 text-sm leading-relaxed text-slate-300" style={{ fontFamily: "'Inter', sans-serif" }}>
                Building Trust Between MSMEs and Credit
              </p>
            </div>
            <div className="mt-6">
              <span className="inline-flex items-center gap-1.5 rounded border border-[#1C1D2E] bg-[#0E0F1A] px-3 py-1.5 font-mono text-[11px] text-slate-400">
                <span>🏦</span> IDBI Innovate 2026 Submission
              </span>
            </div>
          </div>

          {/* Section 2 */}
          <div>
            <h4 className="mb-4 font-mono text-[11px] font-semibold uppercase tracking-[0.15em] text-white">
              PRODUCT
            </h4>
            <ul className="space-y-2.5">
              {[
                { name: "How It Works", href: "#" },
                { name: "Credit Ladder", href: "#" },
                { name: "Credit Readiness API", href: "#" },
                { name: "Borrower Journey", href: "#" }
              ].map((item) => (
                <li key={item.name}>
                  <a
                    href={item.href}
                    className="text-sm text-slate-400 transition-colors duration-300 hover:text-[#00C9A7]"
                    style={{ fontFamily: "'Inter', sans-serif" }}
                  >
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Section 3 */}
          <div>
            <h4 className="mb-4 font-mono text-[11px] font-semibold uppercase tracking-[0.15em] text-white">
              COMPLIANCE
            </h4>
            <ul className="space-y-2.5">
              {[
                { name: "RBI Account Aggregator (AA)", href: "#" },
                { name: "Consent Management", href: "#" },
                { name: "Data Privacy", href: "#" }
              ].map((item) => (
                <li key={item.name}>
                  <a
                    href={item.href}
                    className="text-sm text-slate-400 transition-colors duration-300 hover:text-[#00C9A7]"
                    style={{ fontFamily: "'Inter', sans-serif" }}
                  >
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Section 4 */}
          <div>
            <h4 className="mb-4 font-mono text-[11px] font-semibold uppercase tracking-[0.15em] text-white">
              HACKATHON
            </h4>
            <ul className="space-y-2.5">
              {[
                { name: "IDBI Innovate 2026", href: "#" },
                { name: "Track 03 – Financial Inclusion", href: "#" }
              ].map((item) => (
                <li key={item.name}>
                  <a
                    href={item.href}
                    className="text-sm text-slate-400 transition-colors duration-300 hover:text-[#00C9A7]"
                    style={{ fontFamily: "'Inter', sans-serif" }}
                  >
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom row */}
      <div className="border-t border-[#1C1D2E]">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-6 py-6 md:flex-row">
          <span className="font-mono text-xs text-slate-400">
            &copy; 2026 TrustBridge AI. All Rights Reserved.
          </span>
          <span className="font-mono text-xs text-slate-400">
            Powered by Compass Crew Team
          </span>
        </div>
      </div>
    </footer>
  )
}

