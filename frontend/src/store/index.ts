import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL

const savedTokens: Optional<JWTToken> = JSON.parse(
    localStorage.getItem('accessToken') ?? "null"
    )

if (savedTokens) {
    axios.defaults.headers.common = {
        ...axios.defaults.headers.common,
        Authorization: `Bearer ${savedTokens.access}`,
      }
}
// axios.defaults.headers?.set(
//     'Access-Control-Allow-Origin',
//     '*'
// )
// axios.defaults.headers.common[
//     'Access-Control-Allow-Origin'
// ] = '*'

export * from './auth'
export * from './warehouse'
