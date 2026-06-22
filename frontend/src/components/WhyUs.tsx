"use client"

import { useEffect, useRef, useState } from "react"
import { motion, useInView } from "framer-motion"

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

const rows = [
  { label: "Data Sources", traditional: "ITR, Balance Sheet only", trust: "GST, UPI, AA, EPFO, Invoice" },
  { label: "Assessment Time", traditional: "2-3 weeks", trust: "10 seconds" },
  { label: "NTC/NTB MSMEs", traditional: "Auto-reject", trust: "Starter Loan" },
  { label: "Explainability", traditional: "None", trust: "Full reason codes" },
  { label: "Rejection outcome", traditional: "No guidance", trust: "Growth roadmap" },
]

const impactStats = [
  { value: 78, suffix: "%", label: "of MSME loan applications rejected due to missing documents" },
  { value: 2000000, prefix: "₹", suffix: " Cr", label: "annual MSME credit gap in India's informal sector", transform: (v: number) => `₹${(v / 100000).toFixed(0)}L Cr` },
  { value: 10, suffix: " sec", label: "to generate a complete credit readiness profile" },
]

export default function WhyUs() {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: "-100px" })

  const [countersStarted, setCountersStarted] = useState(false)
  const countersRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const el = countersRef.current
    if (!el) return
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setCountersStarted(true); observer.disconnect() } },
      { threshold: 0.3 }
    )
    observer.observe(el)
    return () => observer.disconnect()
  }, [])

  const counter1 = useCountUp(78, 2, countersStarted)
  const counter2 = useCountUp(2000000, 2.5, countersStarted)
  const counter3 = useCountUp(10, 1.5, countersStarted)

  return (
    <section id="how-it-works" className="px-6 py-24 md:py-32" style={{ backgroundColor: "#07080F" }}>
      <div className="mx-auto max-w-7xl">
        <div className="mx-auto max-w-[600px] text-center">
          <p className="mb-4 font-mono text-[11px] font-medium tracking-[0.2em]" style={{ color: "#00C9A7" }}>
            WHY TRUSTBRIDGE
          </p>
          <h2 className="text-[36px] font-semibold leading-tight tracking-[-1px] md:text-[42px]" style={{ fontFamily: "'Space Grotesk', sans-serif", color: "#F0F2FF" }}>
            Built for the 6.3 crore<br />MSMEs banks can&apos;t see.
          </h2>
        </div>

        <div ref={ref} className="mt-16 grid gap-8 lg:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.6, ease: "easeOut" as const }}
          >
            <div className="overflow-hidden" style={{ border: "1px solid #1C1D2E" }}>
              <div className="grid grid-cols-3 border-b text-xs font-semibold uppercase tracking-wider" style={{ borderColor: "#1C1D2E", backgroundColor: "#0E0F1A", color: "#4A4D6A" }}>
                <div className="px-4 py-3" />
                <div className="border-x px-4 py-3 text-center" style={{ borderColor: "#1C1D2E", color: "#8B8FA8" }}>Traditional Lending</div>
                <div className="px-4 py-3 text-center" style={{ color: "#00C9A7" }}>TrustBridge AI</div>
              </div>
              {rows.map((row, i) => (
                <div
                  key={row.label}
                  className="grid grid-cols-3 border-b text-sm" style={{ borderColor: "#1C1D2E" }}
                >
                  <div className="px-4 py-3.5 text-xs font-medium" style={{ color: "#8B8FA8", fontFamily: "'Inter', sans-serif" }}>{row.label}</div>
                  <div className="border-x px-4 py-3.5 text-center font-mono text-xs" style={{ borderColor: "#1C1D2E", color: "#4A4D6A" }}>
                    <span className="mr-1" style={{ color: "#EF4444" }}>✕</span>{row.traditional}
                  </div>
                  <div className="px-4 py-3.5 text-center font-mono text-xs" style={{ color: "#00C9A7" }}>
                    <span className="mr-1">✓</span>{row.trust}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          <div ref={countersRef} className="flex flex-col justify-center gap-4">
            {[
              { value: `78%`, label: impactStats[0].label },
              { transform: impactStats[0].transform, label: impactStats[0].label },
              { value: `${counter3} sec`, label: impactStats[2].label },
            ].map((stat, i) => {
              const displayValue = i === 0 ? `${counter1}%` : i === 1 ? `₹${(counter2 / 100000).toFixed(0)}L Cr` : `${counter3} sec`
              return (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  animate={countersStarted ? { opacity: 1, y: 0 } : {}}
                  transition={{ delay: i * 0.15, duration: 0.6, ease: "easeOut" as const }}
                  className="border-l-[3px] px-5 py-4"
                  style={{ borderColor: "#00C9A7", backgroundColor: "#0E0F1A", borderLeftWidth: "3px" }}
                >
                  <p className="text-[42px] font-bold leading-none tracking-tight md:text-[48px]" style={{ fontFamily: "'Space Grotesk', sans-serif", color: "#00C9A7" }}>
                    {displayValue}
                  </p>
                  <p className="mt-2 text-sm leading-relaxed" style={{ color: "#8B8FA8", fontFamily: "'Inter', sans-serif" }}>
                    {stat.label}
                  </p>
                </motion.div>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
}
