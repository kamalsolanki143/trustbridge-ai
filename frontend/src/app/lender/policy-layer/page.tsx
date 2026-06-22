"use client"

import PolicySelector from "../../../components/lender/PolicySelector"

const mockPolicies = [
  {
    id: "policy-1",
    name: "Standard MSME Loan",
    min_score: 70,
    min_confidence: "High",
    max_emi_burden: 30,
    min_turnover: 2400000,
    loan_types: ["Working Capital", "Term Loan"],
    is_active: true,
  },
  {
    id: "policy-2",
    name: "Starter Loan Product",
    min_score: 50,
    min_confidence: "Medium",
    max_emi_burden: 40,
    min_turnover: 1000000,
    loan_types: ["Micro Credit", "Equipment Finance"],
    is_active: true,
  },
  {
    id: "policy-3",
    name: "Growth Stage Lending",
    min_score: 60,
    min_confidence: "Medium",
    max_emi_burden: 35,
    min_turnover: 1800000,
    loan_types: ["Business Expansion", "Invoice Discounting"],
    is_active: false,
  },
  {
    id: "policy-4",
    name: "Emergency Credit Line",
    min_score: 40,
    min_confidence: "Low",
    max_emi_burden: 50,
    min_turnover: 500000,
    loan_types: ["Overdraft", "Emergency Loan"],
    is_active: true,
  },
]

import Navbar from "../../../components/common/Navbar"
import Footer from "../../../components/common/Footer"

export default function PolicyLayerPage() {
  const handleSelect = (policy: (typeof mockPolicies)[0]) => {
    alert(`Selected: ${policy.name}`)
  }

  return (
    <div className="flex min-h-screen flex-col bg-[#0A0A0F]">
      <Navbar role="lender" />
      <main className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-3xl">
          <h1 className="mb-2 text-2xl font-bold text-[#F8FAFC]">Policy Layer</h1>
          <p className="mb-6 text-sm text-[#94A3B8]">
            Configure lending policies that map readiness outcomes to loan products
          </p>
          <PolicySelector policies={mockPolicies} onSelect={handleSelect} />
        </div>
      </main>
      <Footer />
    </div>
  )
}
