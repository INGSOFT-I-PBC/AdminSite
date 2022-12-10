import type { ProductVariant, SimpleProduct } from './product.model'
import type { Employee } from './user.model'

export interface MinimalWarehouse {
    name: string
    status: { description: string; name: string; id: string }
}

export interface Warehouse extends MinimalWarehouse {
    id: number
}

export interface TomaFisica {
    id: number
    done_by: Maybe<Employee>
    creaed_at: string
    novedad: string
    warehouse: number
}

export interface TomaFisicaDetail {
    id?: number
    toma_fisica?: number
    product: number
    variant: number
    new_stock: number
    previous_stock: number
    novedad: string
}

export interface FullTomaFisicaDetail {
    id?: number
    toma_fisica?: number
    product: Product
    variant: ProductVariant
    new_stock: number
    previous_stock: number
    novedad: string
}

export interface TomaFisicaQuery {
    id?: number
    done_by?: number
    creaed_at?: string
    novedad?: string
    details?: TomaFisicaDetailsPost[]
    warehouse?: number
}

export interface InventoryQuery {
    id?: number
    created_at?: number
    updated_at?: string
    updated_by?: number
    quantity?: number
    item?: number
}

export interface Movement {
    created_at: string
    created_by: Maybe<Employee>
    id: number
    notes: string
    warehouse_origin: {
        id: number
        name: string
    }
    warehouse_destiny: {
        id: number
        name: string
    }
    status: string
}

export interface MovementQuery {
    created_at: string
    created_by: number
    id: number
    notes: string
    warehouse_origin: number
    warehouse_destiny: number
    status: string
}

export interface WhWithTomaFisica {
    id: number
    name: string
    status: string
    whtf_created_at: string
    whtf_done_by_name: string
    whtf_done_by_lastname: string
    whtf_novedad?: string
}

export interface WarehouseStock {
    product: SimpleProduct
    variant: ProductVariant
    updated_by: Employee
    updated_at: string
    stock_level: number
}

export default {}
