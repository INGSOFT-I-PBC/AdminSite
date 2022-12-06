import axios from 'axios'
import { defineStore } from 'pinia'
import type { Warehouse, WarehouseQuery} from './models/warehouseModels'
import type { PaginatedAPIResponse, Item, } from '@store-types'
import type { WhWithTomaFisica } from '@store/types/warehouse.model'
import type { OrderDetails, OrderSaveData } from './types/orders.model'

type QuantifiedItem = Item & { quantity: number }

type identifier = number | string

export interface WarehouseState {
    lastWarehouseList: Optional<Warehouse[]>
    paginatedWarehouse: Optional<PaginatedAPIResponse<Warehouse>>
    lastOrdersWarehouseList: Optional<OrderSaveData[]>
    OrderDetailsList: Optional<OrderDetails[]>
}

export const useWarehouseStore = defineStore('warehouse-store', {
    state: (): WarehouseState => ({
        lastWarehouseList: null,
        paginatedWarehouse: null,
        lastOrdersWarehouseList: null,
        OrderDetailsList: null,
    }),

    getters: {
        getWarehouseList: state => state.lastWarehouseList,
        getPaginatedWarehouse: state => state.paginatedWarehouse,
        getOrdersWarehouseList: state => state.lastOrdersWarehouseList,
        getOrderDetails: state => state.OrderDetailsList,
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
        //FETCH
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
        },

        async fetchOrdersWarehouse(options: Optional<OrderSaveData> = null){
            const result = await(
                await axios.get('/api/v1/list/warehouses/order-requests',
                { params: options}
                )
            ).data

            return result
        },

        async fetchOrdersDetails(idOrder: identifier,options: Optional<OrderDetails> = null){
            const result = await(
                await axios.get(`/api/v1/order-details?id=${idOrder}`,
                { params: options}
                )
            ).data

            return result
        },

       /*
        async fetchOrdersWarehouse(options: Optional<OrderSaveData> = null, paginated_opt:PaginationOptions){
            const queryParams = {...options,page:paginated_opt.page, per_page : paginated_opt.per_page }
            const result = await(
                await axios.get('/api/v1/list/warehouses/order-requests',
                { params: queryParams}
                )
            ).data

            return result
        },
        */

    },
})
