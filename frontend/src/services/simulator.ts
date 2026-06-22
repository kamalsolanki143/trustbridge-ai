import { api } from "./api"
import type { ScenarioInput, ScenarioResult } from "../types/recommendation"

export async function runScenario(data: ScenarioInput): Promise<ScenarioResult> {
  return api.post<ScenarioResult>("/api/simulator/run", data)
}
