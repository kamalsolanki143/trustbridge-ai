"use client"

import { motion } from "framer-motion"

export default function Header() {
  return (
    <div className="relative h-10 w-full overflow-hidden border-b" style={{ borderColor: "#00C9A720", background: "linear-gradient(90deg, #00C9A710, #6366F110, #00C9A710)" }}>
      <motion.div
        className="absolute inset-0"
        animate={{ x: ["-100%", "100%"] }}
        transition={{ duration: 8, repeat: Infinity, ease: "linear" as const }}
        style={{
          background: "linear-gradient(90deg, transparent, rgba(0,201,167,0.08), transparent)",
          width: "60%",
        }}
      />
      <div className="relative mx-auto flex h-full max-w-7xl items-center justify-between px-6">
        <span className="font-mono text-xs tracking-wide" style={{ color: "#4A4D6A" }}>
          🏦 IDBI Bank
        </span>
        <span className="font-mono text-xs tracking-wide" style={{ color: "#8B8FA8" }}>
          ✦ IDBI Innovate 2026 — Track 03: Financial Inclusion ✦
        </span>
        <span className="font-mono text-xs tracking-wide" style={{ color: "#4A4D6A" }}>
          National Fintech Hackathon
        </span>
      </div>
    </div>
  )
}
