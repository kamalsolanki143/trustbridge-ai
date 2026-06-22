export default function Footer() {
  return (
    <footer className="border-t border-[#1E1E2E] bg-[#0A0A0F] px-6 py-4">
      <div className="mx-auto flex max-w-7xl items-center justify-between text-xs text-[#94A3B8]">
        <span>&copy; {new Date().getFullYear()} TrustBridge AI. All rights reserved.</span>
        <div className="flex gap-4">
          <span>IDBI Bank Partner</span>
          <span>RBI AA Framework Compliant</span>
        </div>
      </div>
    </footer>
  )
}
