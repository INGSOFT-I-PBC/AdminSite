import type { FullPurchaseDetails, Purchase, PurchaseQuery } from '@store-types'
import type {
    FullPurchase,
    MessageResponse,
    PaginatedAPIResponse,
} from '@store/types'
import axios from 'axios'
import { defineStore } from 'pinia'

import type { SaveOrderDetail } from './types/orders.model'

/**
 * Names of the status for puchase registered in the database
 */

export type PurchaseFromOrderData = {
    warehouse_id: number
    order_origin: number
    details: { provider: number; products: SaveOrderDetail[] }[]
}

const APROVED_STATUS = { name: 'aprobado', display: 'Aprobado' }
const DELIVERED_STATUS = { name: 'entregado', display: 'Entregado' }
const TRANSIT_STATUS = { name: 'transito', display: 'En Tránsito' }
const CANCELED_STATUS = { name: 'cancelado', display: 'Cancelado' }
const RETURNED_STATUS = { name: 'rechazado', display: 'Rechazado' }
const PAYED_STATUS = { name: 'pagado', display: 'Pago Completo' }

const valid_status = [
    APROVED_STATUS,
    DELIVERED_STATUS,
    CANCELED_STATUS,
    TRANSIT_STATUS,
    RETURNED_STATUS,
    PAYED_STATUS,
]

export interface PurchaseState {
    lastPurchaseList: Optional<Purchase[]>
    paginatedPurchase: Optional<PaginatedAPIResponse<Purchase>>
}

export const usePurchaseStore = defineStore('purchases-store', {
    state: (): PurchaseState => ({
        lastPurchaseList: null,
        paginatedPurchase: null,
    }),

    getters: {
        getPurchaseList: state => state.lastPurchaseList,
        getPaginatedPurchase: state => state.paginatedPurchase,
    },

    actions: {
        getPurchaseStatus() {
            return valid_status
        },

        async fetchPaginatedPurchases(
            options: PurchaseQuery,
            paginated_opt: PaginationOptions
        ): Promise<PaginatedAPIResponse<Purchase>> {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            const result = await (
                await axios.get<PaginatedAPIResponse<Purchase>>(
                    '/api/v1/warehouse/purchase',
                    { params: queryParams }
                )
            ).data
            this.paginatedPurchase = result
            return result
        },

        async fetchPurchaseInformation(
            options: PurchaseQuery,
            paginated_opt: PaginationOptions
        ): Promise<PaginatedAPIResponse<FullPurchase>> {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            const result = await (
                await axios.get<PaginatedAPIResponse<FullPurchase>>(
                    '/api/v1/purchase',
                    { params: queryParams }
                )
            ).data
            return result
        },

        async fetchPurchaseDetails(
            options: PurchaseQuery
        ): Promise<FullPurchaseDetails[] | MessageResponse> {
            const result = await (
                await axios.get<FullPurchaseDetails[] | MessageResponse>(
                    '/api/v1/purchase/details',
                    { params: options }
                )
            ).data
            return result
        },

        async savePurchaseFromOrder(order: PurchaseFromOrderData) {
            return axios.post<MessageResponse>('/api/v1/purchase/create', order)
        },
    },
})
