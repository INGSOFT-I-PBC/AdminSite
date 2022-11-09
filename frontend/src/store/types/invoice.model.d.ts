import type { Employee } from './user.model'
import type { MetaData } from '@store-types'
import type { date } from 'yup'

export interface ICategory {
    id: number
    name: string
}
export interface IServerOptions {
    page: number
    rowsPerPage: number
    buscar?: string
    sortBy?: string | string[]
    sortType?: SortType | SortType[]
}

export interface IItem {
    id: number
    codename: string
    brand: string
    category: Maybe<Category>
    iva: number
    model: string
    name: string
    price: string
}

export interface IInvoiceDetails {
    id?: number
    price: number
    quantity: number
    item: number
}
export interface IPayment {
    id: number
    created_at: string
    name: string
    status: number
}
export interface IClient {
    id?: number
    business_name: string
    email: string
    number_id: string
    name: string
}

export interface Invoice {
    id?: number
    code: string
    client: Maybe<IClient> | null | number
    emission: string
    return_deadline: string
    created_at?: string
    iva: number
    payment_method: Maybe<IPayment> | null | number
    status: number
    subtotal: number
    total: number
    anulated: boolean
    invoice_details: IInvoiceDetails[] | null
}

export interface FullInvoice extends Invoice {
    meta: Optional<MetaData>
}

export default {}