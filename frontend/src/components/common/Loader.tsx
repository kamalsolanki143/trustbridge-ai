export default function Loader({ text = "Loading..." }: { text?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-20">
      <div className="h-8 w-8 animate-spin rounded-full border-2 border-[#1E1E2E] border-t-[#6366F1]" />
      <p className="text-sm text-[#94A3B8]">{text}</p>
    </div>
  )
}
