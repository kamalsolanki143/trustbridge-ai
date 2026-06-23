import type { GrowthRoadmap as GrowthRoadmapType } from "../../types/recommendation"
import MilestoneCard from "./MilestoneCard"
import OutcomePath from "./OutcomePath"

interface GrowthRoadmapProps {
  roadmap: GrowthRoadmapType
}

export default function GrowthRoadmap({ roadmap }: GrowthRoadmapProps) {
  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-[#1E1E2E] bg-[#12121A] p-5">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <p className="text-sm text-[#94A3B8]">Current Grade</p>
            <p className="text-2xl font-bold text-[#F8FAFC]">{roadmap.current_grade}</p>
          </div>
          <div className="text-right">
            <p className="text-sm text-[#94A3B8]">Target Grade</p>
            <p className="text-2xl font-bold text-[#6366F1]">{roadmap.target_grade}</p>
          </div>
        </div>

        <div className="relative h-2 w-full overflow-hidden rounded-full bg-[#1E1E2E]">
          <div
            className="h-full rounded-full bg-[#6366F1] transition-all duration-700"
            style={{ width: `${roadmap.progress_percent}%` }}
          />
        </div>
        <p className="mt-2 text-xs text-[#94A3B8]">
          {roadmap.progress_percent}% progress toward {roadmap.target_grade}
        </p>
      </div>

      <div className="space-y-3">
        <h3 className="text-sm font-medium text-[#F8FAFC]">Milestones</h3>
        {roadmap.milestones.map((milestone, i) => (
          <MilestoneCard key={i} milestone={milestone} index={i} />
        ))}
      </div>

      <OutcomePath currentGrade={roadmap.current_grade} targetGrade={roadmap.target_grade} />
    </div>
  )
}
