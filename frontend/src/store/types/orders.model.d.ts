import type { Item } from './items.model'
import type { Employee } from './user.model'

export type SaveItemData = {
    item: number
    quantity: number
}

export interface OrderSaveData {
    warehouse: number
    comment?: string
    items: SaveItemData[]
}

export interface OrderSaveData2 {
    id?: number
    warehouse?: string
    requested_at?: string
    requested_by?: string
}

export interface IOrderDetail {
    id?: number
    item: Item
    quantity: number
}

export interface IOrder {
    id: number
    requested_by: Employee
    warehouse: Warehouse
    details: IOrderDetail
    revised_by: Optional<Employee>
    comment: string
}

export interface RawOrderRequest {
    requested_by: number
    requested_at: string
    warehouse: number
    comment: string
    status: OrderRequestStatus
}

/**
 * This object is the detail that belongs to an Order Request, contains
 * all the information about the basic data of the item requested.
 */
export interface OrderRequestDetail {
    /**
     * The item that this record makes reference.
     */
    readonly item_name: string
    /**
     * The brand name in which the item belongs to
     */
    readonly item_brand: string
    /**
     * The category name that this items belongs to
     */
    readonly item_category: string
    /**
     * The quantity of items that this records request
     */
    readonly quantity: number
}

/**
 * The current status of the order request, its a enumeration of strings
 */
export type OrderRequestStatus = 'PA' | 'AP' | 'CR' | 'NG' | 'CR' | 'CN'

/**
 * This object represent all the needed information that an order request has
 * contains all the items and the information of the employee that has created it,
 * and information of the items attached on it.
 */
export interface OrderRequest {
    /**
     * The id of the Order Request
     */
    id: number
    requested_by: Employee
    approved_by: Optional<Employee>
    approved_at: Optional<string | Date>
    items: OrderRequestDetail[]
    warehouse: string
    requested_at: string | Date
    comment: string
    status: OrderRequestStatus
}

export type OrderDetailsRequestBy = {
    name: string
    lastname: string
    cid: string
}

export type OrderDetailsWarehouse = {
    name: string
    latitude: string
    longitude: string
}

export type OrderDetailsDetail = {
    order_request: number
    item: number
    quantity: number
}

export type OrderDetailsStatus = {
    id: number
    created_by: number
    created_at: string
    status: string
}

export interface OrderDetails {
    id: number
    requested_at: string
    requested_by: OrderDetailsRequestBy[]
    warehouse: OrderDetailsWarehouse[]
    comment: string
    details: OrderDetailsDetail[]
    order_status: OrderDetailsStatus[]
}

export interface OrderDetails2 {
    //orderElements: OrderDetailsElements[]
    id: number
    warehouse: string
    cantidad: number
    status: string
}

export default {}
