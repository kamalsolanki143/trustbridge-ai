"use client"

import { useRef } from "react"
import { motion, useInView } from "framer-motion"

const features = [
  {
    icon: (
      <span className="text-2xl font-bold tracking-tight" style={{ color: "#00C9A7", fontFamily: "'Space Grotesk', sans-serif" }}>
        A-
      </span>
    ),
    title: "Explainable Readiness Grade",
    body: "A+ to D grades computed from GST compliance, UPI patterns, AA bank data, and invoice history — with full reason codes.",
    tag: "CORE ENGINE",
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#00C9A7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="2" width="20" height="20" rx="0" />
        <line x1="6" y1="12" x2="10" y2="12" />
        <line x1="6" y1="16" x2="14" y2="16" />
        <line x1="6" y1="8" x2="18" y2="8" />
      </svg>
    ),
    title: "Confidence Band",
    body: "Every score ships with a confidence level — High, Medium, or Low — based on data coverage and history depth.",
    tag: "TRANSPARENCY",
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#00C9A7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 6v6l4 2" />
      </svg>
    ),
    title: "Data Coverage Meter",
    body: "Lenders see exactly how much data backs a decision. 3 of 5 sources connected means 60% coverage — always visible.",
    tag: "TRUST LAYER",
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#00C9A7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="12" y1="20" x2="12" y2="10" />
        <line x1="18" y1="20" x2="18" y2="4" />
        <line x1="6" y1="20" x2="6" y2="16" />
      </svg>
    ),
    title: "4-Stage Credit Ladder",
    body: "Pre-Qualified → Starter Loan → Improve First → Manual Review. No binary rejections. Every MSME gets a next step.",
    tag: "LADDER ENGINE",
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#00C9A7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
        <polyline points="10 9 9 9 8 9" />
      </svg>
    ),
    title: "AI Underwriting Memos",
    body: "Claude AI converts financial signals into plain-language underwriting summaries — reducing manual effort by 80%.",
    tag: "POWERED BY CLAUDE",
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#00C9A7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
      </svg>
    ),
    title: "Dynamic Credit Roadmap",
    body: "Rejected? Get a precise roadmap: connect GST, add 3 months history, improve collection — and watch your grade climb.",
    tag: "FINANCIAL INCLUSION",
  },
]

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
}

export default function Features() {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: "-100px" })

  return (
    <section id="solution" className="px-6 py-24 md:py-32" style={{ backgroundColor: "#07080F" }}>
      <div className="mx-auto max-w-7xl">
        <div className="mx-auto max-w-[600px] text-center">
          <p className="mb-4 font-mono text-[11px] font-medium tracking-[0.2em]" style={{ color: "#00C9A7" }}>
            WHAT WE BUILD
          </p>
          <h2 className="text-[36px] font-semibold leading-tight tracking-[-1px] md:text-[42px]" style={{ fontFamily: "'Space Grotesk', sans-serif", color: "#F0F2FF" }}>
            Every signal. Every insight.<br />One decision.
          </h2>
        </div>

        <div ref={ref} className="mt-16 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial="hidden"
              animate={inView ? "visible" : "hidden"}
              variants={cardVariants}
              transition={{ delay: i * 0.1 }}
              className="group p-8 transition-all duration-300"
              style={{
                backgroundColor: "#0E0F1A",
                border: "1px solid",
                borderColor: "#1C1D2E",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = "#00C9A730"
                e.currentTarget.style.transform = "translateY(-4px)"
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = "#1C1D2E"
                e.currentTarget.style.transform = "translateY(0)"
              }}
            >
              <div className="mb-5 flex h-10 w-10 items-center justify-center" style={{ backgroundColor: "#00C9A710" }}>
                {feature.icon}
              </div>
              <h3 className="mb-3 text-lg font-semibold" style={{ fontFamily: "'Space Grotesk', sans-serif", color: "#F0F2FF" }}>
                {feature.title}
              </h3>
              <p className="text-sm leading-relaxed" style={{ color: "#8B8FA8", fontFamily: "'Inter', sans-serif" }}>
                {feature.body}
              </p>
              <p className="mt-5 font-mono text-[10px] font-medium tracking-[0.15em]" style={{ color: "#00C9A7" }}>
                {feature.tag}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
