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
     * The employee returned by an single search
     */
    const role = ref<Role>()
    /**
     * The pagination list of employees returned by a query
     */
    const paginatedRoles = ref<PaginatedResponse<Role>>()
    /**
     * All the employees listed on the database
     */
    const roles = ref<Role[]>()

    /**
     * This function make a request to teh backend and by the given parameters of
     * search it would return a paginated list of results that the backend would return
     * of employees.
     *
     * @param params the search params that would be sent to the backend
     */
    async function fetchRoles(
        params?: PaginationOptions
    ) {
        const response = (
            await axios.get<PaginatedResponse<Role>>(
                '/api/v1/list/employees',
                { params }
            )
        ).data
        paginatedRoles.value = response
        return response
    }

    /**
     * This function make a request to the backend and by the given parameter, find the
     * desired employee or return an error.
     *
     * @param identifier The identifier of the employee
     */
    async function fetchRole(id: id) {
        const response = (
            await axios.get<Role>(`/api/v1/employee/${id}`)
        ).data
        role.value = response
        return response
    }

    /**
     * This function make a request to the backend and by the given parameter, change the status
     *
     * @param identifier The identifier of the employee

     async function fetchActivateEmployee(identifier: Identifier) {
        const response = (
            await axios.post<Employee>(`/api/v1/employee/${identifier}/activate`)
        ).data
        employee.value = response
        return response
    }



    async function fetchInactivateEmployee(identifier: Identifier) {
        const response = (
            await axios.post<Employee>(`/api/v1/employee/${identifier}/inactivate`)
        ).data
        employee.value = response
        return response
    }*/

    return {
        role,
        paginatedRoles,
        fetchRole,
        fetchRoles,
    }
})
