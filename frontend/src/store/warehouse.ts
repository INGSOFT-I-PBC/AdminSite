import type {
    MessageResponse,
    PaginatedAPIResponse,
    ProductProps,
    Purchase,
} from '@store-types'
import type {
    FullTomaFisicaDetail,
    Movement,
    TomaFisica,
    TomaFisicaQuery,
    WarehouseStock,
    WhWithTomaFisica,
} from '@store/types/warehouse.model'
import axios, { type AxiosResponse } from 'axios'
import { defineStore } from 'pinia'

import type { Warehouse, WarehouseQuery } from './models/warehouseModels'
import type { ProviderProductDetails, PurchaseOrder } from './types/items.model'
import type {
    OrderDetails,
    OrderSaveData,
    OrderSaveData2,
} from './types/orders.model'

type identifier = number | string

export interface WarehouseState {
    lastWarehouseList: Optional<Warehouse[]>
    paginatedWarehouse: Optional<PaginatedAPIResponse<Warehouse>>
    lastOrdersWarehouseList: Optional<OrderSaveData[]>
    OrderDetailsList: Optional<OrderDetails[]>
    ProviderProductDetails: Optional<ProviderProductDetails[]>
}

export type StockWithProps = WarehouseStock & { props: ProductProps[] }

export const useWarehouseStore = defineStore('warehouse-store', {
    state: (): WarehouseState => ({
        lastWarehouseList: null,
        paginatedWarehouse: null,
        lastOrdersWarehouseList: null,
        OrderDetailsList: null,
        ProviderProductDetails: null,
    }),

    getters: {
        getWarehouseList: state => state.lastWarehouseList,
        getPaginatedWarehouse: state => state.paginatedWarehouse,
        getOrdersWarehouseList: state => state.lastOrdersWarehouseList,
        getOrderDetails: state => state.OrderDetailsList,
        getProductProvider: state => state.ProviderProductDetails,
    },

    actions: {
        async fetchWarehouses(
            options: Optional<WarehouseQuery> = null
        ): Promise<void> {
            const result = await (
                await axios.get<Warehouse[]>('/api/v1/list/warehouses/all', {
                    params: options,
                })
            ).data
            this.lastWarehouseList = result
        },
        confirmPurchaseUser(
            purchase: Purchase
        ): Promise<AxiosResponse<MessageResponse>> {
            return axios.post<MessageResponse>(
                '/api/v1/warehouse/purchase/confirm',
                purchase
            )
        },

        async fetchPaginatedWarehouses(
            options: PaginationOptions
        ): Promise<PaginatedAPIResponse<Warehouse>> {
            const result: PaginatedAPIResponse<Warehouse> = await (
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
        ): Promise<PaginatedAPIResponse<WarehouseStock>> {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            const result: PaginatedAPIResponse<WarehouseStock> = await (
                await axios.get<PaginatedAPIResponse<WarehouseStock>>(
                    '/api/v1/warehouse/stock',
                    { params: queryParams }
                )
            ).data
            return result
        },

        async fetchPaginatedWarehouseTomasFisicas(
            options: any,
            paginated_opt: PaginationOptions
        ): Promise<PaginatedAPIResponse<TomaFisica>> {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            const result: PaginatedAPIResponse<TomaFisica> = await (
                await axios.get<PaginatedAPIResponse<TomaFisica>>(
                    '/api/v1/warehouse/tomas-fisicas',
                    { params: queryParams }
                )
            ).data
            return result
        },

        async fetchPaginatedTomasFisicasDetails(
            options: any,
            paginated_opt: PaginationOptions
        ): Promise<PaginatedAPIResponse<FullTomaFisicaDetail>> {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            const result: PaginatedAPIResponse<FullTomaFisicaDetail> = await (
                await axios.get<PaginatedAPIResponse<FullTomaFisicaDetail>>(
                    '/api/v1/warehouse/tomas-fisicas/details',
                    { params: queryParams }
                )
            ).data
            return result
        },

        async saveTomasFisicas(
            tomaFisica: TomaFisicaQuery
        ): Promise<MessageResponse> {
            const data: MessageResponse = await (
                await axios.post<MessageResponse>(
                    '/api/v1/warehouse/tomas-fisicas',
                    tomaFisica
                )
            ).data

            return data
        },

        async fetchWarehousesLatestTomasFisicas(
            options: Optional<PaginationOptions> = null
        ): Promise<PaginatedAPIResponse<WhWithTomaFisica>> {
            const queryParams = { ...options }
            const result: PaginatedAPIResponse<WhWithTomaFisica> = await (
                await axios.get<PaginatedAPIResponse<WhWithTomaFisica>>(
                    '/api/v1/warehouse/tomas-fisicas/all',
                    { params: queryParams }
                )
            ).data
            return result
        },
        async fetchPaginatedWarehouseMovements(
            options: any,
            paginated_opt: PaginationOptions
        ): Promise<PaginatedAPIResponse<Movement>> {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            const result: PaginatedAPIResponse<Movement> = await (
                await axios.get<PaginatedAPIResponse<Movement>>(
                    '/api/v1/warehouse/movements',
                    { params: queryParams }
                )
            ).data
            return result
        },
        async fetchProductVariantProps(
            options: any,
            paginated_opt: PaginationOptions
        ): Promise<PaginatedAPIResponse<ProductProps>> {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            return (
                await axios.get<PaginatedAPIResponse<ProductProps>>(
                    `/api/v1/products/variant/props`,
                    { params: queryParams }
                )
            ).data
        },
        async fetchStockWithProps(
            options: any,
            paginated_opt: PaginationOptions
        ): Promise<PaginatedAPIResponse<StockWithProps>> {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            return (
                await axios.get<PaginatedAPIResponse<StockWithProps>>(
                    `/api/v1/warehouse/stock-props`,
                    { params: queryParams }
                )
            ).data
        },

        async fetchOrdersWarehouse(
            options: Optional<OrderSaveData> = null,
            busqueda = '',
            filtro = ''
        ) {
            const dato = {
                busqueda: busqueda != '' ? busqueda : '',
                filtro: filtro,
            }
            //datobusqueda = busqueda;

            const result = await (
                await axios.get('/api/v1/list/warehouses/order-requests2', {
                    params: busqueda != '' ? dato : options,
                })
            ).data

            return result
        },

        async fetchOrdersDetails(
            idOrder: identifier,
            options: Optional<OrderDetails> = null,
            busqueda = '',
            filtro = ''
        ) {
            const dato = {
                busqueda: busqueda != '' ? busqueda : '',
                filtro: filtro,
            }

            const result = await (
                await axios.get(`/api/v1/order-details?id=${idOrder}`, {
                    params: busqueda != '' ? dato : options,
                })
            ).data

            return result
        },

        async fetchProviderProduct(prod_id: number) {
            const result = await (
                await axios.get(
                    '/api/v1/list/warehouses/order-product-provider',
                    {
                        params: { prod_id: prod_id },
                    }
                )
            ).data

            return result
        },

        async savePriceToItem(
            options: Optional<OrderSaveData> = null,
            item = '',
            price = ''
        ) {
            const dato = {
                id: item,
                price: price,
            }

            const result = await (
                await axios.get('/api/v1/warehouse/order-savepricetoitem', {
                    params: item != '' ? dato : options,
                })
            ).data

            return result
        },

        async saveQuantityToItem(
            options: Optional<OrderSaveData> = null,
            item = '',
            quantity = ''
        ) {
            const dato = {
                id: item,
                quantity: quantity,
            }

            const result = await (
                await axios.get('/api/v1/warehouse/order-savequantitytoitem', {
                    params: item != '' ? dato : options,
                })
            ).data

            return result
        },

        async approvePurchase(options: Optional<OrderSaveData> = null, id = 0) {
            const dato = {
                order_origin_id: id,
            }

            const result = await (
                await axios.get('/api/v1/warehouse/order-approvePurchase', {
                    params: id == 0 ? dato : options,
                })
            ).data

            return result
        },

        async savePurchaseOrder(order: any) {
            return axios.post<MessageResponse>('/api/v1/purchase/create', order)
        },
    },
})
