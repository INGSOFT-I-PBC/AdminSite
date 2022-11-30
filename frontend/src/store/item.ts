import type Item from '@/interfaz/items'
import type Status from '@/interfaz/items'
import type { PaginatedResponse } from '@store-types'
import axios, { type AxiosResponse } from 'axios'

/* eslint-disable */
class ItemDataService {
    clients = ref<PaginatedResponse<any>>()
    async getAll(): Promise<any> {
        return await axios.get('/api/v1/inventory', {
            headers: {
                'Content-Type': 'application/json',
            },
        })
    }
    async getAllPaginated(params?: PaginationOptions) {
        const response = (
            await axios.get<PaginatedResponse<any>>(
                '/api/v1/list/inventory/all',
                { params }
            )
        ).data
        this.clients.value = response
        return response
    }
    async fetchPaginatedListInventory(
        options: any,
        paginated_opt: PaginationOptions
    ) {
        const queryParams = {
            ...options,
            page: paginated_opt.page,
            per_page: paginated_opt.per_page,
        }
        const response = (
            await axios.get<PaginatedResponse<any>>('/api/v1/inventories', {
                params: queryParams,
            })
        ).data
        this.clients.value = response
        return response
    }

    /**
     * This function make a request to the backend and by the given parameter, change the status
     *
     * @param identifier The identifier of the employee
     */
    async fetchActivateItem(identifier: Number) {
        const response = (
            await axios.post<any>(`/api/v1/item/${identifier}/activate`)
        ).data
        this.clients.value = response
        return response
    }

    /**
     * This function make a request to the backend and by the given parameter, change the status
     *
     * @param identifier The identifier of the item
     */

    async fetchInactivateItem(identifier: Number) {
        const response = (
            await axios.post<any>(`/api/v1/item/${identifier}/inactivate`)
        ).data
        this.clients.value = response
        return response
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
        return axios.put(`/api/v1/items/${pk}`, data, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
    }
    updateInventory(pk: number, data: any): Promise<any> {
        return axios.put(`/api/v1/inventory/${pk}`, data, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
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
