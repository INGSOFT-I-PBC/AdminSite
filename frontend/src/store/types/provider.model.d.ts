export interface ProviderModel {
    name: string
    document_path: string
    bussiness_name: string
    phone_no: string
    website: Optional<string>
    email: string
    latitude: string
    longitude: string
}

export interface Provider extends ProviderModel {
    id: number
    status: number
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
