export interface MessageResponse {
    error: Optional<boolean>
    message: string
}

export type DataResponse<T> = T

export type APIResponse<T> = MessageResponse | DataResponse<T>

export type PaginatedResponse<T> = {
    data: T[]
    page: number
    lastPage: Optional<number>
}

export type PaginatedAPIResponse<T> = PaginatedResponse<T> | MessageResponse

type RequestParams = Record<string, any>


export function isMessage(response: APIResponse<T> | PaginatedAPIResponse<T>): response is MessageResponse {
    return response.message ?? undefined === undefined
}

export default PaginatedResponse
