import type {
    MessageResponse,
    Movement,
    MovementDetail,
    MovementQuery,
    MovementSaveData,
    MovementStatus,
    PaginatedAPIResponse,
} from '@store-types'
import axios from 'axios'
import { defineStore } from 'pinia'

/**
 * Names of the status for movements registered in the database
 */
const PENDING_STATUS = { name: 'pendiente', display: 'Pendiente' }
const APROVED_STATUS = { name: 'aprobado', display: 'Aprobado' }
const DELIVERED_STATUS = { name: 'entregado', display: 'Entregado' }
const TRANSIT_STATUS = { name: 'transito', display: 'En Tránsito' }
const CANCELED_STATUS = { name: 'cancelado', display: 'Cancelado' }
const RETURNED_STATUS = { name: 'rechazado', display: 'Rechazado' }

const valid_status = [
    PENDING_STATUS,
    APROVED_STATUS,
    DELIVERED_STATUS,
    CANCELED_STATUS,
    TRANSIT_STATUS,
    RETURNED_STATUS,
]

type FullMovement = Movement & { details: MovementDetail[] }

export interface MovementState {
    lastPurchaseList: Optional<Movement[]>
    paginatedMovement: Optional<PaginatedAPIResponse<Movement>>
}

export const useMovementStore = defineStore('movement-store', {
    state: (): MovementState => ({
        lastPurchaseList: null,
        paginatedMovement: null,
    }),

    getters: {
        getMovementStatus: state => state.lastPurchaseList,
        getPaginatedMovement: state => state.paginatedMovement,
    },

    actions: {
        getPurchaseStatus() {
            return valid_status
        },

        async fetchPaginatedMovement(
            options: MovementQuery,
            paginated_opt: PaginationOptions
        ): Promise<PaginatedAPIResponse<Movement>> {
            const queryParams = {
                ...options,
                page: paginated_opt.page,
                per_page: paginated_opt.per_page,
            }
            const result = await (
                await axios.get<PaginatedAPIResponse<Movement>>(
                    '/api/v1/warehouse/movements',
                    { params: queryParams }
                )
            ).data
            this.paginatedMovement = result
            return result
        },

        async fetchMovementInformation(
            options: MovementQuery
        ): Promise<FullMovement[] | MessageResponse> {
            const result = await (
                await axios.get<FullMovement[] | MessageResponse>(
                    '/api/v1/movement',
                    { params: options }
                )
            ).data
            return result
        },

        async fetchMovementStatus(
            options: MovementQuery
        ): Promise<MovementStatus[] | MessageResponse> {
            const result = await (
                await axios.get<MovementStatus[] | MessageResponse>(
                    '/api/v1/movement/status',
                    { params: options }
                )
            ).data
            return result
        },
        async saveMovement(
            data: MovementSaveData
        ): Promise<Movement | MessageResponse> {
            const result = await (
                await axios.post<Movement | MessageResponse>(
                    '/api/v1/movement/create',
                    data
                )
            ).data
            return result
        },
    },
})
