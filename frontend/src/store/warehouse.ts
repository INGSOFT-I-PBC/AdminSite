import axios from "axios";
import { defineStore } from "pinia";
import type { Warehouse } from "./models/warehouseModels";


export interface WarehouseState {
    lastWarehouseList: Optional<Warehouse[]>
}

export const useWarehouseStore =defineStore('warehouse-store',
{
    state: (): WarehouseState => ({
        lastWarehouseList: null
    }),

    getters: {
        getWarehouseList: state => state.lastWarehouseList
    },

    actions: {
        async fetchPaginated(options: PaginationOptions) {
            const result = await( await axios
                .get<Warehouse[]>('/api/v1/warehouse/list', {params: options}))
                .data
            this.lastWarehouseList = result
        }
    }

})
