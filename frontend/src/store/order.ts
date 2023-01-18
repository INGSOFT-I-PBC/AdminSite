import type { PaginatedAPIResponse, PaginatedResponse } from '@store-types'
import type { MessageResponse } from '@store/types'
import type {
    FullOrderDetail,
    OrderDetailQuery,
    OrderQuery,
    OrderRequest,
    OrderRequestDetail,
    OrderRequestInfo,
    OrderSaveData,
    OrderStatus,
    RawOrderRequest,
    SimpleOrderRequest,
    SimpleOrderStatus,
} from '@store/types/orders.model'
import axios from 'axios'
import { defineStore } from 'pinia'

type OrderSearchParams = {
    order_id: number
    comment: string
}

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
    async function fetchRequests(
        params?: PaginationOptions & Partial<OrderSearchParams>
    ): Promise<PaginatedAPIResponse<SimpleOrderStatus>> {
        const data = (
            await axios.get<PaginatedResponse<SimpleOrderStatus>>(
                '/api/v1/order/status',
                { params }
            )
        ).data

        return data
    }

    /**
     * This function would fetch the data for the order requests on a
     * pagination mode.
     *
     * @param params the search params used for this route
     */
    async function fetchOrderRequests(
        params?: PaginationOptions & Partial<OrderSearchParams>
    ) {
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

    async function fetchStatus(query: OrderQuery) {
        const data = (
            await axios.get<SimpleOrderStatus[] | MessageResponse>(
                '/api/v1/order/status',
                { params: query }
            )
        ).data
        return data
    }

    async function fetchOrdersDetails(options: OrderDetailQuery) {
        const result = await (
            await axios.get<FullOrderDetail[] | MessageResponse>(
                `/api/v1/order/details`,
                {
                    params: options,
                }
            )
        ).data

        return result
    }

    async function fetchOrdersRequestWithInfo(
        options: Optional<OrderQuery> & PaginationOptions
    ) {
        const result = await (
            await axios.get<PaginatedAPIResponse<OrderRequestInfo>>(
                '/api/v1/list/warehouses/order-requests2',
                {
                    params: options,
                }
            )
        ).data

        return result
    }

    async function rejectOrderRequest(order_id: number) {
        return (
            await axios.put<MessageResponse>('/api/v1/order/reject', {
                id: order_id,
            })
        ).data
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
        fetchOrderRequests,
        fetchStatus,
        fetchOrdersRequestWithInfo,
        fetchOrdersDetails,
        rejectOrderRequest,
    }
})
