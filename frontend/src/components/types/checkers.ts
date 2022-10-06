import type { TableColumn, TableColumnish } from '@components-types'

export function isTableColumn(target: TableColumnish): target is TableColumn {
    return typeof target !== 'string'
}
export function identity<T>(input: T): T {
    return input
}

export default {}
