import type { Item } from './items.model'
import type { Employee } from './user.model'

export interface MinimalWarehouse {
    name: string
    status: { description: string; name: string; id: string }
}

export interface Warehouse extends MinimalWarehouse {
    id: number
}

export interface BaseBarcodeModel {
    batch_no: string
    expiration_date: string | null
    quantity: number
    stock_code: string
}

export interface BarcodeModel extends BaseBarcodeModel {
    id: number
    warehouse: number
    item: number
}

export interface FullBarcodeModel extends BaseBarcodeModel {
    warehouse: Warehouse
    item: Item
}

export interface TomaFisica {
    id: number
    done_by: Maybe<Employee>
    creaed_at: string
    novedad: string
    warehouse: number
}

export interface TomaFisicaQuery {
    id?: number
    done_by?: number
    creaed_at?: string
    novedad?: string
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

export default {}
