import { defineStore } from 'pinia'
import type { OrderSaveData } from '@store/types/orders.model'
import axios from 'axios'
import type { MessageResponse } from '@store/types'

export const useOrderStore = defineStore('orders', () => {
    async function saveOrder(order: OrderSaveData) {
        return axios.post<MessageResponse>('/api/v1/order', order)
    }

    return { saveOrder }
})
