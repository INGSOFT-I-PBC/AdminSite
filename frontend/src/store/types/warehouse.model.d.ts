import type { ProductVariant, SimpleProduct } from './product.model'
import type { Employee } from './user.model'

export interface MinimalWarehouse {
    name: string
    status: { description: string; name: string; id: string }
}

export interface Warehouse extends MinimalWarehouse {
    id: number
    latitude?: number
    longitude?: number
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
    acepted: string
    acepted_by?: Maybe<Employee>
}

export interface TomaSaveData {
    id: number
    warehouse_id: number
    new_stock: number
    previous_stock: number
    product: number
    variant: number
    acepted: string
    acepted_comment?: string
}

export interface FullTomaFisicaDetail {
    id?: number
    toma_fisica?: number
    product: Product
    variant: ProductVariant
    new_stock: number
    previous_stock: number
    novedad: string
    acepted: string
    acepted_by: Maybe<Employee>
    warehouse_stock?: numebr
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
    created_at?: string
    created_by?: number
    created_by_name?: string
    transaction_id?: number
    id?: number
    notes?: string
    warehouse_origin?: number
    warehouse_destiny?: number
    from_date?: string
    to_date?: string
    status?: string
    status_from_date?: string
    status_to_date?: string
}

export interface MovementStatus {
    id?: number
    created_at: string | Date
    created_by: Maybe<Employee>
    status: string
    transaction?: number
}

export interface MovementDetail {
    id?: number
    quantity: number
    header?: number
    product: SimpleProduct
    variant: ProductVariant
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
    updated_by?: Employee
    updated_at?: string
    stock_level: number
    is_active?: number
    warehouse?: number
}

export interface MovementSaveData {
    notes: string
    details: MovementDetail[]
    warehouse_destiny: number
    warehouse_origin: number
}

export default {}
