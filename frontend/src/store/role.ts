import type {
    PaginatedAPIResponse,
    PaginatedResponse,
    Role,
} from '@store-types'
import type { MessageResponse } from '@store-types'
import axios from 'axios'
import { defineStore } from 'pinia'

type id = string | number

/**
 * The Employee repository
 */
export const useRoleStore = defineStore('role', () => {
    /**
     * The role returned by an single search
     */
    const role = ref<Role>()
    /**
     * The pagination list of roles returned by a query
     */
    const paginatedRoles = ref<PaginatedResponse<Role>>()

    /**
     * This function make a request to teh backend and by the given parameters of
     * search it would return a paginated list of results that the backend would return
     * of roles.
     *
     * @param params the search params that would be sent to the backend
     */
    async function fetchRoles(params?: PaginationOptions) {
        const response = (
            await axios.get<PaginatedResponse<Role>>('/api/v1/list/roles', {
                params,
            })
        ).data
        paginatedRoles.value = response
        return response
    }

    /**
     * This function make a request to the backend and by the given parameter, find the
     * desired role or return an error.
     *
     * @param id The identifier of th erole
     */
    async function fetchRole(id: id) {
        const response = (await axios.get<Role>(`/api/v1/role/${id}`)).data
        role.value = response
        return response
    }

    /**
     * This function creates an new role and saves it into the system.
     */
    function saveRole(role: Role) {
        return axios.post<MessageResponse>('/api/v1/role', role)
    }

    /**
     * This function update a role.
     */
    function updateRole(id: number | string, data: Role) {
        return axios.put<MessageResponse>(`/api/v1/role/${id}`, data)
    }

    /**
     * This function remove a role.
     */
    function removeRole(id: number | string) {
        return axios.delete<MessageResponse>(`/api/v1/role/${id}`)
    }

    return {
        role,
        paginatedRoles,
        fetchRole,
        fetchRoles,
        saveRole,
        updateRole,
        removeRole,
    }
})
