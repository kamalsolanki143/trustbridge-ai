export const GRADE_BANDS = [
  { min: 90, grade: "A+", label: "Exceptional" },
  { min: 80, grade: "A", label: "Strong" },
  { min: 70, grade: "A-", label: "Good" },
  { min: 60, grade: "B", label: "Adequate" },
  { min: 50, grade: "B-", label: "Below Average" },
  { min: 40, grade: "C+", label: "Limited" },
  { min: 30, grade: "C", label: "Weak" },
  { min: 0, grade: "D", label: "Poor" },
] as const

export const GRADE_COLORS: Record<string, string> = {
  "A+": "#10B981", "A": "#10B981", "A-": "#10B981",
  "B": "#F59E0B", "B-": "#F59E0B",
  "C+": "#EF4444", "C": "#EF4444", "D": "#EF4444",
}

export const MOCK_GSTINS = {
  STRONG: "19AABCS1429B1ZX",
  MEDIUM: "24AAACP3415G1ZK",
  WEAK: "27AAAFK2314H1ZM",
}
