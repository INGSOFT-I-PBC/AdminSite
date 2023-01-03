import type { AxiosError } from 'axios'

export interface MessageResponse {
    error: Optional<boolean>
    message: string
    code?: string
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

export type ErrorResponse<D = any> = AxiosError<MessageResponse, D>

type RequestParams = Record<string, any>

/**
 * This type is a possible response given by a Serializer on django backend
 */
export type BadValidationResponse = Record<string, string[]>

export default PaginatedResponse
