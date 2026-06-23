"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"

interface NavbarProps {
  role: "borrower" | "lender" | "admin"
}

const roleLabels = {
  borrower: "Borrower Portal",
  lender: "Lender Portal",
  admin: "Admin Panel",
}

export default function Navbar({ role }: NavbarProps) {
  const pathname = usePathname()

  return (
    <nav className="border-b border-[#1E1E2E] bg-[#0A0A0F] px-6 py-4">
      <div className="mx-auto flex max-w-7xl items-center justify-between">
        <div className="flex items-center gap-8">
          <Link href={`/${role}`} className="text-xl font-bold text-[#F8FAFC]">
            TrustBridge <span className="text-[#6366F1]">AI</span>
          </Link>
          <span className="rounded-full bg-[#1E1E2E] px-3 py-1 text-xs text-[#94A3B8]">
            {roleLabels[role]}
          </span>
        </div>

        <div className="flex items-center gap-6">
          {role === "borrower" && (
            <>
              <NavLink href="/borrower/consent" current={pathname} label="Consent" />
              <NavLink href="/borrower/readiness" current={pathname} label="Readiness" />
              <NavLink href="/borrower/trust-summary" current={pathname} label="Summary" />
              <NavLink href="/borrower/roadmap" current={pathname} label="Roadmap" />
            </>
          )}
          {role === "lender" && (
            <>
              <NavLink href="/lender" current={pathname} label="Dashboard" />
              <NavLink href="/lender/applications" current={pathname} label="Applications" />
              <NavLink href="/lender/readiness-analysis" current={pathname} label="Analysis" />
              <NavLink href="/lender/manual-review" current={pathname} label="Reviews" />
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

function NavLink({ href, current, label }: { href: string; current: string; label: string }) {
  const isActive = current === href || current.startsWith(href + "/")
  return (
    <Link
      href={href}
      className={`text-sm transition-colors ${
        isActive ? "text-[#6366F1]" : "text-[#94A3B8] hover:text-[#F8FAFC]"
      }`}
    >
      {label}
    </Link>
  )
}
