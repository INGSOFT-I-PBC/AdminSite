export interface MinimalWarehouse {
    name: string
    status: { description: string; name: string; id: string }
}

export interface Warehouse extends MinimalWarehouse {
    id: number
}

export type WarehouseQuery = {
    name?: string
    id?: number
    latitud?: number
    longitud?: number
}

export const a = 'a'
