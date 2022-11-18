import type { Employee, PaginatedResponse } from '@store-types'
import type { MessageResponse } from '@store-types'
import axios from 'axios'
import { defineStore } from 'pinia'

import type { EmployeeForm } from './types/user.model'

export type EmployeeSearchParams = {
    name?: string
    cid?: string
}

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

    /**
     * This function make a request to the backend and by the given parameter, change the status
     *
     * @param identifier The identifier of the employee
     */
    async function fetchActivateEmployee(identifier: Identifier) {
        const response = (
            await axios.post<Employee>(
                `/api/v1/employee/${identifier}/activate`
            )
        ).data
        employee.value = response
        return response
    }

    /**
     * This function make a request to the backend and by the given parameter, change the status
     *
     * @param identifier The identifier of the employee
     */

    async function fetchInactivateEmployee(identifier: Identifier) {
        const response = (
            await axios.post<Employee>(
                `/api/v1/employee/${identifier}/inactivate`
            )
        ).data
        employee.value = response
        return response
    }

    /**
     * This function creates an new employee and saves it into the system.
     *
     * @param employee the user to save
     */
    function saveEmployee(employee: EmployeeForm) {
        return axios.post<MessageResponse>('/api/v1/employee', employee)
    }

    /**
     * This function update an employee and saves it into the system.
     *
     * @param employee th to save
     */
    function updateEmployee(id: number | string, data: EmployeeForm) {
        return axios.put<MessageResponse>(`/api/v1/employee/${id}`, data)
    }

    /**
     * This function remove an employee.
     *
     * @param employee to save
     */
    function removeEmployee(id: number | string) {
        return axios.delete<MessageResponse>(`/api/v1/employee/${id}`)
    }

    return {
        employee,
        paginatedEmployees,
        fetchEmployee,
        fetchEmployees,
        fetchActivateEmployee,
        fetchInactivateEmployee,
        saveEmployee,
        updateEmployee,
        removeEmployee,
    }
})
