import { isMessage } from '@/store/types/typesafe'
import type {
    APIResponse,
    City,
    Client,
    Gender,
    MessageResponse,
    PaginatedAPIResponse,
    Province,
    Status,
} from '@store-types'
import axios from 'axios'
import { defineStore } from 'pinia'

import { type Ref, computed } from 'vue'

export const useClientStore = defineStore('client-store', () => {
    const client: Ref<Optional<Client>> = ref(null)
    const paginatedClient: Ref<Optional<PaginatedAPIResponse<Client>>> =
        ref(null)
    const currentPaginatedClientPage = computed(() => {
        const pitem = paginatedClient.value
        if (isMessage(pitem)) return undefined
        return pitem?.page
    })

    const allClient: Ref<Optional<Client[]>> = ref(null)
    const allProvince: Ref<Optional<Province[]>> = ref(null)
    const allCity: Ref<Optional<City[]>> = ref(null)
    const allGender: Ref<Optional<Gender[]>> = ref(null)
    const status: Ref<Optional<Status>> = ref(null)

    async function fetchAllClient() {
        const data = await (
            await axios.get<Client[]>('/api/v1/list/clients/all')
        ).data
        allClient.value = data
        return data
    }

    async function fetchClientPaginated(options: PaginationOptions) {
        const data = await (
            await axios.get<PaginatedAPIResponse<Client>>(
                '/api/v1/list/items',
                {
                    params: options,
                }
            )
        ).data
        paginatedClient.value = data
        return data
    }

    /**
     * Save the given client into the system.
     *
     * @param item the client to save
     * @returns a response from the backend
     */
    async function saveClient(item: Client) {
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
    async function editClient(id: number, data: Client) {
        return (await axios.put<Client>(`/api/v1/clients?id=${id}`, data)).data
    }

    /**
     * Delete an specific item from the server.
     *
     * @param id the Id of the item to remove
     * @returns the message of the backend.
     */
    async function removeClient(id: number) {
        return (await axios.delete<MessageResponse>(`/api/v1/clients?id=${id}`))
            .data
    }

    /**
     * Search an specific client.
     *
     * @param id the Id of the client to search
     * @returns the Item result of the search
     */
    async function fetchClientById(id: number) {
        return (await axios.get<Client>(`/api/v1/clients?id=${id}`)).data
    }

    async function fetchAllProvince() {
        const data = await (
            await axios.get<Province[]>('/api/v1/list/provinces/all')
        ).data
        allProvince.value = data
        return data
    }
    async function fetchAllCity(id: number) {
        const data = await (
            await axios.get<City[]>(`/api/v1/provinces?id=${id}`)
        ).data
        allCity.value = data
        return data
    }
    async function fetchAllGender() {
        const data = await (
            await axios.get<Gender[]>(`/api/v1/list/gender/all`)
        ).data
        allGender.value = data
        return data
    }
    async function fetchStatus(name: string) {
        const data = await (
            await axios.get<Status>(`/api/v1/status?name=${name}`)
        ).data
        status.value = data
        return data
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
        fetchAllProvince,
        fetchAllCity,
        fetchStatus,
        fetchAllGender,
    }
})
