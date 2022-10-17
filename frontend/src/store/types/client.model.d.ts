import type { Employee } from './user.model'
import type { MetaData } from '@store-types'

//export type MetaDataClient = Record<string, any>

export interface Gender {
    id: number
    name: string
    short_name: string
}
export interface City {
    id: number
    name: string
    short_name: string
}
export interface Province {
    id: number
    name: string
}

export interface Client {
    number_id: string
    name: string
    id: number
    created_at: string
    updated_at: string
    deleted_at: string
    address: string
    business_name: string
    email: string
    phone_number: string
    city: Maybe<City>
    province: Maybe<Province>
    created_by: Maybe<Employee>
    gender: Maybe<Gender>
    status_id: number
}

export interface FullClient extends Client {
    meta: Optional<MetaData>
}

export default {}
