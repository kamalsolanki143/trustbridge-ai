export interface MSME {
  id: string
  business_name: string
  owner_name: string
  business_type: string | null
  address: string | null
  city: string | null
  state: string | null
  gstin: string
  email: string | null
  phone: string | null
  created_at: string
  updated_at: string
}

export interface DataSource {
  source_type: string
  connected: boolean
  connected_at: string | null
}

export interface ConsentGrantRequest {
  msme_id: string
  data_sources: string[]
  purpose: string
}

export interface ConsentRecord {
  id: string
  msme_id: string
  consent_token: string
  data_sources: string[]
  purpose: string
  status: string
  granted_at: string
  expires_at: string | null
}
