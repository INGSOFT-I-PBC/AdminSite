import type { MetaData } from '@store-types'

import type { Employee } from './user.model'

//export type MetaDataClient = Record<string, any>
export interface Status {
    id: number
    name: string
}

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
    id?: number
    created_at?: string
    updated_at?: string
    deleted_at?: string
    address: string
    business_name: string
    email: string
    phone_number: string
    city: Maybe<City> | null
    province: Maybe<Province> | null
    created_by: Maybe<Employee> | null | number
    gender: Maybe<Gender> | null
    status: number
}

export interface FullClient extends Client {
    meta: Optional<MetaData>
}

export default {}
