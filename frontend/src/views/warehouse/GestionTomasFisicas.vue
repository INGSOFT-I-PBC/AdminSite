<script setup lang="ts">
    import type { Warehouse } from '@store/types'
    import { useWarehouseStore } from '@store/warehouse'

    import { ref, watch } from 'vue'

    import { EButton, ECard, ListBox, ModalDialog } from '@custom-components'

    const warehouse = useWarehouseStore()
    const showWaitOverlay = ref(true)
    const showChangeWhModal = ref(false)
    const activeWarehouse = ref<Warehouse>()

    function confirmarCambio() {
        showChangeWhModal.value = false
    }

    function triggerWhChange() {
        console.log(activeWarehouse.value)
    }

    watch(activeWarehouse, triggerWhChange)
    warehouse.fetchWarehouses()
</script>

<template>
    <WaitOverlay :show="showWaitOverlay">
        <ECard>
            <div class="tw-container">
                <div class="row">
                    <ListBox
                        class="col-6"
                        top-label="Inventario Seleccionado"
                        v-model="activeWarehouse"
                        placeholder="Seleccione un inventario a realizar la nueva toma física"
                        label="name"
                        :options="warehouse.getWarehouseList ?? []" />

                    <ModalDialog
                        id="change-modal"
                        v-model:show="showChangeWhModal"
                        title="Confirmar Cambio de Inventario"
                        ok-text="Cambiar"
                        @ok="confirmarCambio()"
                        button-type="ok-cancel">
                        <h1
                            class="tw-text-3xl tw-text-black dark:tw-text-white">
                            Está seguro que quiere cambiar de inventario?
                        </h1>
                        <h2
                            class="tw-text-2xl tw-text-red-700 dark:tw-text-red-600">
                            Perderá todos el progreso de la toma física actual
                        </h2>
                    </ModalDialog>

                    <e-button
                        type="button"
                        variant="primary"
                        class="col-2 mx-2 py-1 col-md-3 col-sm-4">
                        Realizar Toma Física
                    </e-button>
                </div>
            </div>
        </ECard>
    </WaitOverlay>
</template>

<style lang="scss">
    h1.title {
        @apply tw-text-2xl tw-text-black dark:tw-text-neutral-100;
    }
</style>
