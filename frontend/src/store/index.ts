import axios from 'axios'
import { defineStore } from 'pinia'

axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL
// axios.defaults.headers?.set(
//     'Access-Control-Allow-Origin',
//     '*'
// )
// axios.defaults.headers.common[
//     'Access-Control-Allow-Origin'
// ] = '*'
export const useAuthStore2 = defineStore('auth-store', {
    state: () => ({
        token: '',
        isAuthenticated: false,
    }),
    actions: {
        initial() {
            if (localStorage.getItem('token')) {
                this.token = ''
                this.isAuthenticated = true
            } else {
                this.token = ''
                this.isAuthenticated = false
            }
        },
        setToken(state: Auth, token: string) {
            state.token = token
            state.isAuthenticated = true
        },
        removeToken(state: Auth) {
            state.token = ''
            state.isAuthenticated = false
        },
    },
})

export * from './auth'
