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

export type ItemValue = {
    id?: number
    product_name?: string
    price?: string
    brand_name?: string
    variant_name?: string
    created_at?: string
    updated_at?: string
    deleted_at?: string
    sku?: string
    is_active?: boolean
    prod_id?: number
    summary?: string
    short_description?: string
    base_price?: string
}

export interface ProductProvider {
    active?: boolean
    price: string
    product: number
    provider: number
}

export interface Item2 {
    order_request?: number
    item?: ItemValue[]
    quantity?: number
    providerInfo?: ProductProvider
}

export type ProductValues = {
    id?: number
    created_at?: string
    updated_at?: string
    deleted_at?: string
    variant_name?: string
    sku?: string
    price?: string
    is_active?: boolean
    prod_id?: number
    product_name?: string
    brand_name?: string
    sku?: string
    summary?: string
    short_description?: string
    base_price?: string
}

export type ProviderValues = {
    name?: string
    document_path?: string
    bussiness_name?: string
    address?: string
    website?: string
    email?: string
    latitude?: string
    longitude?: string
}

export interface ProviderProductDetails {
    product?: ProductValues[]
    provider?: ProviderValues[]
    price?: string
}

export interface FullItem extends Item {
    meta: Optional<MetaData>
}

export interface ItemProps {
    name: string
    type: string
    value: Optional<string>
}

export type ProductsPurchase = {
    product?: number
    variant?: number
    quantity?: number
    price?: number
}

export interface DetailsOrders {
    provider?: number
    products?: ProductsPurchase[]
}

export interface PurchaseOrder extends DetailsOrders {
    warehouse_id?: number
    order_origin?: number
    details?: DetailsOrders[]
}

export default {}
