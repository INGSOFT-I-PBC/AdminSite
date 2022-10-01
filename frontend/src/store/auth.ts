import { defineStore } from 'pinia'
import axios from 'axios'

const savedToken:JWTToken|null = JSON.parse(localStorage.getItem('accessToken')??'null')

/**
 * This store contains the data from the user authentication. Also
 * contains method to handle the API authorization and authentication.
 */
function getToken():JWTToken|null { return JSON.parse(localStorage.getItem('accessToken')??'null')}

export const useAuthStore = defineStore('auth-store', {
    state: (): AuthState => ({
        jwtData: savedToken,
        userData: null,
    }),
    getters: {
        /** Get the list of permission of the current user */
        getToken(state):JWTToken|null { return state.jwtData },
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
                const data = await (await axios.post<JWTAccessToken>('/api/v1/token-refresh', {
                    refresh: JSON.parse(localStorage.getItem('accessToken')??'null')?.refreshToken,
                })).data
                this.jwtData!.accessToken = data.accessToken
                localStorage.setItem('accessToken', JSON.stringify(this.jwtData))
                axios.defaults.headers.common['Authorization'] = `Bearer ${data.accessToken}`
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

        /**
         * Validate with the backend if user's credentials is correct.
         */
        login(datos:{username: string, password: string}){
            return new Promise<JWTToken>((commit, reject) => {
              axios
                .post<JWTToken>('/api/v1/login', datos)
                .then(({ data }) => {
                  this.jwtData = data
                  localStorage.setItem('accessToken', JSON.stringify(data))
                  axios.defaults.headers.common = {
                    ...axios.defaults.headers.common,
                    Authorization: `Bearer ${this.jwtData?.accessToken}`,
                  }
                  commit(data)
                })
                .catch(err => {
                  reject(err)
                })
            })
        },

        async logout(){
            try {
                const data = await axios.post('/api/v1/logout', {
                    refresh: this.jwtData?.refreshToken || '',
                })
                localStorage.removeItem('accessToken')
            } catch (error) {
                console.error("Couldn't logout.", error)
            }
        }

    },
})
