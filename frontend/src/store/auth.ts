/* eslint-disable  @typescript-eslint/no-non-null-assertion */
import {
    SessionExpiredException,
    UndersiredStateError,
    UserNotLoggedInError,
} from '@/exceptions'
import axios from 'axios'
import { defineStore } from 'pinia'

const savedToken: JWTToken | null = JSON.parse(
    localStorage.getItem('accessToken') ?? 'null'
)
const savedUserData: Nullable<UserInfo> = JSON.parse(
    localStorage.getItem('userData') ?? 'null'
)
/**
 * This store contains the data from the user authentication. Also
 * contains method to handle the API authorization and authentication.
 */
export const useAuthStore = defineStore('auth-store', {
    state: (): AuthState => ({
        jwtData: savedToken,
        userData: savedUserData,
    }),
    getters: {
        /** Get the list of permission of the current user */
        getToken(state): Nullable<JWTToken> {
            return state.jwtData
        },
        getPermissions: (state): Array<string> =>
            state.userData?.permissions ?? [],
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
                const data = await (
                    await axios.post<JWTAccessToken>('/api/v1/token-refresh', {
                        refresh: this.jwtData!.refresh,
                    })
                ).data
                this.jwtData!.access = data.access
                localStorage.setItem(
                    'accessToken',
                    JSON.stringify(this.jwtData)
                )
                axios.defaults.headers.common[
                    'Authorization'
                ] = `Bearer ${data.access}`
            } catch (error) {
                if (this.jwtData) throw new SessionExpiredException()
                throw new UserNotLoggedInError()
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

        /**
         * Validate with the backend if user's credentials is correct.
         */
        login(datos: { username: string; password: string }) {
            return new Promise<JWTToken>((commit, reject) => {
                axios
                    .post<JWTToken>('/api/v1/login', datos)
                    .then(({ data }) => {
                        this.jwtData = data
                        localStorage.setItem(
                            'accessToken',
                            JSON.stringify(data)
                        )
                        axios.defaults.headers.common[
                            'Authorization'
                        ] = `Bearer ${this.jwtData?.access}`
                        commit(data)
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },

        async fetchUserData() {
            const data = await (
                await axios.get<UserInfo>('/api/v1/auth/me')
            ).data
            this.userData = data
            localStorage.setItem('userData', JSON.stringify(data))
            return data
        },

        async logout() {
            try {
                await axios.post('/api/v1/logout', {
                    refresh: this.jwtData?.refresh || '',
                })
                this.jwtData = null
                axios.defaults.headers.common['Authorization'] = undefined
            } catch (error) {
                if (!this.jwtData)
                    throw new UndersiredStateError(
                        'The user has tried log out without login previously'
                    )
                throw error
            } finally {
                localStorage.removeItem('accessToken')
                localStorage.removeItem('userData')
            }
        },
    },
})
