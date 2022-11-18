import type {
    PaginatedAPIResponse,
    Role,
    PaginatedResponse,
} from '@store-types'
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
     * All the roles listed on the database
     */
    const roles = ref<Role[]>()

    /**
     * This function make a request to teh backend and by the given parameters of
     * search it would return a paginated list of results that the backend would return
     * of roles.
     *
     * @param params the search params that would be sent to the backend
     */
    async function fetchRoles(
        params?: PaginationOptions
    ) {
        const response = (
            await axios.get<PaginatedResponse<Role>>(
                '/api/v1/list/roles',
                { params }
            )
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
        const response = (
            await axios.get<Role>(`/api/v1/role/${id}`)
        ).data
        role.value = response
        return response
    }


    return {
        role,
        paginatedRoles,
        fetchRole,
        fetchRoles,
    }
})
