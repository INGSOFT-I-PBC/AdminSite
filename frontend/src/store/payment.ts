import type { IPayment } from '@store-types'
import axios from 'axios'
import { defineStore } from 'pinia'

import type { Ref } from 'vue'

export const usePaymentStore = defineStore('payment-store', () => {
    const allPayment: Ref<Optional<IPayment[]>> = ref(null)

    async function fetchPayment() {
        const data = await (
            await axios.get<IPayment[]>('/api/v1/list/payment/all')
        ).data
        allPayment.value = data
        return data
    }

    return {
        allPayment,
        fetchPayment,
    }
})
