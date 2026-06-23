"use client"

import { useState, useEffect } from "react"
import Navbar from "../../components/common/Navbar"
import Footer from "../../components/common/Footer"
import Loader from "../../components/common/Loader"

const systemMetrics = [
  { label: "Total Assessments Run", value: 145 },
  { label: "Avg Processing Time", value: "1.2s" },
  { label: "Data Sources Connected", value: 23 },
  { label: "Active Consent Tokens", value: 18 },
  { label: "Claude API Calls", value: "892" },
  { label: "System Uptime", value: "99.8%" },
]

const recentActivity = [
  { action: "Assessment created", entity: "Sharma Textile Works", timestamp: "2 min ago" },
  { action: "Consent granted", entity: "Patel Hardware Suppliers", timestamp: "15 min ago" },
  { action: "Manual review submitted", entity: "Khan Catering Services", timestamp: "1 hr ago" },
  { action: "Policy updated", entity: "Standard MSME Loan", timestamp: "3 hrs ago" },
  { action: "Seed data loaded", entity: "3 MSME profiles", timestamp: "1 day ago" },
]

export default function AdminPage() {
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 500)
    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
        <Navbar role="admin" />
        <main className="flex flex-1 items-center justify-center">
          <Loader text="Loading admin panel..." />
        </main>
        <Footer />
      </div>
    )
  }

  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="admin" />
      <main className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-5xl">
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-[#F8FAFC]">Admin Panel</h1>
            <p className="mt-1 text-sm text-[#94A3B8]">System monitoring and configuration</p>
          </div>

          <div className="mb-8 grid gap-4 sm:grid-cols-3 lg:grid-cols-6">
            {systemMetrics.map((metric) => (
              <div
                key={metric.label}
                className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-4 text-center"
              >
                <p className="text-lg font-bold text-[#F8FAFC]">{metric.value}</p>
                <p className="mt-1 text-xs text-[#94A3B8]">{metric.label}</p>
              </div>
            ))}
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-5">
              <h2 className="mb-4 text-sm font-medium text-[#F8FAFC]">Recent Activity</h2>
              <div className="space-y-3">
                {recentActivity.map((item, i) => (
                  <div key={i} className="flex items-center justify-between border-b border-[#1E1E2E] pb-2 last:border-b-0 last:pb-0">
                    <div>
                      <p className="text-sm text-[#F8FAFC]">{item.action}</p>
                      <p className="text-xs text-[#94A3B8]">{item.entity}</p>
                    </div>
                    <span className="text-xs text-[#4A4A5A]">{item.timestamp}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-5">
              <h2 className="mb-4 text-sm font-medium text-[#F8FAFC]">Quick Actions</h2>
              <div className="space-y-3">
                {[
                  { label: "Re-seed Database", desc: "Reload the 3 synthetic MSME profiles" },
                  { label: "Run All Assessments", desc: "Trigger readiness engine for all MSMEs" },
                  { label: "Export Audit Log", desc: "Download system activity log (CSV)" },
                  { label: "Test Claude API", desc: "Verify Claude API connectivity and response" },
                ].map((action) => (
                  <button
                    key={action.label}
                    className="w-full rounded-lg border border-[#1E1E2E] bg-[#0A0A0F] px-4 py-3 text-left transition-colors hover:border-[#6366F1]/50"
                  >
                    <p className="text-sm font-medium text-[#F8FAFC]">{action.label}</p>
                    <p className="text-xs text-[#94A3B8]">{action.desc}</p>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
