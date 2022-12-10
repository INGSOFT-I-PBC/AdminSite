<script setup lang="ts">
    import type { Warehouse, WarehouseStock } from '@store/types'
    import { isMessage } from '@store/types'
    import { useWarehouseStore } from '@store/warehouse'
    import type { TableField } from 'bootstrap-vue-3'

    import { ref, watch } from 'vue'
    import { useToast } from 'vue-toastification'

    import { WaitOverlay } from '@custom-components'

    type SelectionProduct = WarehouseStock & { checked: boolean }

    const toast = useToast()
    const warehouse = useWarehouseStore()
    const showWaitOverlay = ref(true)
    const showChangeWhModal = ref(false)
    const showFinishModal = ref(false)
    const stopWatcher = ref(false)

    const cardTitle = ref<string>('')

    const selectedWarehouse = ref<Warehouse>()

    const codeInputString = ref('')
    const searchString = ref('')
    const invTableData = ref<SelectionProduct[]>([])

    const paginateRows = ref<number>(25)
    const currentPage = ref<number>(1)
    const paginatedTableData = ref<SelectionProduct[]>([])

    const movementsFields: TableField[] = [
        '#',
        'Creada',
        'RealizadaPor',
        'BodegaOrigen',
        'BodegaDestino',
        { label: 'EstadoActual', key: 'status' },
        'Notas',
    ]
    const traceFields: TableField[] = [
        '#',
        'Creada',
        'RealizadaPor',
        'BodegaOrigen',
        'BodegaDestino',
        { label: 'Estado', key: 'status' },
        'Notas',
    ]
</script>

<template>
    <WaitOverlay :show="showWaitOverlay"> </WaitOverlay>
</template>

<style lang="scss">
    .title {
        @apply tw-text-2xl tw-text-black dark:tw-text-neutral-100;
    }

    .custom-Check:checked {
        box-shadow: theme('colors.primary.dark') !important;
        background-color: theme('colors.primary.light') !important;
        border-color: theme('colors.primary.dark') !important;
    }
    .custom-Check:focus {
        box-shadow: 0 0 0 0.25em theme('colors.primary.dark'/25%) !important;

        border-color: theme('colors.primary.dark') !important;
    }
</style>
