import type {
    APIResponse,
    Item,
    MessageResponse,
    PaginatedAPIResponse,
} from '@store-types'
import axios from 'axios'
import { defineStore } from 'pinia'
import type { Ref } from 'vue'

export const itemStore = defineStore('item-store', () => {
    let item: Ref<Optional<Item>> = ref(null)
    let paginatedItems: Ref<Optional<PaginatedAPIResponse<Item>>> = ref(null)

    let allItems: Ref<Optional<Item[]>> = ref(null)

    async function fetchAllItems() {
        const data = await (await axios.get<Item[]>('/api/v1/list/items')).data
        allItems.value = data
        return data
    }
    async function fetchItemsPaginated(options: PaginationOptions) {
        const data = await (
            await axios.get('/api/v1/items', { params: options })
        ).data
        paginatedItems.value = data
        return data
    }

    /**
     * Save the given item into the system.
     *
     * @param item the item to save
     * @returns a response from the backend
     */
    async function saveItem(item: Item) {
        const data = await (
            await axios.post<MessageResponse>('/api/v1/item', item)
        ).data
        return data
    }

    /**
     * Edit the data of an specific Item into the backend.
     *
     * @param id the Id of the item to edit
     * @param data the data to overwrite
     * @returns the response of the backend
     */
    async function editItem(id: number, data: Item) {
        return await (
            await axios.put<APIResponse<Item>>(`/api/v1/item/${id}`, data)
        ).data
    }

    /**
     * Delete an specific item from the server.
     *
     * @param id the Id of the item to remove
     * @returns the message of the backend.
     */
    async function removeItem(id: number) {
        return await (
            await axios.delete<MessageResponse>(`/api/v1/item/${id}`)
        ).data
    }

    /**
     * Search an specific item.
     *
     * @param id the Id of the item to search
     * @returns the Item result of the search
     */
    async function fetchItemById(id: number) {
        return await (
            await axios.get<APIResponse<Item>>(`/api/v1/item/${id}`)
        ).data
    }

    return {
        item,
        paginatedItems,
        allItems,
        fetchItemById,
        fetchAllItems,
        fetchItemsPaginated,
        saveItem,
        editItem,
        removeItem,
    }
})
