import type {
    PaginatedAPIResponse,
    Employee,
    PaginatedResponse,
} from '@store-types'
import axios from 'axios'
import { defineStore } from 'pinia'

export type EmployeeSearchParams = {}

type Identifier = string | number

/**
 * The Employee repository
 */
export const useEmployeeStore = defineStore('employee', () => {
    /**
     * The employee returned by an single search
     */
    const employee = ref<Employee>()
    /**
     * The pagination list of employees returned by a query
     */
    const paginatedEmployees = ref<PaginatedResponse<Employee>>()
    /**
     * All the employees listed on the database
     */
    const employees = ref<Employee[]>()

    /**
     * This function make a request to teh backend and by the given parameters of
     * search it would return a paginated list of results that the backend would return
     * of employees.
     *
     * @param params the search params that would be sent to the backend
     */
    async function fetchEmployees(
        params?: EmployeeSearchParams & PaginationOptions
    ) {
        const response = (
            await axios.get<PaginatedResponse<Employee>>(
                '/api/v1/list/employees',
                { params }
            )
        ).data
        paginatedEmployees.value = response
        return response
    }

    /**
     * This function make a request to the backend and by the given parameter, find the
     * desired employee or return an error.
     *
     * @param identifier The identifier of the employee
     */
    async function fetchEmployee(identifier: Identifier) {
        const response = (
            await axios.get<Employee>(`/api/v1/employee/${identifier}`)
        ).data
        employee.value = response
        return response
    }

    return {
        employee,
        paginatedEmployees,
        fetchEmployee,
        fetchEmployees,
    }
})
