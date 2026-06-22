"use client"

export default function Footer() {
  return (
    <footer style={{ backgroundColor: "#07080F", borderTop: "1px solid #1C1D2E" }}>
      <div className="mx-auto max-w-7xl px-6 py-16">
        <div className="grid gap-10 md:grid-cols-4">
          <div>
            <div className="flex items-baseline gap-1">
              <span className="font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: "20px", color: "#F0F2FF" }}>
                TrustBridge
              </span>
              <span className="font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: "20px", color: "#00C9A7" }}>
                AI
              </span>
            </div>
            <p className="mt-3 text-sm leading-relaxed" style={{ color: "#4A4D6A", fontFamily: "'Inter', sans-serif" }}>
              Building Trust Between MSMEs and Credit
            </p>
            <div
              className="mt-5 inline-block px-3 py-2 font-mono text-[11px]"
              style={{ border: "1px solid #1C1D2E", color: "#4A4D6A" }}
            >
              🏦 IDBI Innovate 2026<br />Track 03 Submission
            </div>
          </div>

          <div>
            <p className="mb-4 font-mono text-[11px] font-medium tracking-[0.15em]" style={{ color: "#00C9A7" }}>
              PRODUCT
            </p>
            <ul className="space-y-3">
              {["How It Works", "Credit Ladder", "Readiness API", "Data Sources", "For Lenders"].map((item) => (
                <li key={item}>
                  <a
                    href="#"
                    className="text-sm transition-colors duration-200"
                    style={{ color: "#8B8FA8", fontFamily: "'Inter', sans-serif" }}
                    onMouseEnter={(e) => { e.currentTarget.style.color = "#00C9A7" }}
                    onMouseLeave={(e) => { e.currentTarget.style.color = "#8B8FA8" }}
                  >
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <p className="mb-4 font-mono text-[11px] font-medium tracking-[0.15em]" style={{ color: "#00C9A7" }}>
              COMPLIANCE
            </p>
            <ul className="space-y-3">
              {["RBI AA Framework", "Data Privacy", "Consent Management", "OCEN Integration", "Security"].map((item) => (
                <li key={item}>
                  <a
                    href="#"
                    className="text-sm transition-colors duration-200"
                    style={{ color: "#8B8FA8", fontFamily: "'Inter', sans-serif" }}
                    onMouseEnter={(e) => { e.currentTarget.style.color = "#00C9A7" }}
                    onMouseLeave={(e) => { e.currentTarget.style.color = "#8B8FA8" }}
                  >
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <p className="mb-4 font-mono text-[11px] font-medium tracking-[0.15em]" style={{ color: "#00C9A7" }}>
              IDBI INNOVATE 2026
            </p>
            <ul className="space-y-3">
              {[
                "Track 03: Financial Inclusion",
                "Team: TrustBridge AI",
                "Theme: Build. Integrate. Transform.",
              ].map((item) => (
                <li key={item}>
                  <span className="text-sm" style={{ color: "#8B8FA8", fontFamily: "'Inter', sans-serif" }}>
                    {item}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <div className="border-t" style={{ borderColor: "#1C1D2E" }}>
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-3 px-6 py-5 md:flex-row">
          <span className="font-mono text-[11px]" style={{ color: "#4A4D6A" }}>
            &copy; 2026 TrustBridge AI. Built for IDBI Innovate 2026.
          </span>
          <span className="font-mono text-[11px]" style={{ color: "#4A4D6A" }}>
            Powered by Claude AI · FastAPI · Next.js
          </span>
        </div>
      </div>
    </footer>
  )
}
