"use client"

import { useEffect, useState } from "react"
import { motion } from "framer-motion"

const navLinks = [
  { label: "Solution", href: "#solution" },
  { label: "How It Works", href: "#how-it-works" },
  { label: "Why TrustBridge", href: "#why-trustbridge" },
  { label: "FAQ", href: "#faq" },
]

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  return (
    <nav
      className="sticky top-0 z-50 h-16 w-full border-b backdrop-blur-xl transition-colors"
      style={{
        backgroundColor: "rgba(7, 8, 15, 0.8)",
        borderColor: scrolled ? "#2A2B40" : "#1C1D2E",
      }}
    >
      <div className="mx-auto flex h-full max-w-7xl items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <a href="/" className="flex items-baseline gap-1">
            <span className="font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: "22px", color: "#F0F2FF" }}>
              TrustBridge
            </span>
            <span className="font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: "22px", color: "#00C9A7" }}>
              AI
            </span>
          </a>
          <span style={{ color: "#4A4D6A" }}>·</span>
          <span className="font-mono text-xs tracking-wide" style={{ color: "#4A4D6A" }}>
            IDBI Innovate 2026
          </span>
        </div>

        <div className="hidden items-center gap-8 md:flex">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="group relative text-sm transition-colors"
              style={{ color: "#8B8FA8", fontFamily: "'Inter', sans-serif" }}
            >
              {link.label}
              <span
                className="absolute -bottom-1 left-0 h-0.5 w-0 transition-all duration-300 group-hover:w-full"
                style={{ backgroundColor: "#00C9A7" }}
              />
            </a>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <a
            href="/lender"
            className="px-5 py-2.5 text-sm font-medium transition-all duration-200"
            style={{
              border: "1px solid #2A2B40",
              color: "#8B8FA8",
              fontFamily: "'Inter', sans-serif",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = "#00C9A7"
              e.currentTarget.style.color = "#00C9A7"
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = "#2A2B40"
              e.currentTarget.style.color = "#8B8FA8"
            }}
          >
            I&apos;m a Lender
          </a>
          <a
            href="/borrower"
            className="px-5 py-2.5 text-sm font-medium text-white transition-all duration-200"
            style={{
              backgroundColor: "#00C9A7",
              fontFamily: "'Inter', sans-serif",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = "0 0 30px rgba(0,201,167,0.25), 0 0 60px rgba(0,201,167,0.1)"
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = "none"
            }}
          >
            Apply Now
          </a>
        </div>
      </div>
    </nav>
  )
}
