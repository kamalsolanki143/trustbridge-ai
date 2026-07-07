"use client"

import { useRef } from "react"
import { motion, useInView } from "framer-motion"

export default function CTA() {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: "-100px" })

  return (
    <section id="why-trustbridge" className="relative overflow-hidden px-6 py-24 md:py-32" style={{ backgroundColor: "#07080F" }}>
      <div
        className="pointer-events-none absolute -left-60 -top-60 h-[600px] w-[600px] rounded-full opacity-[0.06]"
        style={{ background: "radial-gradient(circle, #00C9A7 0%, transparent 70%)" }}
      />
      <div
        className="pointer-events-none absolute -bottom-60 -right-60 h-[600px] w-[600px] rounded-full opacity-[0.06]"
        style={{ background: "radial-gradient(circle, #6366F1 0%, transparent 70%)" }}
      />

      <motion.div
        ref={ref}
        initial={{ opacity: 0, y: 30 }}
        animate={inView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.7, ease: "easeOut" as const }}
        className="relative z-10 mx-auto max-w-3xl text-center rounded-2xl backdrop-blur-sm"
        style={{
          border: "1px solid",
          borderColor: "#00C9A720",
          backgroundColor: "#0E0F1A/80",
          padding: "64px 48px",
        }}
      >
        <p className="mb-4 font-mono text-[11px] font-medium tracking-[0.2em]" style={{ color: "#00C9A7" }}>
          BUILT FOR IDBI INNOVATE 2026
        </p>

        <h2
          className="text-[36px] font-semibold leading-tight tracking-[-1px] md:text-[42px]"
          style={{ fontFamily: "'Space Grotesk', sans-serif", color: "#F0F2FF" }}
        >
          &ldquo;From credit invisible<br />to credit ready.&rdquo;
        </h2>

        <p className="mx-auto mt-6 max-w-[520px] text-base leading-relaxed text-slate-300" style={{ fontFamily: "'Inter', sans-serif" }}>
          The same MSME rejected 3 times with documents gets assessed in 10 seconds using data they already generate.
        </p>

        <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a
            href="/borrower"
            className="rounded px-8 py-4 text-[15px] font-semibold text-white transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]"
            style={{
              backgroundColor: "#00C9A7",
              fontFamily: "'Space Grotesk', sans-serif",
              boxShadow: "0 0 20px rgba(0,201,167,0.15), 0 0 40px rgba(0,201,167,0.05)",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = "0 0 30px rgba(0,201,167,0.25), 0 0 60px rgba(0,201,167,0.1)"
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = "0 0 20px rgba(0,201,167,0.15), 0 0 40px rgba(0,201,167,0.05)"
            }}
          >
            Try the Demo
          </a>
          <a
            href="#solution"
            className="rounded px-8 py-4 text-[15px] font-semibold transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]"
            style={{
              border: "1px solid #2A2B40",
              color: "#F0F2FF",
              fontFamily: "'Space Grotesk', sans-serif",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = "#00C9A7"
              e.currentTarget.style.boxShadow = "0 0 20px rgba(0,201,167,0.1)"
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = "#2A2B40"
              e.currentTarget.style.boxShadow = "none"
            }}
          >
            View Architecture
          </a>
        </div>

        <div className="mt-10 flex items-center justify-center gap-4 font-mono text-xs text-slate-400">
          <span>🏦 IDBI Bank</span>
          <span style={{ color: "#1C1D2E" }}>·</span>
          <span>Track 03</span>
          <span style={{ color: "#1C1D2E" }}>·</span>
          <span>Financial Inclusion</span>
        </div>
      </motion.div>
    </section>
  )
}
