import axios from 'axios'
import { defineStore } from 'pinia'

import type { PaginatedResponse } from './types'
import type {
    BCProductVariant,
    Product,
    ProductCreationForm,
    ProductSearchOptions,
    ProductVariant,
    SimpleProductStock,
} from './types/product'

/**
 * This type represents the identifier of a given product,
 * it must be the `id` or the `sku` value to find them
 */
export type ProductIdentifier = number | string
export type BCSearchParams = {
    code?: string
    name?: string
} & PaginationOptions

export const useProductStore = defineStore('store-product', () => {
    const product = ref<Product>()
    const products = ref<PaginatedResponse<Product>>()
    const productVariant = ref<ProductVariant>()
    const productVariants = ref<PaginatedResponse<ProductVariant>>()

    async function fetchProduct(id: number) {
        const response = (await axios.get<Product>(`/api/v1/product/${id}`))
            .data
        product.value = response
        return response
    }
    async function fetchProducts(
        params?: ProductSearchOptions & PaginationOptions
    ) {
        const response = (
            await axios.get<PaginatedResponse<Product>>(
                `/api/v1/list/products`,
                { params }
            )
        ).data
        products.value = response
        return response
    }

    async function findVariant(id: number | string) {
        const response = (
            await axios.get<ProductVariant>(`/api/v1/products/variant/${id}`)
        ).data
        productVariant.value = response
        return response
    }

    async function fetchVariants(product_id: number) {
        const response = (
            await axios.get<PaginatedResponse<ProductVariant>>(
                `/api/v1/list/product/${product_id}/variants`
            )
        ).data
        productVariants.value = response
        return response
    }

    async function createProduct(data: ProductCreationForm) {
        const response = (await axios.post<Product>(`/api/v1/product`, data))
            .data
        return response
    }

    async function updateProduct(
        id: number,
        data: Partial<ProductCreationForm>
    ) {
        const response = (
            await axios.post<Product>(`/api/v1/product/${id}`, data)
        ).data
        return response
    }

    async function findStockByProduct(
        productId: number,
        options?: Record<'variant' | 'product' | 'warehouse', number>
    ) {
        return (
            await axios.get<SimpleProductStock[]>(
                `api/v1/list/products/${productId}/stock`,
                { params: options }
            )
        ).data
    }

    async function searchThroughVariants(params?: BCSearchParams) {
        const response = (
            await axios.get<PaginatedResponse<BCProductVariant>>(
                `/api/v1/list/products/barcode-data/variants`,
                { params }
            )
        ).data
        productVariants.value = response
        return response
    }

    return {
        product,
        products,
        productVariant,
        productVariants,
        fetchProduct,
        fetchProducts,
        findVariant,
        fetchVariants,
        createProduct,
        updateProduct,
        findStockByProduct,
        searchThroughVariants,
    }
})
