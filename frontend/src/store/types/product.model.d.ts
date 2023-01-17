export type ProductProps = {
    name: string
    value: string
    prod_id?: number
    var_id?: number
}

export type SimpleProduct = {
    id: number
    base_price: number
    product_name: string
    summary: string
    short_description: string
    brand_name: string
}

export type ProductVariant = {
    id: number
    created_at: string
    updated_at: string
    variant_name: string
    sku: string
    price: number
    is_active: boolean
    img?: string
}

export interface VarinatProductI {
    id: number
    created_at: string
    updated_at: string
    deleted_at: string
    variant_name: string
    sku: string
    price: number
    is_active: boolean
    product: SimpleProduct
}

export interface ProductProvider {
    active?: boolean
    price: number
    product: number
    provider: {
        id: number
        name: string
    }
}
