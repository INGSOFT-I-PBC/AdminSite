<script setup lang="ts">
    import { useItemStore } from '@store'
    import type {
        MessageResponse,
        PaginatedResponse,
        ProductProps,
        ProductVariant,
        SimpleProduct,
        TomaFisicaDetail,
        Warehouse,
        WarehouseStock,
    } from '@store/types'
    import { isMessage } from '@store/types'
    import { useWarehouseStore } from '@store/warehouse'
    import type { BPagination, BTable, TableField } from 'bootstrap-vue-3'
    import { Form as ValidationForm, useField } from 'vee-validate'
    import * as yup from 'yup'

    import { onMounted, ref, watch } from 'vue'
    import { useRoute } from 'vue-router'
    import { useToast } from 'vue-toastification'

    import {
        EButton,
        ECard,
        InputText,
        ListBox,
        LoadingBar,
        ModalDialog,
        WaitOverlay,
    } from '@custom-components'

    const PENDING_APPROVAL = { name: 'PA', display: 'Aprobación Pendiente' }

    type SelectionProduct = WarehouseStock & {
        checked: boolean
        novedad: string | undefined
        new_stock: number | undefined
        globalIndx: number
    }
    type ModalProduct = {
        product: SimpleProduct | undefined
        variant: ProductVariant | undefined
        props: ProductProps[]
    }

    const router = useRoute()
    const toast = useToast()
    const warehouse = useWarehouseStore()
    const itemStore = useItemStore()

    const showWaitOverlay = ref(true)
    const showChangeWhModal = ref(false)
    const showFinishModal = ref(false)
    const stopWatcher = ref(false)

    const cardTitle = ref<string>('')

    const selectedWarehouse = ref<Warehouse>()
    const selectedProxyWarehouse = ref<Warehouse>()

    const codeInputString = ref('')
    const searchString = ref('')
    const invTableData = ref<SelectionProduct[]>([])

    const paginateRows = ref<number>(25)
    const currentPage = ref<number>(1)
    const paginatedTableData = ref<SelectionProduct[]>([])

    const tomaFisicaNotes = ref('')

    const productForm = ref({
        novedad: useField(
            'novedad',
            yup
                .string()
                .max(300, 'Máximo número de caracteres excedido (300)')
                .required('Ingrese la razón/novedad')
        ),

        new_stock: useField(
            'new_stock',
            yup
                .number()
                .min(0, 'Tiene que ser mayor a 0')
                .required('Ingrese la cantiad nueva')
                .typeError('Ingrese un número entero')
        ),
    })

    const inventoryFields: TableField[] = [
        '#',
        'CódigoProducto',
        'NombreProducto',
        'Marca',
        'Descripción',
        'PrecioDeVenta',
        'Stock',
        'Confirmado',
        'Acción',
    ]
    /**
     * Manager to confirm the warehouse change. Hides the popup modal and resets the data
     */
    function confirmarCambio() {
        showChangeWhModal.value = false
        invTableData.value = []
        triggerWhChange()
    }
    const loadingProps = ref(true)
    /**
     * Contains the information of the selected product to be displayed in the product modal
     */
    const detailSelectedProduct = ref<ModalProduct>({
        product: undefined,
        variant: undefined,
        props: [],
    })

    const productInfoShow = ref(false)

    /**
     * Loads product info to the modal popup
     * @param product WarehouseStock with and ProductVariant to fetch the props of
     */
    async function showProduct(product: WarehouseStock): Promise<void> {
        detailSelectedProduct.value.product = product.product
        detailSelectedProduct.value.variant = product.variant
        productInfoShow.value = true
        detailSelectedProduct.value.props = []
        loadingProps.value = true
        let res = await itemStore.fetchProductProperties({
            variant_id: product.variant.id,
        })
        if (isMessage(res)) {
            loadingProps.value = false
            detailSelectedProduct.value.props[0] = {
                name: 'Error',
                value: 'No se pudo cargar los detalles',
            }
        } else {
            res = res as PaginatedResponse<ProductProps>
            detailSelectedProduct.value.props = res.data
            loadingProps.value = false
        }
    }

    const selectedNovedadProduct = ref<SelectionProduct>()
    const showNovedadModal = ref(false)

    /**
     * Handler for the novedad modal of each item.
     * @param product Product of the row clicked
     */
    function showNovedad(product: SelectionProduct) {
        selectedNovedadProduct.value = product
        showNovedadModal.value = true
    }

    function cancelNovedad() {
        if (selectedNovedadProduct.value?.globalIndx != undefined) {
            invTableData.value[
                selectedNovedadProduct.value?.globalIndx
            ].novedad = undefined
        }
    }
    /**
     * Contains all the products wiht a non null novedad parameter. Used to display information in the finish toma modal popup
     */

    const productsWithNovedad = ref<SelectionProduct[]>([])
    /**
     * Sets the array of the products with novedad parameter filtering the invTableData for later use.
     */
    function setProductsNovedad() {
        productsWithNovedad.value = invTableData.value.filter(product => {
            return product.novedad != undefined
        })
    }
    /**
     * Sets the novedad parameter of the selected product to the corresponding product in the global array
     * invTableData. Used after the confirm button modal popup after clicking the modify button in the table.
     */

    async function saveDetalleProducto() {
        const isValidStock = await productForm.value.new_stock.validate()
        const isValidNovedad = await productForm.value.novedad.validate()
        const isValid = isValidNovedad.valid && isValidStock.valid

        if (selectedNovedadProduct.value?.globalIndx != undefined && isValid) {
            invTableData.value[
                selectedNovedadProduct.value?.globalIndx
            ].novedad = productForm.value.novedad.value
            invTableData.value[
                selectedNovedadProduct.value?.globalIndx
            ].new_stock = productForm.value.new_stock.value

            productForm.value.new_stock.resetField()
            productForm.value.novedad.resetField()
            toast.success('Novedad registrada', { timeout: 2000 })
            showNovedadModal.value = false
        } else if (isValid) {
            toast.error('Verifique la novedad y cantidad ingresados')
        } else {
            toast.error('Error, vuelva a intentarlo')
            showNovedadModal.value = false
        }
    }

    /**
     * Transform de key to a more readable Form
     * @param key Key name of Product or VariantProduct to be formated
     */
    function keyNaturalName(key: string): string {
        switch (key) {
            case 'product_name':
                return 'Producto'
            case 'variant_name':
                return 'Variante'
            case 'summary':
                return 'Descripción'
            case 'short_description':
                return 'Descripción Corta'
            case 'brand_name':
                return 'Marca'
            case 'base_price':
                return 'Precio Base'
            case 'price':
                return 'Precio de venta'
            case 'sku':
                return 'Código(sku)'
        }
        return key
    }

    /**
     * Checks if the information can be saved. If so, calls the warehouse method with the final information of the
     * toma fisica
     */

    async function saveTomaFisica() {
        showFinishModal.value = false
        showWaitOverlay.value = true

        if (!selectedWarehouse.value) {
            return toast.error('Error de seleccion de bodega', {
                timeout: 2000,
            })
        }
        let detailsQueryArray: undefined | TomaFisicaDetail[]

        if (productsWithNovedad.value.length > 0) {
            detailsQueryArray = []
            for (const detail of productsWithNovedad.value) {
                detailsQueryArray.push({
                    product: detail.product.id,
                    variant: detail.variant.id,
                    new_stock: detail.new_stock
                        ? detail.new_stock
                        : detail.stock_level,
                    previous_stock: detail.stock_level,
                    novedad: detail.novedad ? detail.novedad : 'N/A',
                    acepted: PENDING_APPROVAL.name,
                })
            }
        }

        warehouse
            .saveTomasFisicas({
                novedad: tomaFisicaNotes.value,
                warehouse: selectedWarehouse.value.id,
                details: detailsQueryArray,
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
    /**
     * Flag: All products in the table are checked, used to show a warning message in the popup modal
     */
    const isAllChecked = ref(false)
    /**
     * Checks if a prodcut that has not been checked , has a note attached to it.
     * Calls the setProductsNovedad and shows the modal if the informations is correct
     */
    function checkConfirmedProducts() {
        setProductsNovedad()
        isAllChecked.value = true
        for (const product of invTableData.value) {
            if (!product.novedad && product.checked) continue
            if (!product.novedad && !product.checked) {
                toast.error(
                    'Producto no checkeado y sin novedad registrada: ' +
                        product.product.product_name +
                        '/' +
                        product.variant.variant_name
                )
                return
            }
            isAllChecked.value = false
        }
        showFinishModal.value = true
        return
    }

    /**
     * Shows the confirm change modal and changes the data if the user confirms
     */

    async function triggerWhChange() {
        if (
            selectedWarehouse.value &&
            invTableData.value.length > 0 &&
            selectedProxyWarehouse.value != selectedWarehouse.value
        ) {
            selectedWarehouse.value = selectedProxyWarehouse.value
            showChangeWhModal.value = true
            return
        } else if (selectedProxyWarehouse.value) {
            showWaitOverlay.value = true

            selectedWarehouse.value = selectedProxyWarehouse.value

            let res = await warehouse.fetchPaginatedWarehouseInventory(
                { warehouse_id: selectedProxyWarehouse.value.id },
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
            res = res as PaginatedResponse<WarehouseStock>
            const data = res.data as SelectionProduct[]
            let idx = 0
            for (const product of data) {
                product.globalIndx = idx
                product.checked = false
                idx += 1
            }
            toast.success('Inventario cargado', { timeout: 2500 })
            invTableData.value = data
            paginateData()
            cardTitle.value = selectedWarehouse.value.name
            showWaitOverlay.value = false
        } else {
            toast.error('Seleccione una bodega de la lista', { timeout: 2500 })
        }
        showWaitOverlay.value = false
    }
    /**
     * Filters the tomas fisicas data and paginates it in the main table via the user input string
     */
    function filterData() {
        stopWatcher.value = true
        currentPage.value = 1
        if (searchString.value.length > 0) {
            paginatedTableData.value = (invTableData.value ?? [])
                .filter(whStock => {
                    return (
                        whStock.product.product_name.includes(
                            searchString.value
                        ) ||
                        whStock.variant.variant_name.includes(
                            searchString.value
                        )
                    )
                })
                .slice(
                    (currentPage.value - 1) * paginateRows.value,
                    currentPage.value * paginateRows.value
                )
            stopWatcher.value = false
        } else {
            stopWatcher.value = false
            paginateData()
        }
    }
    /**
     * Paginates the data shown in the main table
     */
    function paginateData() {
        if (!stopWatcher.value) {
            paginatedTableData.value = (invTableData.value ?? []).slice(
                (currentPage.value - 1) * paginateRows.value,
                currentPage.value * paginateRows.value
            )
        }
    }
    /**
     * Checks if the inserte code string has a new line character
     */
    function checkNewLine() {
        if (!codeInputString.value.includes('\n')) {
            return
        }
        const searchStr = codeInputString.value.trim()

        const product_idx = invTableData.value.findIndex(
            product => product.variant.sku === searchStr
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
            product => product.variant.sku === searchStr
        )
        if (data_idx > -1) {
            paginatedTableData.value[data_idx].checked = true
        }
        codeInputString.value = ''
        toast.success('Producto chequeado', { timeout: 2000 })
    }

    watch(searchString, filterData)
    watch(codeInputString, checkNewLine)
    watch(currentPage, paginateData)
    onMounted(() => {
        const warehouse_id = router.params.id
        warehouse
            .fetchWarehouses()
            .then(() => {
                showWaitOverlay.value = false
                if (warehouse_id.length > 0 && warehouse.getWarehouseList) {
                    selectedWarehouse.value = warehouse.getWarehouseList.find(
                        wh => (wh.id = Number(warehouse_id))
                    )
                    triggerWhChange()
                }
            })
            .catch(e => {
                toast.error('Error de carga')
                showWaitOverlay.value = false
            })
    })
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
                        v-model="selectedProxyWarehouse"
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
                        size="3xl"
                        id="finish-modal"
                        v-model:show="showFinishModal"
                        title="Terminar Toma Física"
                        ok-text="Guardar"
                        @ok="saveTomaFisica"
                        button-type="ok-cancel">
                        <h2
                            v-if="!isAllChecked"
                            class="tw-text-xl tw-text-red-700 dark:tw-text-red-600">
                            Es recomendable escribir que se registraron
                            novedades en la caja de texto al final. Items que
                            registran cambios:
                        </h2>
                        <template
                            v-for="(product, idx) in productsWithNovedad"
                            :key="idx">
                            <span class="tw-w-1/2 col-6 dark-mode-text"
                                >{{
                                    product.product.product_name +
                                    '/' +
                                    product.variant.variant_name
                                }}
                            </span>
                            <div
                                class="tw-rounded tw-ring-1 tw-ring-yellow-400 tw-py-1 col-12 mb-2">
                                <div class="row mb-1">
                                    <span
                                        class="tw-font-bold mx-2 col-2 dark-mode-text"
                                        >Stock actual:
                                    </span>
                                    <span class="mx-2 col-2 dark-mode-text">
                                        {{ product.stock_level }}
                                    </span>

                                    <span
                                        class="tw-font-bold col-2 dark-mode-text">
                                        Nuevo stock:
                                    </span>

                                    <span class="col-2 dark-mode-text">{{
                                        product.new_stock
                                    }}</span>
                                </div>
                                <div class="row">
                                    <span
                                        class="tw-font-bold col-2 dark-mode-text mx-2">
                                        Novedad:
                                    </span>
                                    <div
                                        class="overflow-hidden text-break text-wrap dark-mode-text col-8 text-right">
                                        {{ product.novedad }}
                                    </div>
                                </div>
                            </div>
                        </template>
                        <InputText
                            class="dark-mode-text"
                            label="Observaciones de la toma"
                            v-model="tomaFisicaNotes"
                            info-label="Ingrese novedad de la toma"
                            :status="productsWithNovedad.length > 0"
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
                        :disabled="selectedProxyWarehouse?.name === cardTitle"
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
                        @click.left="checkConfirmedProducts">
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
                        <ModalDialog v-model:show="productInfoShow" size="3xl">
                            <template #dialog-title>
                                <b class="tw-text-2xl dark-mode-text"
                                    >Detalle del producto
                                    {{
                                        detailSelectedProduct.product
                                            ?.product_name +
                                        '/' +
                                        detailSelectedProduct.variant
                                            ?.variant_name
                                    }}</b
                                >
                            </template>
                            <div class="container">
                                <h3
                                    class="tw-text-xl tw-font-bold dark-mode-text">
                                    Detalle
                                </h3>
                                <div
                                    class="row tw-pb-3 align-content-center justify-content-center gy-2">
                                    <template
                                        v-for="(
                                            d, k
                                        ) in detailSelectedProduct.product"
                                        :key="k">
                                        <div
                                            class="tw-rounded tw-ring-1 tw-ring-yellow-400 tw-py-1 col-12 col-md-5 tw-mx-2"
                                            v-if="
                                                !['id', 'base_price'].includes(
                                                    k
                                                )
                                            ">
                                            <div class="row">
                                                <span
                                                    class="tw-w-1/2 tw-font-bold col-6 dark-mode-text"
                                                    >{{
                                                        keyNaturalName(k)
                                                    }}:</span
                                                >
                                                <span
                                                    class="col-6 dark-mode-text"
                                                    >{{ d }}</span
                                                >
                                            </div>
                                        </div>
                                    </template>
                                    <template
                                        v-for="(
                                            d, k
                                        ) in detailSelectedProduct.variant"
                                        :key="k">
                                        <div
                                            class="tw-rounded tw-ring-1 tw-ring-yellow-400 tw-py-1 col-12 col-md-5 tw-mx-2"
                                            v-if="
                                                ![
                                                    'id',
                                                    'base_price',
                                                    'created_at',
                                                    'updated_at',
                                                    'is_active',
                                                    'deleted_at',
                                                ].includes(k)
                                            ">
                                            <div class="row">
                                                <span
                                                    class="tw-font-bold col-5 dark-mode-text tw-gap-x-2"
                                                    >{{
                                                        keyNaturalName(k)
                                                    }}:</span
                                                >
                                                <span
                                                    class="col-5 dark-mode-text"
                                                    >{{ d }}</span
                                                >
                                            </div>
                                        </div>
                                    </template>
                                </div>
                                <LoadingBar
                                    v-show="loadingProps"
                                    class="tw-mt-5" />
                                <div
                                    v-if="detailSelectedProduct.props"
                                    class="tw-ring-1 tw-ring-yellow-400 tw-rounded tw-pb-3 row">
                                    <h3
                                        class="col-12 tw-text-xl tw-py-1.5 dark-mode-text">
                                        <b>Características del Producto</b>
                                    </h3>
                                    <template
                                        v-for="(
                                            param, idx
                                        ) in detailSelectedProduct.props"
                                        :key="idx">
                                        <div
                                            class="col-6 col-md-3 col-xl-3 tw-text-md dark-mode-text">
                                            <b>{{ param.name }}:</b>
                                        </div>
                                        <div
                                            class="col-6 col-md-3 col-xl-2 dark-mode-text">
                                            {{ param.value }}
                                        </div>
                                    </template>
                                </div>
                            </div>
                        </ModalDialog>
                        <ModalDialog
                            @cancel="cancelNovedad"
                            cancel-text="Eliminar Novedad"
                            clas="dark-mode-text"
                            id="novedad-modal"
                            v-model:show="showNovedadModal"
                            title="Añadir Novedad"
                            button-type="cancel-only">
                            <h2 class="tw-text-2xl tw-font-bold dark-mode-text">
                                Ingrese el nuevo stock y la razón del cambio:
                            </h2>
                            <div class="row">
                                <ValidationForm
                                    @submit="saveDetalleProducto"
                                    :validation-schema="productForm">
                                    <div class="row">
                                        <InputText
                                            class="dark-mode-text text-break"
                                            label="Novedad"
                                            v-model="productForm.novedad.value"
                                            :info-label="
                                                productForm.novedad.errorMessage
                                            "
                                            :status="
                                                Boolean(
                                                    productForm.novedad
                                                        .errorMessage
                                                )
                                            "
                                            info-status="danger" />
                                    </div>
                                    <div class="row">
                                        <InputText
                                            class="dark-mode-text"
                                            :label="
                                                'Cambio de stock (actual: ' +
                                                selectedNovedadProduct?.stock_level +
                                                ')'
                                            "
                                            v-model="
                                                productForm.new_stock.value
                                            "
                                            :info-label="
                                                productForm.new_stock
                                                    .errorMessage
                                            "
                                            :status="
                                                Boolean(
                                                    productForm.new_stock
                                                        .errorMessage
                                                )
                                            "
                                            info-status="danger" />
                                        <div
                                            class="flex-column mt-4 d-flex align-items-end">
                                            <e-button
                                                variant="success"
                                                class="dark-mode-text col-4">
                                                Confirmar Novedad
                                            </e-button>
                                        </div>
                                    </div>
                                </ValidationForm>
                            </div>
                        </ModalDialog>
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
                            outline
                            :fields="inventoryFields"
                            :items="paginatedTableData">
                            <template #cell(#)="{ index }">
                                {{
                                    index + 1 + (currentPage - 1) * paginateRows
                                }}
                            </template>
                            <template #cell(CódigoProducto)="{ item }">
                                {{ item.variant.sku }}
                            </template>
                            <template #cell(NombreProducto)="{ item }">
                                {{
                                    item.product.product_name +
                                    '/' +
                                    item.variant.variant_name
                                }}
                            </template>
                            <template #cell(Marca)="{ item }">
                                {{ item.product.brand_name }}
                            </template>
                            <template #cell(PrecioDeVenta)="{ item }">
                                {{ Number(item.variant.price).toFixed(2) }}
                            </template>
                            <template #cell(Descripción)="{ item }">
                                {{ item.product.short_description }}
                            </template>
                            <template #cell(Stock)="{ item }">
                                <b class="tw-font-bold tw-text-lg">
                                    {{ item.stock_level }}
                                </b>
                            </template>
                            <template #cell(Confirmado)="{ item }">
                                <b-form-checkbox
                                    class="tw-text-2xl tw-text-center custom-Check"
                                    v-model="item.checked">
                                </b-form-checkbox>
                            </template>
                            <template #cell(Acción)="{ item }">
                                <div class="d-flex">
                                    <e-button
                                        left-icon="fa-eye"
                                        type="button"
                                        variant="primary"
                                        class="px-0"
                                        @click.left="showProduct(item)"
                                        >Ver detalles
                                    </e-button>
                                    <e-button
                                        left-icon="warning"
                                        type="button"
                                        class="px-0"
                                        variant="cancel"
                                        @click.left="showNovedad(item)"
                                        >Modificar Novedad
                                    </e-button>
                                </div>
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
                            v-if="searchString.length > 0"
                            v-model="currentPage"
                            :total-rows="paginatedTableData.length"
                            :per-page="paginateRows"
                            align="center"
                            :limit="10"
                            hide-goto-end-buttons
                            class="paginator">
                        </b-pagination>
                        <b-pagination
                            v-else
                            v-model="currentPage"
                            :total-rows="invTableData.length"
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

    .dark-mode-text {
        @apply dark:tw-text-white tw-text-secondary-dark;
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
