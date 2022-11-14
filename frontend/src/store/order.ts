import type { PaginatedResponse } from '@store-types'
import type { MessageResponse } from '@store/types'
import type {
    OrderRequest,
    OrderSaveData,
    RawOrderRequest,
} from '@store/types/orders.model'
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

    /**
     * This function will make a partial update of a given order request, and
     * would return the response message of the API server.
     *
     * @param target the id of the target Order Request
     * @param data The partial data to update
     * @see RawOrderRequest to view the fields that are allowed to update
     */
    async function partialUpdate(
        target: number,
        data: Partial<RawOrderRequest>
    ) {
        return (
            await axios.patch<MessageResponse>(`/api/v1/order/${target}`, data)
        ).data
    }
    /**
     * This function is a 'safe-way' to approve an {@link OrderRequest}, behind the scenes
     * this is a shortcut of {@link partialUpdate}.
     *
     * @param target The id of the target {@link OrderRequest}
     */
    async function approveOrderRequest(target: number) {
        return partialUpdate(target, { status: 'AP' })
    }

    /**
     * This function is a 'safe-way' to deny or disapprove an {@link OrderRequest}, behind
     * scenes this function is a shortcut of {@link partialUpdate}.
     *
     * @param target The id of the target {@link OrderRequest}
     */
    async function denyOrderRequest(target: number) {
        return partialUpdate(target, { status: 'NG' })
    }

    return {
        orderRequests,
        order,
        saveOrder,
        fetchRequests,
        fetchOrder,
        partialUpdate,
        approveOrderRequest,
        denyOrderRequest,
    }
})
