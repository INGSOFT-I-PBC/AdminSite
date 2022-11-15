import type { StyleValue, TdHTMLAttributes, TrackHTMLAttributes } from 'vue'

import type { ColorVariant } from './bootstrap'

export interface TableColumn {
    label: string
    field: string
}

export type TableItem<T = Record<string, unknown>> = T & {
    rowVariants?: unknown
    cellVariants?: unknown
    showDetails?: boolean
}

export interface TableFieldObject<T = Record<string, unknown>> {
    label?: string
    headerTitle?: string
    borderVariant?: ColorVariant
    variant?: ColorVariant
    tdClass?: string | string[]
    thClass?: string | string[]
    thStyle?: StyleValue
    tdAttr?: TdHTMLAttributes
    thAttr?: TrackHTMLAttributes
    isRowHeader?: boolean
    stickyColumn?: boolean
    selectable?: boolean
}

export type TableField<T = Record<string, unknown>> = string | TableFieldObject

export type TableColumnish = TableColumn | string

export type NormalizedHeader = {
    label: string
    field: string
    content: TableColumnish
}
