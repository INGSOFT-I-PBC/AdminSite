export interface ProviderModel {
    name: string
    document_path: string
    bussiness_name: string
    phone_no: string
    website:Optional<string>
    email: string
    latitude: number
    longitude: number
}

export interface Provider extends ProviderModel {
    id: number
}
export interface ProviderForm {
    name?: string
    document_path?: string
    bussiness_name?: string
    phone_no?: string
    website?:Optional<string>
    email?: string
    latitude?: number
    longitude?: number
}
