import type {
    Item,
    MessageResponse,
    PaginatedAPIResponse,
    Purchase,
} from '@store-types'
import type {
    Movement,
    TomaFisica,
    WhWithTomaFisica,
} from '@store/types/warehouse.model'
import axios from 'axios'
import { defineStore } from 'pinia'

import type { Warehouse, WarehouseQuery } from './models/warehouseModels'

type QuantifiedItem = Item & { quantity: number }

export interface WarehouseState {
    lastWarehouseList: Optional<Warehouse[]>
    paginatedWarehouse: Optional<PaginatedAPIResponse<Warehouse>>
}

export const useWarehouseStore = defineStore('warehouse-store', {
    state: (): WarehouseState => ({
        lastWarehouseList: null,
        paginatedWarehouse: null,
    }),

    getters: {
        getWarehouseList: state => state.lastWarehouseList,
        getPaginatedWarehouse: state => state.paginatedWarehouse,
    },

    actions: {
        async fetchWarehouses(options: Optional<WarehouseQuery> = null) {
            const result = await (
                await axios.get<Warehouse[]>('/api/v1/list/warehouses/all', {
                    params: options,
                })
            ).data
            this.lastWarehouseList = result
        },
        confirmPurchaseUser(purchase: Purchase) {
            return axios.post<MessageResponse>(
                '/api/v1/warehouse/purchase/confirm',
                purchase
            )
        },

        async fetchPaginatedWarehouses(options: PaginationOptions) {
            const result = await (
                await axios.get<PaginatedAPIResponse<Warehouse>>(
                    '/api/v1/list/warehouses',
                    { params: options }
                )
            ).data
            this.paginatedWarehouse = result
            return result
        },
        async fetchPaginatedWarehouseInventory(
            options: any,
            paginated_opt: PaginationOptions
        ) {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            const result = await axios.get<
                PaginatedAPIResponse<QuantifiedItem>
            >('/api/v1/warehouse/inventory', { params: queryParams })
            return result
        },

        async fetchPaginatedWarehousePurchase(
            options: any,
            paginated_opt: PaginationOptions
        ) {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            const result = await await axios.get<
                PaginatedAPIResponse<Purchase>
            >('/api/v1/warehouse/purchase', { params: queryParams })
            return result
        },

        async fetchPaginatedWarehouseTomasFisicas(
            options: any,
            paginated_opt: PaginationOptions
        ) {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            const result = await axios.get<PaginatedAPIResponse<TomaFisica>>(
                '/api/v1/warehouse/tomas-fisicas',
                { params: queryParams }
            )
            return result
        },
        async fetchWarehousesLatestTomasFisicas(
            options: Optional<PaginationOptions> = null
        ) {
            const queryParams = { ...options }
            const result = await await axios.get<WhWithTomaFisica[]>(
                '/api/v1/warehouse/tomas-fisicas/all',
                { params: queryParams }
            )
            return result
        },
        async fetchPaginatedWarehouseMovements(
            options: any,
            paginated_opt: PaginationOptions
        ) {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            const result = await axios.get<PaginatedAPIResponse<Movement>>(
                '/api/v1/warehouse/movements',
                { params: queryParams }
            )
            return result
        },
    },
})
