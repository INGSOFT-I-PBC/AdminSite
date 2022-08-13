import axios from 'axios'

axios.defaults.baseURL =
    import.meta.env.VITE_BACKEND_URL
// axios.defaults.headers?.set(
//     'Access-Control-Allow-Origin',
//     '*'
// )
// axios.defaults.headers.common[
//     'Access-Control-Allow-Origin'
// ] = '*'

export * from './auth'
