from pydantic import BaseModel


class Milestone(BaseModel):
    title: str
    description: str
    impact: str
    timeline: str
    effort: str


class GrowthRoadmapResponse(BaseModel):
    current_grade: str
    target_grade: str
    milestones: list[Milestone]
    progress_percent: float


class ScenarioInput(BaseModel):
    gstin: str
    adjustments: dict


class ScenarioResult(BaseModel):
    projected_score: int
    projected_grade: str
    projected_outcome: str
    delta_score: int
    improvements: list[str]
