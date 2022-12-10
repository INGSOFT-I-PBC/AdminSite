import type { ProductVariant, SimpleProduct } from './product.model'

export interface MinimalPurchase {
    img_details: string
    aproved_at: string
    invoice: {
        id: number
        code: string
    }
    provider: {
        id: number
        name: string
    }
    order_origin: number
    reference: number
    warehouse: number
    status: string
}

export interface Purchase extends MinimalPurchase {
    id: number
}

export interface FUllPurchaseDetails {
    id?: number
    price: number
    quantity: number
    purchase: number
    product: SimpleProduct
    variant: ProductVariant
}

export interface PurchaseQuery {
    img_details?: string
    created_at?: string
    invoice?: number
    provider?: number
    order_origin?: number
    reference?: number
    warehouse?: number
    status?: number
}

export default {}
