import axios from 'axios'
import { defineStore } from 'pinia'
import type { Warehouse, WarehouseQuery} from './models/warehouseModels'
import type { PaginatedAPIResponse, Item, } from '@store-types'
import type { WhWithTomaFisica } from '@store/types/warehouse.model'

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
        async fetchPaginatedWarehouseInventory(options: WarehouseQuery , paginated_opt:PaginationOptions) {
            const queryParams = {...options, page:paginated_opt.page, per_page : paginated_opt.per_page}
            const result = await (
                await axios.get<PaginatedAPIResponse<QuantifiedItem>>(
                    '/api/v1/warehouse/inventory',
                    { params: queryParams }
                )
            )
            return result
        },

        async fetchPaginatedWarehousePurchase(options: WarehouseQuery , paginated_opt:PaginationOptions) {
            const queryParams = {...options, page:paginated_opt.page, per_page : paginated_opt.per_page}
            const result = await (
                await axios.get<PaginatedAPIResponse<any>>(
                    '/api/v1/warehouse/purchase',
                    { params: queryParams }
                )
            )
            return result
        },

        async fetchPaginatedWarehouseTomasFisicas(options: WarehouseQuery , paginated_opt:PaginationOptions) {
            const queryParams = {...options, page:paginated_opt.page, per_page : paginated_opt.per_page}
            const result = await (
                await axios.get<PaginatedAPIResponse<any>>(
                    '/api/v1/warehouse/tomas-fisicas',
                    { params: queryParams }
                )
            )
            return result
        },
        async fetchWarehousesLatestTomasFisicas(options: Optional<PaginationOptions> = null) {
            const queryParams = {...options}
            const result = await (
                await axios.get<WhWithTomaFisica[]>(
                    '/api/v1/warehouse/tomas-fisicas/all',
                    { params: queryParams }
                )
            )
            return result
        }
    },
})
