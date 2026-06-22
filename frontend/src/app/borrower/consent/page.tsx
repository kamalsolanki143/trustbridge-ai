"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Navbar from "../../../components/common/Navbar"
import Footer from "../../../components/common/Footer"
import ConsentCard from "../../../components/consent/ConsentCard"

export default function ConsentPage() {
  const router = useRouter()
  const [approvedSources, setApprovedSources] = useState<string[]>([])
  const [granted, setGranted] = useState(false)

  const handleApproveAll = (sources: string[]) => {
    setApprovedSources(sources)
  }

  const handleApproveSingle = (source: string, approved: boolean) => {
    setApprovedSources((prev) =>
      approved ? [...prev, source] : prev.filter((s) => s !== source)
    )
  }

  const handleGrant = () => {
    setGranted(true)
    setTimeout(() => {
      router.push("/borrower/readiness")
    }, 1500)
  }

  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="borrower" />
      <main className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-2xl">
          <div className="mb-6">
            <div className="mb-4 flex items-center gap-3">
              <span className="rounded bg-[#1E1E2E] px-2 py-1 text-xs text-[#94A3B8]">
                Step 1 of 4
              </span>
              <span className="text-xs text-[#4A4A5A]">Consent &bull; Readiness &bull; Summary &bull; Roadmap</span>
            </div>
            <h1 className="text-2xl font-bold text-[#F8FAFC]">Data Consent</h1>
            <p className="mt-1 text-sm text-[#94A3B8]">
              Grant permission to access your financial data via RBI AA Framework
            </p>
          </div>

          {!granted ? (
            <>
              <ConsentCard
                onApproveAll={handleApproveAll}
                onApproveSingle={handleApproveSingle}
              />

              <div className="mt-6">
                <button
                  onClick={handleGrant}
                  disabled={approvedSources.length === 0}
                  className="w-full rounded-lg bg-[#6366F1] px-6 py-3 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {approvedSources.length === 0
                    ? "Select at least one data source"
                    : `Grant Consent (${approvedSources.length} sources)`}
                </button>
              </div>
            </>
          ) : (
            <div className="rounded-lg border border-[#10B981]/30 bg-[#10B981]/5 p-8 text-center">
              <div className="text-4xl">✅</div>
              <h2 className="mt-3 text-lg font-semibold text-[#10B981]">Consent Granted</h2>
              <p className="mt-1 text-sm text-[#94A3B8]">
                Redirecting to your readiness dashboard...
              </p>
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  )
}
