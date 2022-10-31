import type { Employee } from './user.model'
import type { MetaData } from '@store-types'

export interface IInvoiceDetails {
    id: number
    price: number
    quantity: number
    invoice: number
    item:number
}
export interface IPayment {
    id: number
    name: string
}
export interface IClient {
    business_name: string,
    email:string,
    number_id:string
    name: string
}

export interface Invoice {
    id:number,
    client:Maybe<IClient>,
    created_at?: string,
    iva:number,
    payment_method:Maybe<IPayment>
    status:number,
    subtotal:number,
    total:number,
    anulated:boolean,
    created_by: Maybe<Employee> | null
    invoice_details: Maybe<IInvoiceDetails[]> | null
}


export interface FullInvoice extends Invoice {
    meta: Optional<MetaData>
}

export default {}
