import { isMessage } from '@/store/types/typesafe'
import type {
    CreditNote,
    EditCreditNoteInvoice,
    IClient,
    IEditInventory,
    IInventory,
    IPayment,
    Invoice,
    MessageResponse,
    PaginatedAPIResponse,
} from '@store-types'
import type { PaginatedResponse } from '@store-types'
import axios from 'axios'
import { defineStore } from 'pinia'

import { type Ref, computed } from 'vue'

export const useCreditNoteStore = defineStore('creditnote-store', () => {
    const invoice: Ref<Optional<CreditNote>> = ref(null)
    const inventory: Ref<Optional<IInventory>> = ref(null)
    const paginatedInvoice: Ref<Optional<PaginatedAPIResponse<CreditNote>>> =
        ref(null)
    const paginatedCreditNote = ref<PaginatedResponse<CreditNote>>() // Ref<Optional<PaginatedAPIResponse<Invoice>>> =
    // ref(null)

    const paginatedItems: Ref<Optional<PaginatedAPIResponse<IInventory>>> =
        ref(null)

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

    async function fetchPaginatedListCreditNote(
        options: any,
        paginated_opt: PaginationOptions
    ) {
        const queryParams = {
            ...options,
            page: paginated_opt.page,
            per_page: paginated_opt.per_page,
        }
        const response = (
            await axios.get<PaginatedResponse<CreditNote>>(
                '/api/v1/creditnotes',
                {
                    params: queryParams,
                }
            )
        ).data
        paginatedCreditNote.value = response
        return response
    }

    async function getAllInvoice() {
        return await axios.get<CreditNote[]>('/api/v1/list/invoice', {})
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
    async function saveCreditNote(item: CreditNote): Promise<any> {
        const data = (
            await axios.post<MessageResponse>('/api/v1/save/creditnote', item)
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
    async function editCreditNoteInvoice(
        id: number,
        data: EditCreditNoteInvoice
    ) {
        return (
            await axios.put<CreditNote>(
                `/api/v1/edit/creditnote/invoice?id=${id}`,
                data
            )
        ).data
    }

    /**
     * Edit the data of an specific Item into the backend.
     *
     * @param id the Id of the item to edit
     * @param data the data to overwrite
     * @returns the response of the backend
     */
    async function editquantityInventory(id: number, data: IEditInventory) {
        return (
            await axios.put<IEditInventory>(
                `/api/v1/invoice/quantity?id=${id}`,
                data
            )
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
            await axios.get<CreditNote>(`/api/v1/invoice/editar?id=${id}`)
        ).data
        invoice.value = data
        return data
    }

    async function fetchIInventoryById(id: number) {
        return (
            await axios.get<IInventory>(`/api/v1/invoice/details/item?id=${id}`)
        ).data
    }

    async function fetchIItemsPaginated(options: PaginationOptions) {
        const data = await (
            await axios.get<PaginatedAPIResponse<IInventory>>(
                `/api/v1/invoice/product-inventory`,
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
            await axios.get<PaginatedResponse<CreditNote>>(
                '/api/v1/list/invoices/all',
                { params }
            )
        ).data
        paginatedInvoice.value = response
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
        paginatedCreditNote,
        paginatedItems,
        allInvoice,
        inventory,
        currentPaginatedItemPage,
        currentPaginatedInvoicePage,
        fetchPaginatedListCreditNote,
        fetchIInventoryById,
        getAllInvoice,
        editquantityInventory,
        fetchPayment,
        fetchInvoiceById,
        fetchIItemsPaginated,
        fetchInvoicePaginated,
        saveCreditNote,
        editCreditNoteInvoice,
        removeInvoice,
        fetchClientNumber,
    }
})
