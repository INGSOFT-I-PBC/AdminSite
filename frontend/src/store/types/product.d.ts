interface AttributeHolder {
    attributes: ProductAttribute[]
}

interface BaseProduct extends AttributeHolder {
    product_name: string
    summary: string
    short_description: string
    brand_name: string
    base_price: string
}

interface BaseProductVariant extends AttributeHolder {
    variant_name: string
    sku: string
    price: string
    stock_level: number
}

export interface VariantCreateForm extends Partial<AttributeHolder> {
    variant_name: string
    price: string
}

export interface ProductCreationForm
    extends Partial<AttributeHolder>,
        BaseProduct {
    variants?: VariantCreateForm[]
}

export interface ProductAttribute {
    name: string
    value: string
    type: string
}

// TODO: complete this type
export interface ProductCategory {
    name: string
}

export type ProductSearchOptions = Partial<{
    name: string
}>

export interface Product extends BaseProduct {
    id: number
    variants: ProductVariant[]
    created_at: string
    created_by: number
}

export interface SimpleProductStock {
    readonly warehouse: number
    readonly warehouse_name: string
    readonly product: number
    readonly variant: number
    readonly stock_level: number
    readonly updated_by: number
}

export interface ProductVariant extends BaseProductVariant {
    id: number
    img: string | null
    upc: string | null
    ean: string | null
}

export interface BCProductVariant extends ProductVariant {
    product_name: string
    summary: string
    brand_name: string
    short_description: string
}
