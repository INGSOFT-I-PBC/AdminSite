import type { MetaData } from '@store-types'
import type { date } from 'yup'

import type { IClient } from './invoice.model'
import type { Employee } from './user.model'

export interface IServerOptions {
    page: number
    rowsPerPage: number
    buscar?: string
    sortBy?: string | string[]
    sortType?: SortType | SortType[]
}
export interface IPayment {
    id: number
    //created_at: string
    name: string
    //status: number
}
/*export interface CClient {
    id: number
    business_name: string
    email: string
    number_id: string
    name: string
}*/
export interface CEmployee {
    name: string
    lastname: string
    cid: string
    role: number
}
export interface CreditNote {
    id?: number
    code: string
    created_at?: string
    created_by?: CEmployee
    client: Maybe<IClient> | number | undefined
    iva: number
    return_deadline: string
    payment_method: Maybe<IPayment> | number
    subtotal: number
    total: number
    active: boolean
}
export interface EditCreditNoteInvoice {
    credit_note: number
}

export default {}
