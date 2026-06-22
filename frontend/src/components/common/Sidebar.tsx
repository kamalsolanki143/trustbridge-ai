"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"

interface SidebarProps {
  role: "borrower" | "lender" | "admin"
}

const borrowerLinks = [
  { href: "/borrower", label: "Dashboard", icon: "📊" },
  { href: "/borrower/consent", label: "Consent", icon: "🔐" },
  { href: "/borrower/readiness", label: "Readiness", icon: "📈" },
  { href: "/borrower/trust-summary", label: "Trust Summary", icon: "📋" },
  { href: "/borrower/roadmap", label: "Roadmap", icon: "🗺️" },
  { href: "/borrower/outcome-simulator", label: "Simulator", icon: "🎯" },
]

const lenderLinks = [
  { href: "/lender", label: "Dashboard", icon: "📊" },
  { href: "/lender/applications", label: "Applications", icon: "📑" },
  { href: "/lender/readiness-analysis", label: "Readiness Analysis", icon: "📈" },
  { href: "/lender/policy-layer", label: "Policy Layer", icon: "⚙️" },
  { href: "/lender/manual-review", label: "Manual Review", icon: "🔍" },
  { href: "/lender/simulator", label: "Simulator", icon: "🎯" },
]

const adminLinks = [
  { href: "/admin", label: "Dashboard", icon: "📊" },
  { href: "/lender", label: "Switch to Lender", icon: "🔄" },
  { href: "/borrower", label: "Switch to Borrower", icon: "🔄" },
]

export default function Sidebar({ role }: SidebarProps) {
  const pathname = usePathname()
  const links = role === "admin" ? adminLinks : role === "lender" ? lenderLinks : borrowerLinks

  return (
    <aside className="w-56 border-r border-[#1E1E2E] bg-[#0A0A0F] p-4">
      <div className="mb-6 mt-2">
        <p className="text-xs font-medium uppercase tracking-wider text-[#94A3B8]">
          {role === "admin" ? "Admin" : role === "lender" ? "Lender" : "Borrower"} Menu
        </p>
      </div>
      <nav className="flex flex-col gap-1">
        {links.map((link) => {
          const isActive = pathname === link.href
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors ${
                isActive
                  ? "bg-[#6366F1]/10 text-[#6366F1]"
                  : "text-[#94A3B8] hover:bg-[#12121A] hover:text-[#F8FAFC]"
              }`}
            >
              <span>{link.icon}</span>
              {link.label}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
