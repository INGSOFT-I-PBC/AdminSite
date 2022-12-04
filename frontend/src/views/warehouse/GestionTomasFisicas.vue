<script setup lang="ts">
    import type {
        MessageResponse,
        PaginatedResponse,
        Product,
        ProductProps,
        Warehouse,
    } from '@store/types'
    import { isMessage } from '@store/types'
    import { useWarehouseStore } from '@store/warehouse'
    import type { BPagination, BTable, TableField } from 'bootstrap-vue-3'

    import { ref, watch } from 'vue'
    import { useToast } from 'vue-toastification'

    import {
        EButton,
        ECard,
        InputText,
        ListBox,
        ModalDialog,
        WaitOverlay,
    } from '@custom-components'

    type QuantifiedProduct = Product & { quantity: number }
    type SelectionProduct = QuantifiedProduct & { checked: boolean }

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
    const currentPage = ref<number>(0)
    const paginatedTableData = ref<SelectionProduct[]>([])

    const tomaFisicaNotes = ref('')

    const inventoryFields: TableField[] = [
        '#',
        { label: 'Codigo Producto', key: 'sku' },
        'NombreProducto',
        { label: 'Marca', key: 'brand_name' },
        { label: 'Descripción', key: 'short_description' },
        { label: 'Precio Venta', key: 'price' },
        { label: 'Cantidad', key: 'quantity' },
        'Confirmado',
        'Acción',
    ]

    function confirmarCambio() {
        showChangeWhModal.value = false
        invTableData.value = []
        triggerWhChange()
    }
    async function saveTomaFisica() {
        if (!isAllChecked.value && tomaFisicaNotes.value.length < 1) {
            toast.error(
                'Debe ingresar la novedad si no estan todos los productos checkeados',
                { timeout: 4500 }
            )
            return
        }

        showFinishModal.value = false
        showWaitOverlay.value = true

        if (!selectedWarehouse.value) {
            return toast.error('Error de seleccion de bodega', {
                timeout: 2000,
            })
        }

        warehouse
            .saveTomasFisicas({
                novedad: tomaFisicaNotes.value,
                warehouse: selectedWarehouse.value.id,
            })
            .then(() => {
                toast.success('Toma Física guardada correctamente')
                selectedWarehouse.value = undefined
                invTableData.value = []
            })
            .catch((it: MessageResponse) => {
                toast.error(`No se pudo guardar la orden [${it.code}]`)
            })
            .finally(() => {
                showWaitOverlay.value = false
            })
    }

    const isAllChecked = ref(false)
    function checkConfirmedProducts() {
        for (const product of invTableData.value) {
            if (product.checked) continue
            isAllChecked.value = false
            return
        }
        isAllChecked.value = true
        return
    }

    async function triggerWhChange() {
        if (selectedWarehouse.value && invTableData.value.length > 0) {
            showChangeWhModal.value = true
        } else if (selectedWarehouse.value) {
            showWaitOverlay.value = true

            let res = await warehouse.fetchPaginatedProductInventory(
                { warehouse_id: selectedWarehouse.value.id },
                { page: 1, per_page: 100000 }
            )
            if (isMessage(res)) {
                toast.error(res.message + ' ' + res.code, { timeout: 2500 })
                invTableData.value = []
                showWaitOverlay.value = false
                return
            } else if (res.data.length == 0) {
                toast.error('No se ha encontrado registros de inventario', {
                    timeout: 2500,
                })
                showWaitOverlay.value = false
                return
            }
            res = res as PaginatedResponse<QuantifiedProduct>
            const data = res.data as SelectionProduct[]

            for (const product of data) {
                product.checked = false
            }
            toast.success('Inventario cargado', { timeout: 2500 })
            invTableData.value = data
            paginateData()
            cardTitle.value = selectedWarehouse.value.name
            showWaitOverlay.value = false
        } else {
            toast.error('Seleccione una bodega de la lista', { timeout: 2500 })
        }
    }

    function filterData() {
        stopWatcher.value = true
        currentPage.value = 0

        if (searchString.value.length > 0) {
            paginatedTableData.value = (invTableData.value ?? [])
                .filter(product => {
                    return (
                        product.product_name.includes(searchString.value) ||
                        product.variant_name.includes(searchString.value)
                    )
                })
                .slice(
                    currentPage.value * paginateRows.value,
                    (currentPage.value + 1) * paginateRows.value
                )
            stopWatcher.value = false
        } else {
            stopWatcher.value = false
            paginateData()
        }
    }

    function paginateData() {
        if (!stopWatcher.value) {
            paginatedTableData.value = (invTableData.value ?? []).slice(
                currentPage.value * paginateRows.value,
                (currentPage.value + 1) * paginateRows.value
            )
        }
    }

    function checkNewLine() {
        console.log(codeInputString.value)
        if (!codeInputString.value.includes('\n')) {
            return
        }
        const searchStr = codeInputString.value.trim()

        const product_idx = invTableData.value.findIndex(
            product => product.sku === searchStr
        )
        if (product_idx < 0) {
            toast.error('Código no encontrado en este inventario', {
                timeout: 4500,
            })
            codeInputString.value = ''
            return
        }

        if (invTableData.value[product_idx].checked) {
            toast.warning('Producto confirmado previamente', { timeout: 2000 })
            codeInputString.value = ''
            return
        }

        invTableData.value[product_idx].checked = true

        const data_idx = paginatedTableData.value.findIndex(
            product => product.sku === searchStr
        )
        if (data_idx > -1) {
            paginatedTableData.value[data_idx].checked = true
        }
        codeInputString.value = ''
        toast.success('Producto chequeado', { timeout: 2000 })
    }

    warehouse.fetchWarehouses().then(() => {
        showWaitOverlay.value = false
    })

    watch(searchString, filterData)
    watch(codeInputString, checkNewLine)
    watch(currentPage, paginateData)

    function printCheck(checked: any) {
        console.log(checked)
    }
</script>

<template>
    <WaitOverlay :show="showWaitOverlay">
        <ECard>
            <div class="tw-container">
                <div class="row inline-flex">
                    <span
                        class="tw-text-black dark:tw-text-neutral-100 tw-text-lg tw-text-center col-2">
                        Inventario Seleccionado:
                    </span>
                    <ListBox
                        class="col-3"
                        v-model="selectedWarehouse"
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
                            ¿Está seguro que quiere cambiar de inventario?
                        </h1>
                        <h2
                            class="tw-text-2xl tw-text-red-700 dark:tw-text-red-600">
                            Perderá todo el progreso de la toma física actual
                        </h2>
                    </ModalDialog>
                    <ModalDialog
                        id="finish-modal"
                        v-model:show="showFinishModal"
                        title="Terminar Toma Física"
                        ok-text="Guardar"
                        @ok="saveTomaFisica"
                        button-type="ok-cancel">
                        <h2
                            v-if="!isAllChecked"
                            class="tw-text-2xl tw-text-red-700 dark:tw-text-red-600">
                            ADVERTENCIA: Existen productos sin
                            checkear/escanear. Especifique el motivo si desea
                            continuar.
                        </h2>

                        <InputText
                            label="Observaciones de la toma"
                            v-model="tomaFisicaNotes"
                            info-label="Ingrese cualquier novedad de la toma"
                            :status="tomaFisicaNotes.length > 0"
                            info-status="warning" />
                    </ModalDialog>

                    <e-button
                        v-if="invTableData.length < 1"
                        type="button"
                        variant="primary"
                        class="col-1 mx-1 py-1 col-md-3 col-sm-4"
                        @click.left="triggerWhChange">
                        Realizar Toma Física
                    </e-button>
                    <e-button
                        v-else
                        :disabled="selectedWarehouse?.name === cardTitle"
                        type="button"
                        variant="primary"
                        class="col-1 mx-1 py-1 col-md-3 col-sm-4"
                        @click.left="triggerWhChange">
                        Cambiar de inventario
                    </e-button>
                    <e-button
                        v-if="invTableData.length > 0"
                        type="button"
                        variant="primary"
                        class="col-1 mx-1 py-1 col-md-3 col-sm-4"
                        @click.left="
                            () => {
                                checkConfirmedProducts()
                                showFinishModal = true
                            }
                        ">
                        Terminar Toma Física
                    </e-button>
                </div>
                <div class="container mt-3" v-if="invTableData.length < 1">
                    <div
                        class="row align-content-center justify-content-center">
                        <h1 class="title tw-text-center my-2">
                            Elija un inventario para iniciar la toma física
                        </h1>
                        <br />
                        <h2
                            class="tw-text-black dark:tw-text-neutral-100 tw-text-xl tw-text-center my-2">
                            No existen productos cargados
                        </h2>
                    </div>
                </div>

                <div class="container mt-3" v-else>
                    <div
                        class="row align-content-center justify-content-center mb-3">
                        <h1 class="title tw-text-center tw-text-lg col-3">
                            Nueva toma: {{ cardTitle }}
                        </h1>

                        <textarea
                            name="code"
                            v-model="codeInputString"
                            cols="35"
                            rows="1"
                            placeholder="Ingrese un código de producto para marcarlo"
                            class="t-input-text tw-py-1 tw-px-1 tw-bg-transparent min-w-full tw-flex-1">
                        </textarea>
                        <InputText
                            v-model="searchString"
                            info-label="Búsqueda por nombre"
                            info-status="info"
                            class="col-4" />
                    </div>

                    <div class="row">
                        <BTable
                            :fields="inventoryFields"
                            :items="paginatedTableData">
                            <template #cell(#)="{ index }">
                                {{ (index + 1) * (currentPage + 1) }}
                            </template>
                            <template #cell(NombreProducto)="{ item }">
                                {{
                                    item.product_name + '-' + item.variant_name
                                }}
                            </template>
                            <template #cell(Confirmado)="{ item }">
                                <b-form-checkbox
                                    class="tw-text-2xl tw-text-center custom-Check"
                                    v-model="item.checked">
                                    Confirmar
                                </b-form-checkbox>
                            </template>
                            <template #cell(Acción)="{ item }">
                                <e-button
                                    left-icon="fa-eye"
                                    type="button"
                                    variant="primary"
                                    @click.left="printCheck(item)"
                                    >Ver detalles
                                </e-button>
                            </template>
                        </BTable>
                        <div
                            class="row my-3"
                            v-if="paginatedTableData.length == 0">
                            <h1 class="title tw-text-center">
                                No se ha encontrado registros a partir de la
                                búsqueda, vuelva a intentarlo
                            </h1>
                        </div>
                        <b-pagination
                            v-model="currentPage"
                            :total-rows="paginatedTableData.length"
                            :per-page="paginateRows"
                            align="center"
                            :limit="10"
                            hide-goto-end-buttons
                            class="paginator">
                        </b-pagination>
                    </div>
                </div>
            </div>
        </ECard>
    </WaitOverlay>
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
