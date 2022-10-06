import type { Booleanish } from '../Common'

export default interface TableSettings {
    hover?: Booleanish
    align?: VerticalAlignment
    caption?: string
    borderless?: Booleanish
    bordered?: Booleanish
    dark?: Booleanish
    fields?: Array<TableField>
    items?: Array<TableItem>
    responsive?: boolean | 'sm' | 'md' | 'lg' | 'xl' | 'xxl'
    perPage?: number
    stripped?: Booleanish
    currentPage?: number
    tableClass?: string | string[]
}
