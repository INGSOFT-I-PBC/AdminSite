export interface MinimalWarehouse {
    name: string;
    status: { description: string, name: string, id: string };
}

export interface Warehouse extends MinimalWarehouse {
    id: number;
}

export default {}
