export type SaveItemData = {
    item: number
    quantity: number
}

export interface OrderSaveData {
    warehouse: number
    comment?: string
    items: SaveItemData[]
}


export type OrderDetailsRequestBy={
    name: string
    lastname: string
    cid:string
}

export type OrderDetailsWarehouse={
    name: string
    latitude: string
    longitude:string
}

export type OrderDetailsDetail={
    order_request: number
    item: number
    quantity: number
}

export type OrderDetailsStatus={
    id: number
    created_by: number
    created_at: string
    status: string
}

export interface OrderDetails{
    id:number
    requested_at: string
    requested_by: OrderDetailsRequestBy[]
    warehouse: OrderDetailsWarehouse[]
    comment: string
    details: OrderDetailsDetail[]
    order_status: OrderDetailsStatus[]
}

export type OrderDetailsElements={
    id:any
    warehouse: any
    cantidad: any
    status: any
}

export interface OrderDetails2{
    //orderElements: OrderDetailsElements[]
    id:number
    warehouse: string
    cantidad: number
    status: string
}




export default {}
