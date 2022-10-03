export interface TableColumn {
    label: string
    field: string

}

// declare function isTableColumn(TableCo)

// export function isTableColumn(target: TableColumnish): target is TableColumn {
//     return typeof target !== 'string'
// }

export type TableColumnish = TableColumn | string

export type NormalizedHeader = {
    label: string
    field: string
    content: TableColumnish
}
