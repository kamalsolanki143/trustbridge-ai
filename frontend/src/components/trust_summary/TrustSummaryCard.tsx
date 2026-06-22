"use client"

import { useState, useEffect } from "react"
import type { ReadinessAssessment } from "../../types/readiness"

interface TrustSummaryCardProps {
  assessment: ReadinessAssessment
}

export default function TrustSummaryCard({ assessment }: TrustSummaryCardProps) {
  const [displayedSummary, setDisplayedSummary] = useState("")
  const [isTyping, setIsTyping] = useState(true)

  useEffect(() => {
    if (!assessment.ai_summary) {
      setIsTyping(false)
      return
    }

    let i = 0
    const interval = setInterval(() => {
      if (i < assessment.ai_summary!.length) {
        setDisplayedSummary(assessment.ai_summary!.slice(0, i + 1))
        i++
      } else {
        clearInterval(interval)
        setIsTyping(false)
      }
    }, 15)

    return () => clearInterval(interval)
  }, [assessment.ai_summary])

  return (
    <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-6">
      <h3 className="mb-4 text-sm font-medium text-[#F8FAFC]">AI Underwriting Summary</h3>
      <div className="relative">
        <p className="text-sm leading-relaxed text-[#94A3B8]">
          {displayedSummary}
          {isTyping && <span className="ml-0.5 animate-pulse text-[#6366F1]">|</span>}
        </p>
      </div>
    </div>
  )
}
