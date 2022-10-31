import type {
    APIResponse,
    Invoice,
    IClient,
    MessageResponse,
    PaginatedAPIResponse,
} from '@store-types'
import { isMessage } from '@/store/types/typesafe'
import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, type Ref } from 'vue'

export const useInvoiceStore = defineStore('invoice-store', () => {
    const invoice: Ref<Optional<Invoice>> = ref(null)
    const paginatedInvoice: Ref<Optional<PaginatedAPIResponse<Invoice>>> =
        ref(null)
    const currentPaginatedInvoicePage = computed(() => {
        const pitem = paginatedInvoice.value
        if (isMessage(pitem)) return undefined
        return pitem?.page
    })

    const allInvoice: Ref<Optional<Invoice[]>> = ref(null)

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

    async function fetchInvoicePaginated(options: PaginationOptions) {
        const data = await (
            await axios.get<PaginatedAPIResponse<Invoice>>(
                '/api/v1/list/items',
                {
                    params: options,
                }
            )
        ).data
        paginatedInvoice.value = data
        return data
    }

    /**
     * Save the given client into the system.
     *
     * @param item the client to save
     * @returns a response from the backend
     */
    async function saveInvoice(item: Invoice) {
        const data = await (
            await axios.post<MessageResponse>('/api/v1/clients', item)
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
        return (await axios.put<Invoice>(`/api/v1/clients?id=${id}`, data)).data
    }

    /**
     * Delete an specific item from the server.
     *
     * @param id the Id of the item to remove
     * @returns the message of the backend.
     */
    async function removeInvoice(id: number) {
        return (await axios.delete<MessageResponse>(`/api/v1/clients?id=${id}`))
            .data
    }

    /**
     * Search an specific client.
     *
     * @param id the Id of the client to search
     * @returns the Item result of the search
     */
    async function fetchInvoiceById(id: number) {
        return (await axios.get<Invoice>(`/api/v1/clients?id=${id}`)).data
    }

    /*async function fetchStatus(name: string) {
        const data = await (
            await axios.get<Status>(`/api/v1/status?name=${name}`)
        ).data
        status.value = data
        return data
    }*/

    return {
        invoice,
        paginatedInvoice,
        allInvoice,
        currentPaginatedInvoicePage,
        fetchInvoiceById,
        fetchAllInvoice,
        fetchInvoicePaginated,
        saveInvoice,
        editInvoice,
        removeInvoice,
        fetchClientNumber,
        //fetchStatus,
    }
})
