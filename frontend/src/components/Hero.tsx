"use client"

import { useEffect, useRef, useState } from "react"
import { motion } from "framer-motion"

function useCountUp(target: number, duration = 2, start = false) {
  const [count, setCount] = useState(0)
  const ref = useRef<number | null>(null)

  useEffect(() => {
    if (!start) return
    let startTime: number | null = null
    const animate = (ts: number) => {
      if (!startTime) startTime = ts
      const elapsed = (ts - startTime) / 1000
      const progress = Math.min(elapsed / duration, 1)
      setCount(Math.floor(progress * target))
      if (progress < 1) ref.current = requestAnimationFrame(animate)
    }
    ref.current = requestAnimationFrame(animate)
    return () => { if (ref.current) cancelAnimationFrame(ref.current) }
  }, [target, duration, start])

  return count
}

function CounterStat({ value, label, suffix = "" }: { value: number; label: string; suffix?: string }) {
  const ref = useRef<HTMLDivElement>(null)
  const [inView, setInView] = useState(false)
  const count = useCountUp(value, 2, inView)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setInView(true); observer.disconnect() } },
      { threshold: 0.3 }
    )
    observer.observe(el)
    return () => observer.disconnect()
  }, [])

  const display = value >= 10000000
    ? `${(count / 10000000).toFixed(1)}Cr`
    : value >= 100000
      ? `₹${(count / 100000).toFixed(0)}L Cr`
      : `${count}${suffix}`

  return (
    <div ref={ref} className="flex flex-col items-center border-r px-6 last:border-r-0" style={{ borderColor: "#1C1D2E" }}>
      <span className="text-4xl font-bold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif", color: "#00C9A7", fontSize: "36px" }}>
        {display}
      </span>
      <span className="mt-1 text-center text-xs leading-relaxed" style={{ color: "#4A4D6A", fontFamily: "'Inter', sans-serif" }}>
        {label}
      </span>
    </div>
  )
}

const stagger = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1 } },
}

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" as const } },
}

export default function Hero() {
  const [reducedMotion, setReducedMotion] = useState(false)

  useEffect(() => {
    setReducedMotion(window.matchMedia("(prefers-reduced-motion: reduce)").matches)
  }, [])

  return (
    <section
      className="relative min-h-screen overflow-hidden"
      style={{ backgroundColor: "#07080F" }}
    >
      <div
        className="absolute inset-0"
        style={{
          backgroundImage:
            "linear-gradient(rgba(0, 201, 167, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 201, 167, 0.03) 1px, transparent 1px)",
          backgroundSize: "40px 40px",
          animation: reducedMotion ? "none" : "gridPulse 8s ease-in-out infinite",
        }}
      />
      <div
        className="pointer-events-none absolute -left-40 -top-40 h-[500px] w-[500px] rounded-full opacity-[0.04]"
        style={{ background: "radial-gradient(circle, #00C9A7 0%, transparent 70%)" }}
      />
      <div
        className="pointer-events-none absolute -bottom-40 -right-40 h-[500px] w-[500px] rounded-full opacity-[0.04]"
        style={{ background: "radial-gradient(circle, #6366F1 0%, transparent 70%)" }}
      />

      <div className="relative z-10 mx-auto max-w-7xl px-6 pt-24 md:pt-32">
        <motion.div
          className="mx-auto max-w-[900px] text-center"
          variants={stagger}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={fadeUp} className="mb-8 inline-flex items-center gap-2 border-l-4 px-4 py-2" style={{ borderColor: "#00C9A7", backgroundColor: "#00C9A710" }}>
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full opacity-75" style={{ backgroundColor: "#00C9A7" }} />
              <span className="relative inline-flex h-2 w-2 rounded-full" style={{ backgroundColor: "#00C9A7" }} />
            </span>
            <span className="font-mono text-xs font-medium tracking-wide" style={{ color: "#00C9A7" }}>
              LIVE &nbsp;MSME Credit Assessment Engine
            </span>
          </motion.div>

          <motion.h1
            variants={fadeUp}
            className="text-[56px] font-bold leading-none tracking-[-3px] md:text-[72px]"
            style={{ fontFamily: "'Space Grotesk', sans-serif" }}
          >
            <span style={{ color: "#F0F2FF" }}>Credit Invisible<br /></span>
            <span style={{ color: "#00C9A7" }}>No More.</span>
          </motion.h1>

          <motion.p
            variants={fadeUp}
            className="mx-auto mt-6 max-w-[600px] text-lg leading-relaxed"
            style={{ color: "#8B8FA8", fontFamily: "'Inter', sans-serif" }}
          >
            TrustBridge AI converts GST filings, UPI transactions, and bank data into an explainable credit readiness profile — helping IDBI Bank say yes to MSMEs that deserve it.
          </motion.p>

          <motion.div variants={fadeUp} className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <a
              href="/borrower"
              className="group relative px-8 py-4 text-[15px] font-semibold text-white transition-all duration-200"
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
              I&apos;m a Borrower →
            </a>
            <a
              href="/lender"
              className="px-8 py-4 text-[15px] font-semibold transition-all duration-200"
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
              I&apos;m a Lender
            </a>
          </motion.div>

          <motion.div variants={fadeUp} className="mt-6 flex items-center justify-center gap-4">
            {[
              "🏦 IDBI Bank Partner",
              "🔒 RBI AA Framework",
              "⚡ 10-Second Assessment",
            ].map((item, i) => (
              <div key={i} className="flex items-center gap-2">
                <span className="font-mono text-xs" style={{ color: "#4A4D6A" }}>
                  {item}
                </span>
                {i < 2 && <span style={{ color: "#1C1D2E" }}>|</span>}
              </div>
            ))}
          </motion.div>

          <motion.div
            variants={fadeUp}
            className="mt-10 flex items-center justify-center gap-0 border border-[#1C1D2E] py-6"
            style={{ backgroundColor: "#0E0F1A" }}
          >
            <CounterStat value={63000000} label="MSMEs in India" />
            <CounterStat value={2000000} label="Credit Gap (Informal)" />
            <CounterStat value={78} label="Rejection Rate" suffix="%" />
            <CounterStat value={10} label="Assessment Time" suffix=" sec" />
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2, duration: 0.8, ease: "easeOut" as const }}
          className="mx-auto mt-16 max-w-[640px]"
          style={{
            border: "1px solid",
            borderColor: "#00C9A730",
            backgroundColor: "#0E0F1A",
            boxShadow: "0 0 20px rgba(0,201,167,0.15), 0 0 40px rgba(0,201,167,0.05)",
          }}
        >
          <motion.div
            animate={reducedMotion ? {} : { y: [0, -8, 0] }}
            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" as const }}
          >
            <div className="flex items-center justify-between border-b px-6 py-4" style={{ borderColor: "#1C1D2E" }}>
              <span className="text-sm font-semibold" style={{ color: "#F0F2FF", fontFamily: "'Space Grotesk', sans-serif" }}>
                MSME Financial Health Card
              </span>
              <span className="flex items-center gap-1.5 font-mono text-xs font-medium" style={{ color: "#10B981" }}>
                <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: "#10B981" }} />
                PRE-QUALIFIED
              </span>
            </div>

            <div className="px-6 py-5">
              <p className="text-sm font-medium" style={{ color: "#F0F2FF", fontFamily: "'Inter', sans-serif" }}>
                Sharma Textile Works, Kolkata
              </p>

              <div className="mt-5 grid grid-cols-3 gap-4 border-b pb-5" style={{ borderColor: "#1C1D2E" }}>
                {[
                  { label: "Readiness Grade", value: "A-" },
                  { label: "Confidence", value: "HIGH" },
                  { label: "Coverage", value: "100%" },
                ].map((item) => (
                  <div key={item.label} className="text-center">
                    <p className="font-mono text-xs" style={{ color: "#4A4D6A" }}>{item.label}</p>
                    <p className="mt-1 text-lg font-bold tracking-tight" style={{ color: "#00C9A7", fontFamily: "'Space Grotesk', sans-serif" }}>
                      {item.value}
                    </p>
                  </div>
                ))}
              </div>

              <div className="mt-5">
                <div className="flex justify-between text-xs" style={{ color: "#4A4D6A" }}>
                  <span>Readiness Score</span>
                  <span style={{ color: "#00C9A7" }}>81/100</span>
                </div>
                <div className="mt-1.5 h-2 w-full" style={{ backgroundColor: "#1C1D2E" }}>
                  <motion.div
                    className="h-full"
                    style={{ backgroundColor: "#00C9A7" }}
                    initial={{ width: "0%" }}
                    animate={{ width: "81%" }}
                    transition={{ delay: 1.6, duration: 1, ease: "easeOut" as const }}
                  />
                </div>
              </div>

              <div className="mt-4 space-y-1.5">
                {[
                  { icon: "✓", text: "Stable Weekly Inflows", color: "#10B981" },
                  { icon: "✓", text: "GST Compliance 11/12", color: "#10B981" },
                  { icon: "⚡", text: "Seasonal Revenue Pattern", color: "#F59E0B" },
                ].map((item, i) => (
                  <div key={i} className="flex items-center gap-2 font-mono text-xs" style={{ color: "#8B8FA8" }}>
                    <span style={{ color: item.color }}>{item.icon}</span>
                    {item.text}
                  </div>
                ))}
              </div>

              <div className="mt-5 border-t pt-4 text-center font-mono text-xs font-medium tracking-wide" style={{ borderColor: "#1C1D2E", color: "#00C9A7" }}>
                Recommended: Working Capital Loan up to ₹12 Lakhs
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>

      <div className="h-20" />

      <style jsx>{`
        @keyframes gridPulse {
          0%, 100% { opacity: 0.5; }
          50% { opacity: 1; }
        }
      `}</style>
    </section>
  )
}
