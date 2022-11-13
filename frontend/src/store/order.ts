import type { PaginatedResponse } from '@store-types'
import type { MessageResponse } from '@store/types'
import type { OrderRequest, OrderSaveData } from '@store/types/orders.model'
import axios from 'axios'
import { defineStore } from 'pinia'

export const useOrderStore = defineStore('orders', () => {
    const order = ref<OrderRequest>()
    const orderRequests = ref<PaginatedResponse<OrderRequest>>()
    async function saveOrder(order: OrderSaveData) {
        return axios.post<MessageResponse>('/api/v1/order', order)
    }

    /**
     * This function search a specific order and return all its detailed data.
     *
     * @param id The id of the desired order request
     */
    async function fetchOrder(id: number) {
        const data = (
            await axios.get<OrderRequest>(`/api/v1/detailed/order/${id}`)
        ).data
        order.value = data

        return data
    }

    /**
     * This function returns a paginated list of Order Requests
     * @param params the search params for this route
     */
    async function fetchRequests(params: PaginationOptions) {
        const data = (
            await axios.get<PaginatedResponse<OrderRequest>>(
                '/api/v1/list/warehouses/order-requests',
                { params }
            )
        ).data
        orderRequests.value = data
        return data
    }

    return {
        orderRequests,
        order,
        saveOrder,
        fetchRequests,
        fetchOrder,
    }
})
