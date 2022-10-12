import axios, { type AxiosResponse } from 'axios'
import type Item from '@/interfaz/items'

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

    updateItem(id: any, data: any): Promise<any> {
        return axios.put(
            `/api/v1/items/${id}`,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            },
            data
        )
    }
    updateInventory(id: any, data: any): Promise<any> {
        return axios.put(
            `/api/v1/inventory/${id}`,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            },
            data
        )
    }

    deleteItem(id: any): Promise<any> {
        return axios.delete(`/api/v1/items/${id}`, {
            headers: {},
        })
    }

    deleteInventory(id: any): Promise<any> {
        return axios.delete(`/api/v1/inventory/${id}`, {
            headers: {},
        })
    }
}

export default new ItemDataService()
