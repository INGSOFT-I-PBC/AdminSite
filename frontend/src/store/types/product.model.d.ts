export type ProductProps = {
    name: string
    value: string
    prod_id?: number
    var_id?: number
}

export type Product = {
    id: number
    base_price: number
    sku: string
    updated_at: string
    product_name: string
    variant_name: string
    price: number
    summary: string
    short_description: string
    brand_name: string
}
