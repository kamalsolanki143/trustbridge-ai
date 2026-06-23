"use client"

import { useState } from "react"
import Navbar from "../../../components/common/Navbar"
import Footer from "../../../components/common/Footer"
import GrowthRoadmap from "../../../components/roadmap/GrowthRoadmap"
import type { GrowthRoadmap as GrowthRoadmapType } from "../../../types/recommendation"

const mockRoadmap: GrowthRoadmapType = {
  current_grade: "A-",
  target_grade: "A",
  progress_percent: 65,
  milestones: [
    {
      title: "Increase Monthly Inflows by 15%",
      description: "Expand B2B client base to increase average monthly UPI/bank inflows. Target: ₹3.7L/month.",
      impact: "High",
      timeline: "3-4 months",
      effort: "Medium",
    },
    {
      title: "Achieve 100% GST Filing Compliance",
      description: "File pending GST returns for the current month to achieve 12/12 filing record.",
      impact: "High",
      timeline: "1 month",
      effort: "Low",
    },
    {
      title: "Maintain EMI Burden Below 25%",
      description: "Continue current debt management. Consider prepayment if surplus cash allows.",
      impact: "Medium",
      timeline: "Ongoing",
      effort: "Low",
    },
    {
      title: "Hire 2 Additional Employees",
      description: "Expand team to strengthen EPFO footprint and demonstrate business growth.",
      impact: "Medium",
      timeline: "6 months",
      effort: "High",
    },
    {
      title: "Digitize Invoice Management",
      description: "Move to e-invoicing for all B2B transactions to improve data traceability.",
      impact: "Low",
      timeline: "2 months",
      effort: "Low",
    },
  ],
}

export default function RoadmapPage() {
  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="borrower" />
      <main className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-3xl">
          <div className="mb-6">
            <span className="rounded bg-[#1E1E2E] px-2 py-1 text-xs text-[#94A3B8]">Step 4 of 4</span>
            <h1 className="mt-2 text-2xl font-bold text-[#F8FAFC]">Growth Roadmap</h1>
            <p className="text-sm text-[#94A3B8]">Personalized plan to improve your credit readiness grade</p>
          </div>

          <GrowthRoadmap roadmap={mockRoadmap} />
        </div>
      </main>
      <Footer />
    </div>
  )
}
