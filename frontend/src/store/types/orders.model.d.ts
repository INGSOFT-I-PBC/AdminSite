import type { Item } from './items.model'
import { type ProductProvider, VarinatProductI } from './product.model'
import type { Employee } from './user.model'
import { Warehouse } from './warehouse.model'

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
    revised_by: Optional<Employee>
    revised_at: Optional<string | Date>
    items: OrderRequestDetail[]
    warehouse: string
    requested_at: string | Date
    comment: string
    status: OrderRequestStatus
}

export type FullOrderDetail = {
    order_request: number
    item: VarinatProductI
    quantity: number
    providerInfo: ProductProvider[]
}

export type SaveOrderDetail = {
    variant: number
    product: number
    price: number
    quantity: number
}

export type OrderStatus = {
    id: number
    created_by: number
    created_at: string
    status: string
}

export interface OrderRequestInfo {
    id: number
    requested_at: string
    requested_by: Maybe<Employee>
    warehouse: Warehouse
    comment: string
    status: string
    revised_by: Maybe<Employee>
    revised_at?: string
}

export interface SimpleOrderStatus {
    id?: number
    created_by: Employee
    created_at: string | Date
    status: string
}

export interface OrderDetailQuery {
    order_id?: number
    item_name?: string
}

export interface OrderQuery {
    id?: number
    warehouse_id?: number
    requested_by_name?: string
}

export interface SimpleOrderRequest {
    id: number
    requested_at: string | Date
    revised_by?: Employee
    revised_at?: string | Date
    comment?: string
    status_list?: SimpleOrderStatus[]
}

export default {}
