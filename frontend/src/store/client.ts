import type {
    APIResponse,
    Client,
    MessageResponse,
    PaginatedAPIResponse,
} from '@store-types'
import { isMessage } from '@/store/types/typesafe'
import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, type Ref } from 'vue'

export const useClientStore = defineStore('client-store', () => {
    const client: Ref<Optional<Client>> = ref(null)
    const paginatedClient: Ref<Optional<PaginatedAPIResponse<Client>>> = ref(null)
    const currentPaginatedClientPage = computed(() => {
        const pitem = paginatedClient.value
        if (isMessage(pitem)) return undefined
        return pitem?.page
    })

    const allClient: Ref<Optional<Client[]>> = ref(null)

    async function fetchAllClient() {
        const data = await (await axios.get<Client[]>('/api/v1/list/clients/all')).data
        allClient.value = data
        return data
    }

    async function fetchClientPaginated(options: PaginationOptions) {
        const data = await (
            await axios.get<PaginatedAPIResponse<Client>>('/api/v1/list/items', {
                params: options,
            })
        ).data
        paginatedClient.value = data
        return data
    }

    /**
     * Save the given item into the system.
     *
     * @param item the item to save
     * @returns a response from the backend
     */
    async function saveClient(item: Client) {
        const data = await (
            await axios.post<MessageResponse>('/api/v1/item', item)
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
    async function editClient(id: number, data: Client) {
        return (await axios.put<APIResponse<Client>>(`/api/v1/item/${id}`, data))
            .data
    }

    /**
     * Delete an specific item from the server.
     *
     * @param id the Id of the item to remove
     * @returns the message of the backend.
     */
    async function removeClient(id: number) {
        return (await axios.delete<MessageResponse>(`/api/v1/item/${id}`)).data
    }

    /**
     * Search an specific item.
     *
     * @param id the Id of the item to search
     * @returns the Item result of the search
     */
    async function fetchClientById(id: number) {
        return (await axios.get<APIResponse<Client>>(`/api/v1/item/${id}`)).data
    }


    return {
        client,
        paginatedClient,
        allClient,
        currentPaginatedClientPage,
        fetchClientById,
        fetchAllClient,
        fetchClientPaginated,
        saveClient,
        editClient,
        removeClient,
    }
})
