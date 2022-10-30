import type { PaginatedAPIResponse } from '@store-types'

export interface Group {
    id?: number
    codename: string
    name: string
}

export type PaginatedGroups = PaginatedAPIResponse<Group>

export type Groups = Group[]
