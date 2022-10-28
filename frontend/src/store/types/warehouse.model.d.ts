import type { Employee } from "./user.model";

export interface MinimalWarehouse {
    name: string
    status: { description: string; name: string; id: string }
}

export interface Warehouse extends MinimalWarehouse {
    id: number
}

export interface TomaFisica {
    id :number
    done_by : Maybe<Employee>
    creaed_at: string
    novedad: string
    warehouse: number
}

export interface WhWithTomaFisica{
    id: number,
    name: string,
    status: string,
    whtf_created_at: string,
    whtf_done_by_name: string,
    whtf_done_by_lastname: string,
    whtf_novedad?: string,
}


export default {}
