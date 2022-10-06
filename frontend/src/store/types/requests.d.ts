export interface MessageResponse {
    error: Optional<boolean>
    message: string
}

export type DataResponse<T> = T

export type APIResponse<T> = MessageResponse | DataResponse<T>

export type PaginatedResponse<T> = {
    data: T[]
    page: number
    lastPage: number
    total: number
    next?: string
    previous?: string
}

export type PaginatedAPIResponse<T> = PaginatedResponse<T> | MessageResponse

type RequestParams = Record<string, any>

export default PaginatedResponse
