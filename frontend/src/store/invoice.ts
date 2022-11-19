import { isMessage } from '@/store/types/typesafe'
import type {
    IClient,
    IInventory,
    IItem,
    IPayment,
    Invoice,
    MessageResponse,
    PaginatedAPIResponse,
} from '@store-types'
import type { PaginatedResponse } from '@store-types'
import axios from 'axios'
import { defineStore } from 'pinia'

import { type Ref, computed } from 'vue'

export const useInvoiceStore = defineStore('invoice-store', () => {
    const invoice: Ref<Optional<Invoice>> = ref(null)
    const inventory: Ref<Optional<IInventory>> = ref(null)
    const paginatedInvoice: Ref<Optional<PaginatedAPIResponse<Invoice>>> =
        ref(null)

    const paginatedItems: Ref<Optional<PaginatedAPIResponse<IInventory>>> =
        ref(null)
    const providers = ref<PaginatedResponse<Invoice>>()
    //const providers: Ref<Optional<PaginatedAPIResponse<Invoice>>> = ref(null)

    const currentPaginatedItemPage = computed(() => {
        const pitem = paginatedItems.value
        if (isMessage(pitem)) return undefined
        return pitem?.page
    })
    const currentPaginatedInvoicePage = computed(() => {
        const pitem = paginatedInvoice.value
        if (isMessage(pitem)) return undefined
        return pitem?.page
    })

    const allInvoice: Ref<Optional<Invoice[]>> = ref(null)

    const allPayment: Ref<Optional<IPayment[]>> = ref(null)

    async function fetchAllInvoice() {
        const data = await (
            await axios.get<Invoice[]>('/api/v1/list/invoices/all')
        ).data
        allInvoice.value = data
        return data
    }

    async function fetchClientNumber(number_id: string) {
        return (
            await axios.get<IClient>(
                `/api/v1/invoice/client?number_id=${number_id}`
            )
        ).data
    }

    /**
     * Save the given client into the system.
     *
     * @param item the client to save
     * @returns a response from the backend
     */
    async function saveInvoice(item: Invoice) {
        const data = await (
            await axios.post<MessageResponse>('/api/v1/invoice', item)
        ).data
        return data
    }

    /**
     * Edit the data of an specific Item into the backend.
     *
     * @param id the Id of the item to edit
     * @param data the data to overwrite
     * @returns the response of the backend
     */
    async function editInvoice(id: number, data: Invoice) {
        return (
            await axios.put<Invoice>(`/api/v1/invoice/editar?id=${id}`, data)
        ).data
    }

    /**
     * Delete an specific item from the server.
     *
     * @param id the Id of the item to remove
     * @returns the message of the backend.
     */
    async function removeInvoice(id: number) {
        return (
            await axios.delete<MessageResponse>(
                `/api/v1/invoice/editar?id=${id}`
            )
        ).data
    }

    /**
     * Search an specific client.
     *
     * @param id the Id of the client to search
     * @returns the Item result of the search
     */
    async function fetchInvoiceById(id: number) {
        const data = (
            await axios.get<Invoice>(`/api/v1/invoice/editar?id=${id}`)
        ).data
        invoice.value = data
        return data
    }
    /* async function fetchIInventoryById(id: number) {
        const data = (
            await axios.get<IInventory>(`/api/v1/invoice/details/item?id=${id}`)
        ).data
        inventory.value = data
        return data
    }*/
    async function fetchIInventoryById(id: number) {
        return (
            await axios.get<IInventory>(`/api/v1/invoice/details/item?id=${id}`)
        ).data
    }

    /*async function fetchStatus(name: string) {
        const data = await (
            await axios.get<Status>(`/api/v1/status?name=${name}`)
        ).data
        status.value = data
        return data
    }*/
    async function fetchIItemsPaginated(options: PaginationOptions) {
        const data = await (
            await axios.get<PaginatedAPIResponse<IInventory>>(
                `/api/v1/invoice/item/all`,
                {
                    params: options,
                }
            )
        ).data
        paginatedItems.value = data
        return data
    }

    async function fetchInvoicePaginated(params?: PaginationOptions) {
        const response = (
            await axios.get<PaginatedResponse<Invoice>>(
                '/api/v1/list/invoices/all',
                { params }
            )
        ).data
        paginatedInvoice.value = response
        return response
    }
    /**
     * This method will fetch a paginated list of users that are
     * filtered by the given params.
     *
     * @param params the search params
     */
    async function fetchProviders(params?: PaginationOptions) {
        const response = (
            await axios.get<PaginatedResponse<Invoice>>(
                '/api/v1/list/invoices/all',
                { params }
            )
        ).data
        providers.value = response
        return response
    }

    async function fetchPayment() {
        const data = await (
            await axios.get<IPayment[]>('/api/v1/list/payment/all')
        ).data
        allPayment.value = data
        return data
    }

    return {
        invoice,
        paginatedInvoice,
        paginatedItems,
        allInvoice,
        inventory,
        currentPaginatedItemPage,
        currentPaginatedInvoicePage,
        fetchIInventoryById,
        fetchPayment,
        fetchInvoiceById,
        fetchAllInvoice,
        fetchIItemsPaginated,
        fetchInvoicePaginated,
        saveInvoice,
        editInvoice,
        removeInvoice,
        fetchClientNumber,
        providers,
        fetchProviders,
        //fetchStatus,
    }
})
