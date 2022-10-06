import type {
    APIResponse,
    MessageResponse,
    PaginatedAPIResponse,
} from '@store-types'

export function isMessage<T>(
    response: APIResponse<T> | PaginatedAPIResponse<T>
): response is MessageResponse {
    const keylen =
        typeof response == 'object' ? Object.keys(response ?? {}).length : 0
    return (
        response != null &&
        'message' in response &&
        keylen > 0 &&
        keylen <= 2 &&
        typeof response.message == 'string'
    )
}
