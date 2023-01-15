import type { Employee } from './user.model'

export interface ProviderModel {
    name: string
    document_path: string
    bussiness_name: string
    phone_no: string
    website: Optional<string>
    email: string
    address: string
    latitude: string
    longitude: string
}

export interface Provider extends ProviderModel {
    id: number
    is_active: boolean
    created_by: number
    created_at: string
}
export interface ProviderForm {
    name?: string
    document_path?: string
    bussiness_name?: string
    phone_no?: string
    website?: Optional<string>
    email?: string
    latitude?: number | string
    longitude?: number | string
}
