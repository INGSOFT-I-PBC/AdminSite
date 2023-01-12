import type { number } from 'yup'

import type { SimpleOrderRequest } from './orders.model'
import type { ProductVariant, SimpleProduct } from './product.model'
import type { Employee } from './user.model'
import type { Warehouse } from './warehouse.model'

export interface MinimalPurchase {
    approved_at: string
    order_origin: SimpleOrderRequest
    reference: number
    status: string
    warehouse?: Warehouse
}

export interface Purchase extends MinimalPurchase {
    id: number
}

export interface PurchaseChild {
    id?: number
    details?: FullPurchaseDetails[]
    img_details?: string
    invoice?: number | { id: number; code: string }
    provider?: { id: number; name: string }
    is_purchased: boolean
    is_delivered: boolean
    purchase_header?: number
    comment?: string
}

export interface PurchaseStatus {
    id?: number
    purchase: number
    created_by: Employee
    created_at: string | Date
    status: string
}

export interface FullPurchase extends MinimalPurchase {
    id?: number
    status_list: PurchaseStatus[]
    childs: PurchaseChild[]
}

export interface FullPurchaseDetails {
    id?: number
    price: number
    product: SimpleProduct
    purchase_child?: number
    quantity: number
    variant: ProductVariant
    provider?: { id: number; name: string }
}

export interface PurchaseQuery {
    approved_date?: boolean
    created_at?: string
    img_details?: string
    from_date?: string
    to_date?: string
    invoice?: number
    order_origin?: number
    provider_name?: number
    purchase_child_id?: number
    purchase_id?: number
    reference?: number
    status_from_date?: string
    status_to_date?: string
    status?: string
    warehouse_id?: number
    warhouse_name?: string
}
