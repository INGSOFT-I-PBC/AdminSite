import type { MessageResponse, PaginatedResponse, Status } from '@store/types'
import type {
    FUllPurchaseDetails,
    Purchase,
    PurchaseQuery,
} from '@store/types/purchase.model'
import axios from 'axios'
import { defineStore } from 'pinia'

/**
 * Names of the status for puchase registered in the database
 */

const APROVED_STATUS = { name: 'aprovado', display: 'Aprovado' }
const DELIVERED_STATUS = { name: 'entregado', display: 'Entregado' }
const TRANSIT_STATUS = { name: 'transito', display: 'En Tránsito' }
const CANCELED_STATUS = { name: 'cancelado', display: 'Cancelado' }
const RETURNED_STATUS = { name: 'rechazado', display: 'Rechazado' }

const valid_status = [
    APROVED_STATUS,
    DELIVERED_STATUS,
    CANCELED_STATUS,
    TRANSIT_STATUS,
    RETURNED_STATUS,
]

export const usePurchaseStore = defineStore('orders', () => {
    const purchase = ref<Purchase>()
    const purchaseRequest = ref<PaginatedResponse<Purchase>>()
    const purchaseStatus = ref<Status[]>()
    /**
     * This function searches all the valid purchase status
     */
    function getPurchaseStatus() {
        return valid_status
    }

    return {
        getPurchaseStatus,
    }
})
