import type { Employee } from './user.model'

export type MetaData = Record<string, any>

export interface Category {
    id: number
    description: string
    name: string
    short_name: string
}

export interface Item {
    id: number
    brand: string
    category: Maybe<Category>
    created_by: Maybe<Employee>
    img: string
    iva: number
    model: string
    name: string
    price: number
    codename: string
}

export interface FullItem extends Item {
    meta: Optional<MetaData>
}

export interface ItemProps {
    name: string
    type: string
    value: Optional<string>
}

export default {}
