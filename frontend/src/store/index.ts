import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL

const savedTokens: Optional<JWTToken> = JSON.parse(
    localStorage.getItem('accessToken') ?? 'null'
)

if (savedTokens) {
    axios.defaults.headers.common = {
        ...axios.defaults.headers.common,
        Authorization: `Bearer ${savedTokens.access}`,
    }
}

export * from './auth'
export * from './warehouse'
export * from './items'
