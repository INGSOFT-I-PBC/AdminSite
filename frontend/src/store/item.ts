import axios, { type AxiosResponse } from 'axios'
import type Item from '@/interfaz/items'
import type Status from '@/interfaz/items'

/* eslint-disable */
class ItemDataService {
    async getAll(): Promise<any> {
        return await axios.get('/api/v1/inventory', {
            headers: {
                'Content-Type': 'application/json',
            },
        })
    }
    async getAllCategory(): Promise<any> {
        return await axios.get('/api/v1/category', {
            headers: {
                'Content-Type': 'application/json',
            },
        })
    }
    async getAllWarehouses(): Promise<any> {
        return await axios.get('/api/v1/list/warehouses/all', {
            headers: {
                'Content-Type': 'application/json',
            },
        })
    }

    async get(id: string): Promise<AxiosResponse<Item>> {
        return await axios.get(`/api/v1/inventory/${id}`, {
            headers: {
                'Content-Type': 'application/json',
            },
        })
    }

    createItem(data: any): Promise<any> {
        return axios.post('/api/v1/items', data, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
    }
    createInventory(data: any): Promise<any> {
        return axios.post('/api/v1/inventory', data, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
    }

    updateItem(pk: number, data: any): Promise<any> {
        return axios.put(
            `/api/v1/items/${pk}`,data,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            },

        )
    }
    updateInventory(pk: number, data: any): Promise<any> {
        return axios.put(
            `/api/v1/inventory/${pk}`,data,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            },

        )
    }

    deleteItem(pk: number): Promise<any> {
        return axios.delete(`/api/v1/items/${pk}`, {
            headers: {},
        })
    }

    deleteInventory(pk: number): Promise<any> {
        return axios.delete(`/api/v1/inventory/${pk}`, {
            headers: {},
        })
    }
    async fetchStatus(name: string) {
        const data = await (
            await axios.get<Status>(`/api/v1/status?name=${name}`)
        ).data
        return data
    }

}

export default new ItemDataService()
