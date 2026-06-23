import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "TrustBridge AI — MSME Credit Ladder Engine",
  description: "AI-powered credit readiness assessment for Indian MSMEs",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-[#0A0A0F] text-[#F8FAFC] antialiased">{children}</body>
    </html>
  )
}
