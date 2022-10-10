export type SaveItemData = {
    item: number
    quantity: number
}

export interface OrderSaveData {
    warehouse: number
    comment?: string
    items: SaveItemData[]
}

export default {}
