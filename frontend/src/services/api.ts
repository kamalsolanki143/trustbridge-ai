const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

interface ApiError {
  detail: string
}

export class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl
  }

  private async request<T>(path: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${path}`
    const res = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
      ...options,
    })

    if (!res.ok) {
      let error: ApiError
      try {
        error = await res.json()
      } catch {
        error = { detail: `HTTP ${res.status}: ${res.statusText}` }
      }
      throw new Error(error.detail || "API request failed")
    }

    return res.json()
  }

  async get<T>(path: string): Promise<T> {
    return this.request<T>(path)
  }

  async post<T>(path: string, body: unknown): Promise<T> {
    return this.request<T>(path, {
      method: "POST",
      body: JSON.stringify(body),
    })
  }
}

export const api = new ApiClient()
