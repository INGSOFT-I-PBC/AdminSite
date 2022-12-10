<script setup lang="ts">
    import { usePurchaseStore } from '@store/purchase'
    import type { Status, Warehouse } from '@store/types'
    import { useWarehouseStore } from '@store/warehouse'

    import { useRouter } from 'vue-router'
    import { useToast } from 'vue-toastification'

    import { EButton, ECard, ListBox, WaitOverlay } from '@custom-components'

    const showWaitOverlay = ref(true)
    const router = useRouter()

    const purchase = usePurchaseStore()
    const warehouse = useWarehouseStore()
    const toast = useToast()

    const selectedWarehouse = ref<Warehouse>()

    const selectedStatus = ref<Status>()

    warehouse
        .fetchWarehouses()
        .then((): void => {
            showWaitOverlay.value = false
        })
        .catch((): void => {
            toast.error('Error de carga')
            showWaitOverlay.value = false
        })
</script>

<template>
    <WaitOverlay :show="showWaitOverlay">
        <ECard>
            <div class="container">
                <div class="row">
                    <h1 class="title my-2 col-5 dark-mode-text">
                        Bodegas Disponibles
                    </h1>
                </div>
                <div class="row inline-flex">
                    <ListBox
                        class="col-3"
                        v-model="selectedWarehouse"
                        placeholder="Filtro por bodega"
                        label="name"
                        :options="warehouse.getWarehouseList ?? []" />

                    <ListBox
                        class="col-3 tw-capitalize"
                        v-model="selectedStatus"
                        placeholder="Filtro por estado actual"
                        label="display"
                        :options="purchase.getPurchaseStatus() ?? []" />

                    <e-button class="col-2"> Buscar </e-button>
                </div>
            </div>
        </ECard>
    </WaitOverlay>
</template>
<style lang="scss">
    h1.title {
        @apply tw-text-2xl tw-text-black dark:tw-text-neutral-100;
    }

    .smaller-btn-group {
        --bs-list-group-border-width: 1px;
        --bs-list-group-border-radius: 0.25rem;
        --bs-list-group-item-padding-x: 0.8rem;
        --bs-list-group-item-padding-y: 0.3rem;
    }

    .dark-mode-text {
        @apply dark:tw-text-white tw-text-secondary-dark;
    }

    .table {
        > thead {
            @apply tw-bg-secondary tw-text-white tw-font-bold tw-text-sm;
        }

        > tbody {
            @apply tw-text-sm;
        }

        @media (prefers-color-scheme: dark) {
            color: white !important;
            --bs-table-striped-color: theme(colors.zinc.400);
            --bs-table-hover-color: theme('colors.primary.light');
            --bs-table-hover-bg: theme(colors.primary.light / 15%);
        }
    }
</style>
