import type { NumberSchema } from 'yup'

import type { Employee } from './user.model'

export type MetaData = Record<string, any>

export interface Category {
    id: number
    description: string
    name: string
    short_name: string
}

export interface IEmployee {
    created_by: number
    name: string
    lastname: string
}
export interface Inventory {
    id: number
    created_at: string
    updated_at: string
    deleted_at: string
    quantity: number
    item_id: number
    updated_by_id: number
    warehouse_id: number
    nombreItem: string
    created_at_Item: string
    brandItem: string
    imgItem: string
    ivaItem: number
    modelItem: string
    priceItem: number
    category_id_Item: number
    category_name_Item: string
    status_id_Item: null
    created_by_Item: Maybe<IEmployee>
    codename_Item: string
    is_active: boolean
}

export default {}
