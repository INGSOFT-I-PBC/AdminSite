import type { MessageResponse } from '@store-types'
import axios from 'axios'
import { defineStore } from 'pinia'

import { ref } from 'vue'

import type { PaginatedResponse, User } from './types'
import type { SimpleUser, SimpleUserForm, UserForm } from './types/user.model'

export type UserSearchParams = {
    username?: string
    order_by?: string | string[]
}
type identifier = number | string

export const useUserStore = defineStore('user-store', () => {
    const user = ref<SimpleUser | null>(null)

    const users = ref<PaginatedResponse<SimpleUser> | null>(null)

    /**
     * This function make a request to the backend and, if params are provided,
     * return a list of the matching users by pagination.
     *
     * @param params the search params of the request
     */
    async function fetchUsers(params?: UserSearchParams & PaginationOptions) {
        const response = (
            await axios.get<PaginatedResponse<SimpleUser>>(
                '/api/v1/list/users',
                { params }
            )
        ).data
        users.value = response
        return response
    }

    /**
     * This function make a request to the backend and by the given parameter,
     * finds the user of not.
     *
     * @param idOrUsername The search param for the user
     */
    async function fetchUser(idOrUsername: identifier) {
        const response = (
            await axios.get<SimpleUser>(`/api/v1/user/${idOrUsername}`)
        ).data
        user.value = response
        return response
    }

    /**
     * This function creates an new user and saves it into the system.
     *
     * @param user the user to save
     */
    function saveUser(user: SimpleUserForm) {
        return axios.post<MessageResponse>('/api/v1/user', user)
    }

    /**
     * This function saves the data related to an active user, and updates with
     * the provided data
     *
     * @param idOrUsername the id or username of the user to update
     * @param data The data to modify into the user
     */
    function updateUser(idOrUsername: identifier, data: UserForm) {
        return axios.put<MessageResponse>(`/api/v1/user/${idOrUsername}`, data)
    }

    /**
     * This function soft-delete a given user on the system only if it can be removed.
     *
     * @param idOrUsername The id or username of the user to deactivate on the system
     */
    function removeUser(idOrUsername: identifier) {
        return axios.delete<MessageResponse>(`/api/v1/user/${idOrUsername}`)
    }

    /**
     * This function activate a user on the system if and only if it's deactivated.
     *
     * @param idOrUsername The id or username of the target user
     */
    function activateUser(idOrUsername: identifier) {
        return axios.post<MessageResponse>(
            `/api/v1/user/${idOrUsername}/activate`
        )
    }

    return {
        user,
        users,
        fetchUsers,
        fetchUser,
        saveUser,
        updateUser,
        removeUser,
        activateUser,
    }
})
