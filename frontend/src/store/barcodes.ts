import axios from 'axios'
import { defineStore } from 'pinia'

import type { PaginatedResponse } from './types'
import type { FullBarcodeModel } from './types/warehouse.model'

export type BarcodeSearchOptions = PaginationOptions & {
    batch_no?: string
}

export const useBarcodeStore = defineStore('barcode-store', () => {
    const barcode = ref<FullBarcodeModel>()
    const barcodes = ref<PaginatedResponse<FullBarcodeModel>>()

    async function getBarcodes(warehouse: number) {
        const result = (
            await axios.get(`/api/v1/warehouse/${warehouse}/barcodes`)
        ).data
        return result
    }

    async function updateBarcode(
        warehouse: number,
        barcode: number,
        data: FullBarccodeModel
    ) {
        const result =
            (await axios.patch(
                `/api/v1/warehouse/${warehouse}/barcode/${barcode}`
            ),
            data)
        return result
    }

    async function createBarcode() {
        console.debug('TODO: Complete this')
    }

    async function invalidateBarcode() {
        console.debug('TODO: Complete this')
    }

    return {
        barcode,
        barcodes,
        getBarcodes,
        updateBarcode,
        createBarcode,
        invalidateBarcode,
    }
})
