import axios from 'axios'
import { defineStore } from 'pinia'

import type { MessageResponse, PaginatedResponse } from './types'
import type {
    Provider,
    ProviderForm,
    ProviderModel,
} from './types/provider.model'

export type ProviderSearchParam = {
    name?: string
    document_path?: string
    email?: string
}

type identifier = number
export const useProviderStore = defineStore('provider-store', () => {
    const provider = ref<Provider>()
    const providers = ref<PaginatedResponse<Provider>>()

    async function fetchProvider(param: identifier) {
        const response = (
            await axios.get<Provider>(`/api/v1/provider/${param}`)
        ).data
        provider.value = response
        return response
    }

    /**
     * This method will fetch a paginated list of users that are
     * filtered by the given params.
     *
     * @param params the search params
     */
    async function fetchProviders(
        params?: PaginationOptions & ProviderSearchParam
    ) {
        const response = (
            await axios.get<PaginatedResponse<Provider>>(
                '/api/v1/list/providers',
                { params }
            )
        ).data
        providers.value = response
        return response
    }

    /**
     * This method would update certain data of a given provider.
     *
     * @param identifier The identifier of the target provider
     * @param data The data to update on the target provider
     */
    async function updateProvider(identifier: identifier, data: ProviderForm) {
        return (
            await axios.put<MessageResponse>(
                `/api/v1/provider/${identifier}`,
                data
            )
        ).data
    }

    /**
     * This method would delete the provider with the respective
     * identifier.
     *
     * @param identifier The identifier of the target user
     */
    async function deleteProvider(identifier: identifier) {
        return (
            await axios.delete<MessageResponse>(
                `/api/v1/provider/${identifier}`
            )
        ).data
    }

    /**
     * This function create a new Provider with the given data.
     *
     * @param data the data of the given provider
     */
    async function createProvider(data: ProviderModel) {
        return (await axios.post<Provider>('/api/v1/provider', data)).data
    }

    return {
        provider,
        providers,
        fetchProvider,
        fetchProviders,
        updateProvider,
        deleteProvider,
        createProvider,
    }
})
