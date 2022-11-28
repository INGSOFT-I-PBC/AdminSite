import type { Item } from './items.model'

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

export default {}
