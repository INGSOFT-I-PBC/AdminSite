export interface MinimalPurchase {

        img_details: string,
        invoice: {
            id: number,
            code: string
        },
        provider: number,
        order_origin: number,
        reference: number,
        warehouse: number,
        status: string
}

export interface Purchase extends MinimalWarehouse {
    id: number
}

export default {}
