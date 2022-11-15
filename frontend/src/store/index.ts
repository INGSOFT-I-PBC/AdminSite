import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL

const savedTokens: Optional<JWTToken> = JSON.parse(
    localStorage.getItem('accessToken') ?? 'null'
)

if (savedTokens) {
    axios.defaults.headers.common[
        'Authorization'
    ] = `Bearer ${savedTokens.access}`
}

export * from './auth'
export * from './client'
export * from './common'
export * from './employee'
export * from './items'
export * from './order'
export * from './provider'
export * from './users'
export * from './warehouse'
export * from './payment'
