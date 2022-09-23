import { defineStore } from 'pinia'
import axios from 'axios'

/**
 * This store contains the data from the user authentication. Also
 * contains method to handle the API authorization and authentication.
 */
export const useAuthStore = defineStore('auth-store', {
    state: (): AuthState => ({
        jwtData: null,
        userData: null,
    }),
    getters: {
        /** Get the list of permission of the current user */
        getPermissions: (state): Array<string> => state.userData?.permissions || [],
    },
    actions: {
        /**
         * This method would try to refresh the authorization token when called
         * and configure all the axios cookies to use the new one.
         *
         * @param param0 The inferred parameter injected by Pinia
         */
        async refreshToken() {
            try {
                const data = await axios.post(
                    'http://127.0.0.1:8000/api/v1/token-refresh',
                    {
                        refresh: this.jwtData?.refreshToken || '',
                    }
                )
            } catch (error) {
                console.error("Couldn't refresh token.", error)
            }
        },
        /**
         * Check if the current user has a specific permission to unlock a functionality.
         *
         * @param permission the permission to check
         * @returns true if the current user has the given permission
         */
        hasPermission(permission: string): boolean {
            console.info(
                `[AUTH-STORE] Checking if has the permission: ${permission}`
            )
            return this.getPermissions.indexOf(permission) >= 0
        },
        /**
         * Validate with the backend if the current user is already authenticated
         * and, if not, try to refresh the token to proceed or redirect to login.
         *
         * @returns a promise with the response of the server that validate
         * the authentication
         */
        async isAuthenticated(): Promise<boolean> {
            console.debug('[AUTH-STORE] Checking if is authenticated')
            // TODO: Change this with real checking
            return true
        },
    },
})
