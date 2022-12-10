import type {
    APIResponse,
    MessageResponse,
    PaginatedAPIResponse,
} from '@store-types'
import axios from 'axios'

import type { ErrorResponse } from './requests'

export function isMessage<T>(
    response: APIResponse<T> | PaginatedAPIResponse<T>
): response is MessageResponse {
    const keylen =
        typeof response == 'object' ? Object.keys(response ?? {}).length : 0
    let incidences = 0
    Object.keys(response ?? {}).forEach(key => {
        if (['error', 'message', 'code'].includes(key)) {
            incidences += 1
        }
    })
    return (
        response != null &&
        'message' in response &&
        incidences == keylen &&
        typeof response.message == 'string'
    )
}

export function isErrorResponse(value: unknown): value is ErrorResponse {
    if (!axios.isAxiosError(value)) return false

    return isMessage(value.response?.data)
}
