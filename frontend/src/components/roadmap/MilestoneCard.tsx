import type { Milestone } from "../../types/recommendation"

interface MilestoneCardProps {
  milestone: Milestone
  index: number
}

export default function MilestoneCard({ milestone, index }: MilestoneCardProps) {
  return (
    <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-4 transition-colors hover:border-[#6366F1]/50">
      <div className="flex items-start gap-3">
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#6366F1]/10 text-sm font-bold text-[#6366F1]">
          {index + 1}
        </div>
        <div className="flex-1">
          <h4 className="text-sm font-medium text-[#F8FAFC]">{milestone.title}</h4>
          <p className="mt-1 text-xs text-[#94A3B8]">{milestone.description}</p>
          <div className="mt-2 flex flex-wrap gap-2">
            <span className="rounded bg-[#10B981]/10 px-2 py-0.5 text-xs text-[#10B981]">
              Impact: {milestone.impact}
            </span>
            <span className="rounded bg-[#F59E0B]/10 px-2 py-0.5 text-xs text-[#F59E0B]">
              {milestone.timeline}
            </span>
            <span className="rounded bg-[#6366F1]/10 px-2 py-0.5 text-xs text-[#6366F1]">
              Effort: {milestone.effort}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
