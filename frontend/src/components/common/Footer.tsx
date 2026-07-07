export default function Footer() {
  return (
    <footer className="border-t border-[#1E1E2E] bg-[#0A0A0F] px-6 py-5">
      <div className="mx-auto flex max-w-7xl items-center justify-between text-xs text-slate-400">
        <span>&copy; {new Date().getFullYear()} TrustBridge AI. All rights reserved.</span>
        <div className="flex gap-6">
          <span className="flex items-center gap-1">🏦 IDBI Bank Partner</span>
          <span className="flex items-center gap-1">🛡️ RBI AA Framework Compliant</span>
        </div>
      </div>
    </footer>
  )
}
