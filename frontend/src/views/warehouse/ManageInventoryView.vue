<template>
    <ECard>
        <Title size="2xl">Gestión de inventario</Title>
        <div
            class="tw-h-0.5 tw-w-full tw-bg-secondary dark:tw-bg-primary"></div>
        <WaitOverlay :show="loadingState.waitWarehouse">
            <div class="container">
                <div class="row">
                    <!-- left division -->
                    <div
                        class="col col-3 tw-bg-slate-600 tw-py-2 tw-rounded-lg tw-text-white">
                        <VeeForm>
                            <VeeField
                                label="Hola"
                                name="name"
                                v-slot="{ field, handleChange }">
                                <InputText
                                    label="Búsqueda"
                                    :model-value="field.value as string"
                                    @update:model-value="handleChange" />
                            </VeeField>
                        </VeeForm>
                        <BPagination
                            :total-rows="(warehouseStore.paginatedWarehouse as PaginatedResponse<Warehouse>)?.total"
                            :per-page="paginationData.per_page" />
                    </div>

                    <!-- right division, must contain all the information about the warehouse -->
                    <div class="col">
                        <WaitOverlay :show="loadingState.waitData">
                        </WaitOverlay>
                    </div>
                </div>
            </div>
        </WaitOverlay>
    </ECard>
</template>

<script setup lang="ts">
    import { useWarehouseStore } from '@store'
    import type { PaginatedResponse, Warehouse } from '@store/types'
    import { BPagination } from 'bootstrap-vue-3'

    import { ECard, InputText, Title, WaitOverlay } from '@custom-components'

    const loadingState = ref({
        waitWarehouse: false,
        waitData: false,
    })

    const paginationData = ref<PaginationOptions>({
        page: 1,
        per_page: 10,
    })
    const warehouseStore = useWarehouseStore()
</script>
