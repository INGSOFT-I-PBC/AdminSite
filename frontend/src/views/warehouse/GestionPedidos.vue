<script setup lang="ts">
    import { inventory } from '@/router/routes/inventory'
    import { useItemStore } from '@/store'
    import {
        type Item,
        type MessageResponse,
        type Movement,
        type Purchase,
        type TomaFisica,
        type Warehouse,
        type WhWithTomaFisica,
        isMessage,
    } from '@store/types'
    import type { ItemProps } from '@store/types/items.model'
    import { useWarehouseStore } from '@store/warehouse'
    import Datepicker from '@vuepic/vue-datepicker'
    import {
        BForm,
        BFormCheckbox,
        BFormInput,
        BListGroup,
        BListGroupItem,
        BPagination,
        BTab,
        BTable,
        BTabs,
        type TableField,
    } from 'bootstrap-vue-3'
    import { max } from 'date-fns'
    import {
        type FieldContext,
        Form as ValidationForm,
        useField,
    } from 'vee-validate'
    import { resourceLimits } from 'worker_threads'
    import * as yup from 'yup'

    import { registerRuntimeCompiler } from 'vue'
    import { useToast } from 'vue-toastification'

    import {
        EButton,
        ECard,
        ECol,
        ETab,
        InputText,
        ListBox,
        ModalDialog,
        UserCardItem,
        WaitOverlay,
    } from '@custom-components'

    const DELIVERED_PURCHASE_STATUS = ref('entregado')

    type SelectedItem = { item: Item | null; props: ItemProps[] }
    type QuantifiedItem = Item & { quantity: number }

    type whCardController = {
        currentPage: number
        totalRows: number
    }

    type warehouseInformation = {
        bodega: Warehouse
        inventory: QuantifiedItem[]
        purchases: Purchase[]
        tomasFisicas: TomaFisica[]
        movements: Movement[]
    }

    const toast = useToast()

    const showWaitOverlay = ref(true)

    const purchaseModalShow = ref(false)

    const selectedPurchase = ref<Purchase>()

    const warehouse = useWarehouseStore()

    const itemStore = useItemStore()

    const whPageCount = ref(15)

    const showAllWarehouses = ref(true)

    const whInformationPerPage = ref(15)

    const detailSelectedItem = ref<SelectedItem>({
        item: null,
        props: [],
    })

    const allWarehousesFields: TableField[] = [
        '#',
        { label: 'Nombre', key: 'name' },
        'FechaTomaFisica',
        'RealizadaPor',
        'Novedad',
        'Detalles',
    ]

    const inventoryFields: TableField[] = [
        '#',
        { label: 'Codigo Producto', key: 'codename' },
        { label: 'Nombre Producto', key: 'name' },
        { label: 'Stock', key: 'quantity' },
        { label: 'Precio', key: 'price' },
        'PVenta',
        'Acciones',
    ]

    const purchasesFields: TableField[] = [
        '#',
        'FechaCreación',
        { label: 'Codigo Orden', key: 'reference' },
        'Proveedor',
        'Entregado',
        'Pago',
        'FechaPago',
        'Acciones',
    ]

    const tomasFisFields: TableField[] = [
        '#',
        'FechaRealizacion',
        'RealizadaPor',
        { label: 'Novedad', key: 'novedad' },
        'Acciones',
    ]

    const movementsFields: TableField[] = [
        '#',
        'Creada',
        'RealizadaPor',
        'BodegaRelacionada',
        'TipoDeMovimiento',
        { label: 'Estado', key: 'status' },
        'Notas',
    ]

    let allWarehousesTableInformation: WhWithTomaFisica[] = []

    const currentAsidePage = ref(1)
    const whRows = ref(0)
    const paginatedWarehouse = ref()
    const activeWharehouseButton = ref(-1)

    const paginatedMainTable = ref()

    const mainPageController = ref<whCardController>({
        currentPage: 1,
        totalRows: whRows.value,
    })

    const activeWhInformation = ref<warehouseInformation>({
        bodega: {
            id: -1,
            name: 'Not Selected',
            status: { description: '', name: '', id: '' },
        },
        inventory: [],
        purchases: [],
        tomasFisicas: [],
        movements: [],
    })

    const invTabController = ref<whCardController>({
        currentPage: 1,
        totalRows: 15,
    })

    const tomasFisicasTabController = ref<whCardController>({
        currentPage: 1,
        totalRows: 15,
    })

    const purchaseTabController = ref<whCardController>({
        currentPage: 1,
        totalRows: 15,
    })

    const movementTabController = ref<whCardController>({
        currentPage: 1,
        totalRows: 15,
    })

    const arrayControllers = [
        invTabController.value,
        tomasFisicasTabController.value,
        purchaseTabController.value,
        movementTabController.value,
    ]

    const inventoryForm = ref({
        from_date: useField(
            'from_date',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr, orig) => (orig === '' ? null : curr))
                .typeError('Fecha Invalida')
        ),
        to_date: useField(
            'to_date',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr, orig) => (orig === '' ? null : curr))
                .typeError('Fecha Invalida')
        ),
        name: useField('name', yup.string().optional().nullable(true)),
        codename: useField('codename', yup.string().optional().nullable(true)),
        min_quantity: useField(
            'min_quantity',
            yup
                .number()
                .min(0, 'Tiene que ser mayor a 0')
                .optional()
                .transform((curr, orig) => (orig === '' ? undefined : curr))
                .typeError('Ingrese un número entero')
        ),
        max_quantity: useField(
            'max_quantity',
            yup
                .number()
                .min(0, 'Tiene que ser mayor a 1')
                .optional()
                .transform((curr, orig) => (orig === '' ? undefined : curr))
                .typeError('Ingrese un número entero')
        ),
        min_price: useField(
            'min_price',
            yup
                .number()
                .min(0, 'Tiene que ser mayor a 0')
                .optional()
                .transform((curr, orig) => (orig === '' ? undefined : curr))
                .typeError('Ingrese un número')
        ),
        max_price: useField(
            'max_price',
            yup
                .number()
                .min(0, 'Tiene que ser mayor a 0')
                .optional()
                .transform((curr, orig) => (orig === '' ? undefined : curr))
                .typeError('Ingrese un número')
        ),
    })
    const priceRangeError = computed(() => {
        const f = inventoryForm.value

        return f.max_price.value != '' &&
            f.min_price.value != '' &&
            f.max_price.value <= f.min_price.value
            ? 'Precio máximo tiene que ser mayor al mínimo'
            : f.max_price.errorMessage
    })
    const quantityRangeError = computed(() => {
        const f = inventoryForm.value
        return f.max_quantity.value != '' &&
            f.min_quantity.value != '' &&
            f.max_quantity.value <= f.min_quantity.value
            ? 'Cantidad máxima tiene que ser mayor al minimo'
            : f.max_quantity.errorMessage
    })

    const purchaseForm = ref({
        from_date: useField(
            'to_date_p',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr, orig) => (orig === '' ? null : curr))
                .typeError('Fecha Invalida')
        ),
        to_date: useField(
            'to_date_p',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr, orig) => (orig === '' ? null : curr))
                .typeError('Fecha Invalida')
        ),
        aproved_date: true,
        invoice_date: false,
        provider_name: useField(
            'provider_name',
            yup.string().optional().nullable(true)
        ),
        status: useField('status_p', yup.string().optional().nullable(true)),
        invoice_code: useField(
            'invoice_code',
            yup.string().optional().nullable(true)
        ),
        reference: useField(
            'reference',
            yup
                .number()
                .optional()
                .transform((curr, orig) => (orig === '' ? undefined : curr))
                .typeError('Ingrese un número entero')
        ),
    })
    const tomasFisicasForm = ref({
        from_date: useField(
            'to_date_t',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr, orig) => (orig === '' ? null : curr))
                .typeError('Fecha Invalida')
        ),
        to_date: useField(
            'to_date_t',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr, orig) => (orig === '' ? null : curr))
                .typeError('Fecha Invalida')
        ),
        done_by_name: useField(
            'done_by_name',
            yup.string().optional().nullable(true)
        ),
        novedad: useField('novedad', yup.string().optional().nullable(true)),
    })
    const movementForm = ref({
        from_date: useField(
            'to_date_m',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr, orig) => (orig === '' ? null : curr))
                .typeError('Fecha Invalida')
        ),
        to_date: useField(
            'to_date_m',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr, orig) => (orig === '' ? null : curr))
                .typeError('Fecha Invalida')
        ),
        entrada: false,
        salida: false,
        done_by_name: useField(
            'done_by_name_m',
            yup.string().optional().nullable(true)
        ),
        warehouse_name: useField(
            'warehouse_name_m',
            yup.string().optional().nullable(true)
        ),
        status: useField('status_m', yup.string().optional().nullable(true)),
        notes: useField('reference', yup.string().optional().nullable(true)),
    })

    const itemInfoShow = ref(false)

    function paginateAside(page_size: number, page_number: number) {
        paginatedWarehouse.value = (warehouse.getWarehouseList ?? []).slice(
            page_number * page_size,
            (page_number + 1) * page_size
        )
    }

    function onAsidePageChanged(event: Event, page: number) {
        paginateAside(whPageCount.value, page - 1)
    }

    function paginateMain(page_size: number, page_number: number) {
        paginatedMainTable.value = allWarehousesTableInformation.slice(
            page_number * page_size,
            (page_number + 1) * page_size
        )
    }

    function onMainPageChanged(event: Event, page: number): void {
        paginateMain(whPageCount.value, page - 1)
    }

    function resetWhData(): void {
        for (const controller of arrayControllers) {
            ;(controller.currentPage = 1), (controller.totalRows = 1)
        }
    }

    async function fetchManager(
        tabOption: string,
        query: any,
        paginated_opt: PaginationOptions
    ): Promise<void> {
        switch (tabOption) {
            case 'inventory': {
                const res = await warehouse.fetchPaginatedWarehouseInventory(
                    query,
                    paginated_opt
                )
                activeWhInformation.value.inventory = res.data.data
                invTabController.value.totalRows = res.data.total
                break
            }
            case 'purchases': {
                const res = await warehouse.fetchPaginatedWarehousePurchase(
                    query,
                    paginated_opt
                )
                activeWhInformation.value.purchases = res.data.data
                purchaseTabController.value.totalRows = res.data.total
                break
            }
            case 'tomas-fisicas': {
                const res = await warehouse.fetchPaginatedWarehouseTomasFisicas(
                    query,
                    paginated_opt
                )
                activeWhInformation.value.tomasFisicas = res.data.data
                tomasFisicasTabController.value.totalRows = res.data.total
                break
            }
            case 'movements': {
                query.entrada = true
                query.salida = true
                const res = await warehouse.fetchPaginatedWarehouseMovements(
                    query,
                    paginated_opt
                )
                activeWhInformation.value.movements = res.data.data
                movementTabController.value.totalRows = res.data.total
                break
            }
        }
    }

    async function onSubmit(
        tabOption: string,
        controller: whCardController
    ): Promise<void> {
        showWaitOverlay.value = true
        const query: Record<string, any> = {
            warehouse_id: activeWhInformation.value.bodega.id,
        }
        showWaitOverlay.value = true
        switch (tabOption) {
            case 'inventory': {
                const f = inventoryForm.value
                if (
                    f.name.errorMessage ||
                    f.codename.errorMessage ||
                    f.min_price.errorMessage ||
                    f.min_quantity.errorMessage ||
                    f.from_date.errorMessage ||
                    f.to_date.errorMessage ||
                    priceRangeError.value ||
                    quantityRangeError.value
                ) {
                    toast.error('Verifique los datos antes buscar')
                    showWaitOverlay.value = false
                    return
                }
                query.name = f.name.value
                query.codename = f.codename.value as number
                query.max_price = f.max_price.value as number
                query.min_price = f.min_price.value as number
                query.max_quantity = f.max_quantity.value as number
                query.min_quantity = f.min_quantity.value as number
                query.from_date = f.from_date.value
                query.to_date = f.to_date.value
                fetchManager(tabOption, query, { per_page: 15, page: 1 })
                    .then(() => {
                        if (activeWhInformation.value.inventory.length < 1) {
                            toast.error(
                                'No se ha encontrado registros en la busqueda'
                            )
                        } else {
                            toast.success('Busqueda exitosa')
                        }
                    })
                    .catch(err => {
                        if (isMessage(err)) {
                            toast.error(err.message)
                        } else {
                            toast.error('Error desconocido')
                        }
                    })
                    .finally(() => {
                        showWaitOverlay.value = false
                    })
                break
            }
            case 'purchases': {
                const f = purchaseForm.value
                if (
                    f.from_date.errorMessage ||
                    f.to_date.errorMessage ||
                    f.provider_name.errorMessage ||
                    f.status.errorMessage ||
                    f.invoice_code.errorMessage ||
                    f.reference.errorMessage
                ) {
                    toast.error('Verifique los datos antes buscar')
                    showWaitOverlay.value = false
                    return
                } else if (!f.aproved_date && !f.invoice_date) {
                    toast.error('Marque un tipo de busqueda por fecha')
                    showWaitOverlay.value = false
                    return
                }
                query.from_date = f.from_date.value
                query.to_date = f.to_date.value
                query.aproved_date = f.aproved_date
                query.invoice_date = f.invoice_date
                query.provider_name = f.provider_name.value
                query.status = f.status.value
                query.invoice_code = f.invoice_code.value
                query.reference = f.reference.value as number
                fetchManager(tabOption, query, { per_page: 15, page: 1 })
                    .then(() => {
                        if (activeWhInformation.value.purchases.length < 1) {
                            toast.error(
                                'No se ha encontrado registros en la busqueda'
                            )
                        } else {
                            toast.success('Busqueda exitosa')
                        }
                    })
                    .catch(err => {
                        if (isMessage(err)) {
                            toast.error(err.message)
                        } else {
                            toast.error('Error desconocido')
                        }
                    })
                    .finally(() => {
                        showWaitOverlay.value = false
                    })

                break
            }
            case 'tomas-fisicas': {
                const f = tomasFisicasForm.value
                if (
                    f.from_date.errorMessage ||
                    f.to_date.errorMessage ||
                    f.done_by_name.errorMessage ||
                    f.novedad.errorMessage
                ) {
                    toast.error('Verifique los datos antes buscar')
                    showWaitOverlay.value = false
                    return
                }
                query.from_date = f.from_date.value
                query.to_date = f.to_date.value
                query.done_by_name = f.done_by_name.value
                query.novedad = f.novedad.value

                fetchManager(tabOption, query, { per_page: 15, page: 1 })
                    .then(() => {
                        if (activeWhInformation.value.tomasFisicas.length < 1) {
                            toast.error(
                                'No se ha encontrado registros en la busqueda'
                            )
                        } else {
                            toast.success('Busqueda exitosa')
                        }
                    })
                    .catch(err => {
                        if (isMessage(err)) {
                            toast.error(err.message)
                        } else {
                            toast.error('Error desconocido')
                        }
                    })
                    .finally(() => {
                        showWaitOverlay.value = false
                    })
                break
            }
            case 'movements': {
                const f = movementForm.value
                if (
                    f.from_date.errorMessage ||
                    f.to_date.errorMessage ||
                    f.done_by_name.errorMessage ||
                    f.warehouse_name.errorMessage ||
                    f.status.errorMessage ||
                    f.notes.errorMessage
                ) {
                    toast.error('Verifique los datos antes buscar')
                    showWaitOverlay.value = false
                    return
                }
                query.from_date = f.from_date.value
                query.to_date = f.to_date.value
                query.done_by_name = f.done_by_name.value
                query.notas = f.notes.value
                query.warehouse_name = f.warehouse_name.value
                query.status = f.status.value
                query.entrada = f.entrada
                query.salida = f.salida
                fetchManager(tabOption, query, { per_page: 15, page: 1 })
                    .then(() => {
                        if (activeWhInformation.value.movements.length < 1) {
                            toast.error(
                                'No se ha encontrado registros en la busqueda'
                            )
                        } else {
                            toast.success('Busqueda exitosa')
                        }
                    })
                    .catch(err => {
                        if (isMessage(err)) {
                            toast.error(err.message)
                        } else {
                            toast.error('Error desconocido')
                        }
                    })
                    .finally(() => {
                        showWaitOverlay.value = false
                    })

                break
            }
        }
        await fetchManager(
            tabOption,
            { warehouse_id: activeWhInformation.value.bodega.id },
            { page: 1, per_page: whInformationPerPage.value }
        )

        controller.currentPage = 1

        fetchManager(tabOption, query, { page: 1, per_page: 20 })

        showWaitOverlay.value = false
    }

    async function onReset(
        controller: whCardController,
        tabOption: string
    ): Promise<void> {
        showWaitOverlay.value = true
        switch (tabOption) {
            case 'inventory': {
                inventoryForm.value.name.resetField()
                inventoryForm.value.codename.resetField()
                inventoryForm.value.max_price.resetField()
                inventoryForm.value.min_price.resetField()
                inventoryForm.value.max_quantity.resetField()
                inventoryForm.value.min_quantity.resetField()
                inventoryForm.value.from_date.resetField()
                inventoryForm.value.to_date.resetField()
                break
            }
            case 'purchases': {
                purchaseForm.value.from_date.resetField()
                purchaseForm.value.to_date.resetField()
                purchaseForm.value.aproved_date = false
                purchaseForm.value.invoice_date = false
                purchaseForm.value.provider_name.resetField()
                purchaseForm.value.status.resetField()
                purchaseForm.value.invoice_code.resetField()
                purchaseForm.value.reference.resetField()
                break
            }
            case 'tomas-fisicas': {
                tomasFisicasForm.value.from_date.resetField()
                tomasFisicasForm.value.to_date.resetField()
                tomasFisicasForm.value.done_by_name.resetField()
                tomasFisicasForm.value.novedad.resetField()
                break
            }
            case 'movements': {
                movementForm.value.from_date.resetField()
                movementForm.value.to_date.resetField()
                movementForm.value.done_by_name.resetField()
                movementForm.value.notes.resetField()
                movementForm.value.warehouse_name.resetField()
                movementForm.value.status.resetField()
                movementForm.value.entrada = false
                movementForm.value.salida = false
                break
            }
        }
        await fetchManager(
            tabOption,
            { warehouse_id: activeWhInformation.value.bodega.id },
            { page: 1, per_page: whInformationPerPage.value }
        )
        controller.currentPage = 1
        showWaitOverlay.value = false
    }

    async function onPageChanged(
        tabOption: string,
        controller: whCardController
    ) {
        showWaitOverlay.value = true

        const pageOpt = {
            page: controller.currentPage,
            per_page: whInformationPerPage.value,
        }

        await fetchManager(
            tabOption,
            { warehouse_id: activeWhInformation.value.bodega.id },
            pageOpt
        )

        showWaitOverlay.value = false
    }

    function wharehouseButtonPressed(
        event: Event,
        whId: number,
        index: number
    ) {
        showAllWarehouses.value = true

        activeWharehouseButton.value = whId

        activeWhInformation.value.bodega = (warehouse.getWarehouseList ?? [])[
            index
        ]

        showWaitOverlay.value = true

        resetWhData()

        onPageChanged('inventory', invTabController.value)
        onPageChanged('tomas-fisicas', tomasFisicasTabController.value)
        onPageChanged('purchases', purchaseTabController.value)
        onPageChanged('movements', movementTabController.value).then(() => {
            showWaitOverlay.value = false
        })

        showAllWarehouses.value = false
    }
    function purchaseConfirmHandler(item: Purchase) {
        selectedPurchase.value = item
        purchaseModalShow.value = true
    }
    async function confirmarPedido() {
        showWaitOverlay.value = true
        const purchase_copy = { ...selectedPurchase.value }
        purchase_copy.status = DELIVERED_PURCHASE_STATUS.value
        warehouse
            .confirmPurchaseUser(purchase_copy as Purchase)
            .then(() => {
                toast.success('Entrega del pedido confirmada!')
                selectedPurchase.value.status = DELIVERED_PURCHASE_STATUS.value
                showWaitOverlay.value = false
            })
            .catch((error: MessageResponse) => {
                toast.error(error.message)
                showWaitOverlay.value = false
            })
    }

    async function showItem(item: Item): Promise<void> {
        detailSelectedItem.value.item = item
        itemInfoShow.value = true
        detailSelectedItem.value.props = []
        detailSelectedItem.value.props = await itemStore.fetchItemProperties(
            item.id
        )
    }

    const truncate = (text: string, length: number, suffix: string): string => {
        if (typeof text == undefined || text == null) {
            return '---'
        }
        if (text.length > length) {
            return text.substring(0, length) + suffix
        } else {
            return text
        }
    }

    warehouse.fetchWarehouses().then(() => {
        whRows.value = (warehouse.getWarehouseList ?? []).length
        paginateAside(whPageCount.value, 0)
    })

    warehouse.fetchWarehousesLatestTomasFisicas().then(it => {
        allWarehousesTableInformation = it.data as WhWithTomaFisica[]
        paginateMain(whPageCount.value, 0)
        showWaitOverlay.value = false
    })
</script>

<template>
    <WaitOverlay :show="showWaitOverlay">
        <ECard>
            <div
                class="row d-inline-flex allign-content-center tw-bg-slate-50 dark:tw-bg-slate-600">
                <div
                    class="col-sm-12 col-md-12 col-xl-2 mx-1 tw-flex-col tw-rounded-lg tw-bg-white dark:tw-bg-slate-800">
                    <h1 class="title mt-2">Bodegas Disponibles</h1>

                    <b-form class="mt-2 t-form" role="search">
                        <b-form-input
                            class="mt-2"
                            type="search"
                            placeholder="Buscar"
                            aria-label="Search">
                        </b-form-input>
                    </b-form>

                    <b-pagination
                        v-model="currentAsidePage"
                        :total-rows="whRows"
                        :per-page="whPageCount"
                        aria-controls="b-list-warehouses"
                        align="center"
                        @page-click.left="onAsidePageChanged"
                        :limit="3"
                        hide-goto-end-buttons
                        class="paginator"></b-pagination>

                    <b-list-group
                        :per-page="whPageCount"
                        :current-page="currentAsidePage"
                        class="button-group smaller-btn-group">
                        <b-list-group-item
                            :class="{ active: activeWharehouseButton === -1 }"
                            button
                            @click.left="
                                () => {
                                    showAllWarehouses = true
                                    activeWharehouseButton = -1
                                }
                            ">
                            Todas las bodegas
                        </b-list-group-item>
                        <b-list-group-item
                            v-for="(wh, index) in paginatedWarehouse"
                            button
                            :class="{
                                active: wh.id === activeWharehouseButton,
                            }"
                            :key="wh.id"
                            :id="'whbtn-' + wh.id"
                            @click.left="
                                wharehouseButtonPressed($event, wh.id, index)
                            ">
                            {{ wh.name }}
                        </b-list-group-item>
                    </b-list-group>
                </div>

                <div
                    v-if="showAllWarehouses"
                    class="col-xl tw-bg-slate-50 dark:tw-bg-slate-700">
                    <h1 class="title tw-text-3xl tw-mt-2 mb-2">
                        Bodegas y Últimas Tomas Físicas
                    </h1>

                    <div class="row display-inline-flex">
                        <b-form inline class="col-3">
                            <b-form-input
                                id="wh-search"
                                placeholder="Busqueda de Bodega">
                            </b-form-input>
                        </b-form>
                        <e-button type="button" variant="primary" class="col-1"
                            >Buscar
                        </e-button>

                        <b-pagination
                            v-model="mainPageController.currentPage"
                            :total-rows="whRows"
                            :per-page="whPageCount"
                            aria-controls="b-list-warehouses"
                            align="center"
                            @page-click.left="onMainPageChanged"
                            :limit="10"
                            class="paginator col-5 tw-inline-flex"></b-pagination>

                        <e-button
                            type="button"
                            variant="secondary"
                            class="col-2 mx-1 col-md-3 col-sm-4">
                            Limpiar filtros
                        </e-button>
                    </div>

                    <BTable
                        :fields="allWarehousesFields"
                        :items="paginatedMainTable"
                        class="text-center">
                        <template #cell(#)="{ index }">
                            {{ index + 1 }}
                        </template>
                        <template #cell(RealizadaPor)="{ item }">
                            {{
                                (item.whtf_done_by_name ?? '--') +
                                ' ' +
                                (item.whtf_done_by_lastname ?? '--')
                            }}
                        </template>
                        <template #cell(FechaTomaFisica)="{ item }">
                            {{ truncate(item.whtf_created_at, 10, '') }}
                        </template>
                        <template #cell(Novedad)="{ item }">
                            {{ truncate(item.whtf_novedad, 15, '...') }}
                        </template>
                        <template #cell(Detalles)="{}">
                            <e-button
                                left-icon="fa-eye"
                                type="button"
                                variant="primary"
                                >Ver detalles
                            </e-button>
                        </template>
                    </BTable>
                </div>

                <!-- Specific warehouse card  -->

                <div v-else class="col-xl">
                    <div
                        class="row tw-bg-slate-50 dark:tw-bg-slate-600 mt-2 mb-2">
                        <h1 class="tw-text-3xl tw-font-bold">
                            {{ activeWhInformation.bodega?.name }}
                        </h1>
                    </div>

                    <b-tabs
                        active-tab-class=""
                        content-class="mt-3 tabs-style"
                        pills>
                        <!--


                            INVENTARIO TAB


                        -->

                        <b-tab title="Inventario" active>
                            <div class="row display-inline-flex mb-1">
                                <e-button
                                    v-b-toggle.collapse-1
                                    type="button"
                                    variant="primary"
                                    class="col-2 mx-1 col-md-3 col-sm-4"
                                    >Desplegar Busqueda
                                </e-button>
                                <b-collapse id="collapse-1" class="mt-2">
                                    <ECard>
                                        <ValidationForm
                                            v-slot="{ handleReset }"
                                            @submit="
                                                onSubmit(
                                                    'inventory',
                                                    invTabController
                                                )
                                            "
                                            :validation-schema="inventoryForm">
                                            <div class="row" align-v="start">
                                                <div
                                                    class="col-lg-4 col-xl-3 col-sm-6">
                                                    <Datepicker
                                                        v-model="
                                                            inventoryForm
                                                                .from_date.value
                                                        "
                                                        :max-date="
                                                            inventoryForm
                                                                .to_date?.value
                                                        "
                                                        show-now-button
                                                        now-button-label="Ahora"
                                                        auto-apply
                                                        close-on-scroll
                                                        textinput
                                                        dark
                                                        teleport-center>
                                                        <template
                                                            #dp-input="{
                                                                value,
                                                            }">
                                                            <InputText
                                                                label="Fecha Min de Actualizacion"
                                                                :model-value="
                                                                    value
                                                                "
                                                                :info-label="
                                                                    inventoryForm
                                                                        .from_date
                                                                        .errorMessage
                                                                "
                                                                :status="
                                                                    Boolean(
                                                                        inventoryForm
                                                                            .from_date
                                                                            .errorMessage
                                                                    )
                                                                "
                                                                info-status="danger" />
                                                        </template>
                                                    </Datepicker>
                                                </div>
                                                <div
                                                    class="col-lg-4 col-xl-3 col-sm-6">
                                                    <Datepicker
                                                        v-model="
                                                            inventoryForm
                                                                .to_date.value
                                                        "
                                                        :min-date="
                                                            inventoryForm
                                                                .from_date
                                                                ?.value
                                                        "
                                                        show-now-button
                                                        now-button-label="Ahora"
                                                        auto-apply
                                                        close-on-scroll
                                                        textinput
                                                        dark
                                                        teleport-center>
                                                        <template
                                                            #dp-input="{
                                                                value,
                                                            }">
                                                            <InputText
                                                                label="Fecha Max de Actualizacion"
                                                                :model-value="
                                                                    value
                                                                "
                                                                :info-label="
                                                                    inventoryForm
                                                                        .to_date
                                                                        .errorMessage
                                                                "
                                                                :status="
                                                                    Boolean(
                                                                        inventoryForm
                                                                            .to_date
                                                                            .errorMessage
                                                                    )
                                                                "
                                                                info-status="danger" />
                                                        </template>
                                                    </Datepicker>
                                                </div>
                                                <div
                                                    class="col-lg-6 col-xl-3 col-sm-12 mt-auto">
                                                    <InputText
                                                        label="Código Producto"
                                                        v-model="
                                                            inventoryForm
                                                                .codename.value
                                                        "
                                                        :info-label="
                                                            inventoryForm
                                                                .codename
                                                                .errorMessage
                                                        "
                                                        :status="
                                                            Boolean(
                                                                inventoryForm
                                                                    .codename
                                                                    .errorMessage
                                                            )
                                                        "
                                                        info-status="danger" />
                                                </div>
                                                <div
                                                    class="col-lg-4 col-xl-3 col-sm-6 mt-auto">
                                                    <InputText
                                                        label="Nombre Producto"
                                                        v-model="
                                                            inventoryForm.name
                                                                .value
                                                        "
                                                        :info-label="
                                                            inventoryForm.name
                                                                .errorMessage
                                                        "
                                                        :status="
                                                            Boolean(
                                                                inventoryForm
                                                                    .name
                                                                    .errorMessage
                                                            )
                                                        "
                                                        info-status="danger" />
                                                </div>
                                            </div>
                                            <div class="row" align-v="start">
                                                <div
                                                    class="col-sm-3 col-lg-4 col-xl-2">
                                                    <InputText
                                                        label="Cantidad Min"
                                                        v-model="
                                                            inventoryForm
                                                                .min_quantity
                                                                .value
                                                        "
                                                        :info-label="
                                                            inventoryForm
                                                                .min_quantity
                                                                .errorMessage
                                                        "
                                                        :status="
                                                            Boolean(
                                                                inventoryForm
                                                                    .min_quantity
                                                                    .errorMessage
                                                            )
                                                        "
                                                        info-status="danger" />
                                                </div>
                                                <div
                                                    class="col-sm-3 col-lg-4 col-xl-2">
                                                    <InputText
                                                        label="Cantidad Max"
                                                        v-model="
                                                            inventoryForm
                                                                .max_quantity
                                                                .value
                                                        "
                                                        :info-label="
                                                            quantityRangeError
                                                        "
                                                        :status="
                                                            Boolean(
                                                                inventoryForm
                                                                    .max_quantity
                                                                    .errorMessage
                                                            )
                                                        "
                                                        info-status="danger" />
                                                </div>
                                                <div
                                                    class="col-sm-3 col-lg-4 col-xl-2">
                                                    <InputText
                                                        label="Precio Min"
                                                        v-model="
                                                            inventoryForm
                                                                .min_price.value
                                                        "
                                                        :info-label="
                                                            inventoryForm
                                                                .min_price
                                                                .errorMessage
                                                        "
                                                        :status="
                                                            Boolean(
                                                                inventoryForm
                                                                    .min_price
                                                                    .errorMessage
                                                            )
                                                        "
                                                        info-status="danger" />
                                                </div>
                                                <div
                                                    class="col-sm-3 col-lg-4 col-xl-2">
                                                    <InputText
                                                        label="Precio Max"
                                                        v-model="
                                                            inventoryForm
                                                                .max_price.value
                                                        "
                                                        :info-label="
                                                            priceRangeError
                                                        "
                                                        :status="
                                                            Boolean(
                                                                inventoryForm
                                                                    .max_price
                                                                    .errorMessage
                                                            )
                                                        "
                                                        info-status="danger" />
                                                </div>
                                                <div
                                                    class="col-2 col-md-3 col-sm-4 mt-4 text-center">
                                                    <EButton class="">
                                                        Confirmar Busqueda
                                                    </EButton>
                                                </div>
                                                <div
                                                    class="col-2 col-sm-3 col-md-3 col-sm-4 mt-4">
                                                    <e-button
                                                        @click.left="
                                                            () => {
                                                                onReset(
                                                                    invTabController,
                                                                    'inventory'
                                                                )
                                                                handleReset()
                                                            }
                                                        "
                                                        type="button"
                                                        variant="secondary">
                                                        Limpiar Busqueda
                                                    </e-button>
                                                </div>
                                            </div>
                                        </ValidationForm>
                                    </ECard>
                                </b-collapse>
                            </div>

                            <ModalDialog v-model:show="itemInfoShow" size="3xl">
                                <template #dialog-title>
                                    <b class="tw-text-2xl"
                                        >Detalle del Ítem
                                        {{ detailSelectedItem.item?.name }}</b
                                    >
                                </template>
                                <div class="container">
                                    <h3 class="tw-text-xl tw-font-bold">
                                        Detalle
                                    </h3>
                                    <div
                                        class="row tw-pb-3 align-content-center justify-content-center gy-2">
                                        <template
                                            v-for="(
                                                d, k
                                            ) in detailSelectedItem.item"
                                            :key="k">
                                            <div
                                                class="tw-rounded tw-ring-1 tw-ring-slate-500 tw-py-1 col-12 col-md-5 tw-mx-2"
                                                v-if="
                                                    ![
                                                        'category',
                                                        'img',
                                                        'quantity',
                                                    ].includes(k)
                                                ">
                                                <div class="row">
                                                    <span
                                                        class="tw-w-1/2 tw-font-bold col-6"
                                                        >{{ k }}:</span
                                                    >
                                                    <span class="col-6">{{
                                                        d
                                                    }}</span>
                                                </div>
                                            </div>
                                        </template>
                                    </div>
                                    <div
                                        v-if="detailSelectedItem.props"
                                        class="tw-ring-1 tw-ring-slate-500 tw-rounded tw-pb-3 row">
                                        <h3 class="col-12 tw-text-xl tw-py-1.5">
                                            <b>Caracteríticas del Ítem</b>
                                        </h3>
                                        <template
                                            v-for="(
                                                param, idx
                                            ) in detailSelectedItem.props"
                                            :key="idx">
                                            <div
                                                class="col-6 col-md-3 col-xl-2 tw-text-md">
                                                <b>{{ param.name }}:</b>
                                            </div>
                                            <div
                                                class="col-6 col-md-3 col-xl-2">
                                                {{ param.value }}
                                            </div>
                                        </template>
                                    </div>
                                </div>
                            </ModalDialog>

                            <BTable
                                id="whinv-table"
                                :fields="inventoryFields"
                                :items="activeWhInformation.inventory"
                                class="table">
                                <template #cell(#)="{ index }">
                                    {{ index + 1 }}
                                </template>
                                <template #cell(PVenta)="{ item }">
                                    {{ item.price * item.quantity }}
                                </template>
                                <template #cell(Acciones)="{ item }">
                                    <e-button
                                        left-icon="fa-eye"
                                        @click.left="showItem(item)"
                                        type="button"
                                        variant="secondary"
                                        >Ver detalles
                                    </e-button>
                                </template>
                            </BTable>

                            <b-pagination
                                v-model="invTabController.currentPage"
                                :total-rows="invTabController.totalRows"
                                :per-page="whInformationPerPage"
                                aria-controls="whinv-table"
                                align="center"
                                @page-click.left="
                                    onPageChanged('inventory', invTabController)
                                "
                                :limit="10"
                                hide-goto-end-buttons
                                class="paginator"></b-pagination>
                        </b-tab>

                        <!--


                            HISTORIAL DE COMPRAS TAB


                        -->

                        <b-tab title="Historial de Compras">
                            <div class="row display-inline-flex mb-1">
                                <div class="row display-inline-flex mb-1">
                                    <e-button
                                        v-b-toggle.collapse-2
                                        type="button"
                                        variant="primary"
                                        class="col-2 mx-1 col-md-3 col-sm-4"
                                        >Desplegar Busqueda
                                    </e-button>
                                    <b-collapse id="collapse-2" class="mt-2">
                                        <ModalDialog
                                            id="purchase-modal"
                                            v-model:show="purchaseModalShow"
                                            title="Confirmar Entrega de pedido"
                                            ok-text="Confirmar"
                                            @ok="confirmarPedido()"
                                            button-type="ok-cancel">
                                            <h1
                                                class="tw-text-3xl tw-text-black dark:tw-text-white">
                                                ¿Quiere confirmar que llegó el
                                                pedido?
                                            </h1>

                                            <div class="row">
                                                <div
                                                    class="row col-12 tw-rounded tw-ring-1 tw-ring-slate-500 tw-py-2">
                                                    <h3
                                                        class="tw-w-1/2 tw-font-bold col-6">
                                                        Fecha de aprobacion:
                                                    </h3>
                                                    <p class="col-6">
                                                        {{
                                                            selectedPurchase?.aproved_at
                                                        }}
                                                    </p>
                                                </div>
                                                <div
                                                    class="row col-12 tw-rounded tw-ring-1 tw-ring-slate-500 tw-py-2">
                                                    <h3
                                                        class="tw-w-1/2 tw-font-bold col-6">
                                                        Código de referencia
                                                    </h3>
                                                    <p class="col-6">
                                                        {{
                                                            selectedPurchase?.reference
                                                        }}
                                                    </p>
                                                </div>

                                                <div
                                                    class="row col-12 tw-rounded tw-ring-1 tw-ring-slate-500 tw-py-2">
                                                    <h3
                                                        class="tw-w-1/2 tw-font-bold col-6">
                                                        Código de factura:
                                                    </h3>
                                                    <p class="col-6">
                                                        {{
                                                            selectedPurchase
                                                                ?.invoice.code
                                                        }}
                                                    </p>
                                                </div>
                                                <div
                                                    class="row col-12 tw-rounded tw-ring-1 tw-ring-slate-500 tw-py-2">
                                                    <h3
                                                        class="tw-w-1/2 tw-font-bold col-6">
                                                        Código de factura:
                                                    </h3>
                                                    <p class="col-6">
                                                        {{
                                                            selectedPurchase
                                                                ?.invoice.code
                                                        }}
                                                    </p>
                                                </div>
                                                <div
                                                    class="row col-12 tw-rounded tw-ring-1 tw-ring-slate-500 tw-py-2">
                                                    <h3
                                                        class="tw-w-1/2 tw-font-bold col-6">
                                                        Proveedor
                                                    </h3>
                                                    <p class="col-6">
                                                        {{
                                                            selectedPurchase
                                                                ?.provider.name
                                                        }}
                                                    </p>
                                                </div>
                                            </div>
                                        </ModalDialog>
                                        <ECard>
                                            <ValidationForm
                                                v-slot="{ handleReset }"
                                                @submit="
                                                    onSubmit(
                                                        'purchases',
                                                        purchaseTabController
                                                    )
                                                "
                                                :validation-schema="
                                                    purchaseForm
                                                ">
                                                <div
                                                    class="row"
                                                    align-v="start">
                                                    <div
                                                        class="col-lg-4 col-xl-3 col-sm-6">
                                                        <Datepicker
                                                            v-model="
                                                                purchaseForm
                                                                    .from_date
                                                                    .value
                                                            "
                                                            :max-date="
                                                                purchaseForm
                                                                    .to_date
                                                                    ?.value
                                                            "
                                                            show-now-button
                                                            now-button-label="Ahora"
                                                            auto-apply
                                                            close-on-scroll
                                                            textinput
                                                            dark
                                                            teleport-center>
                                                            <template
                                                                #dp-input="{
                                                                    value,
                                                                }">
                                                                <InputText
                                                                    label="Fecha Mínima"
                                                                    :model-value="
                                                                        value
                                                                    "
                                                                    :info-label="
                                                                        purchaseForm
                                                                            .from_date
                                                                            .errorMessage
                                                                    "
                                                                    :status="
                                                                        Boolean(
                                                                            purchaseForm
                                                                                .from_date
                                                                                .errorMessage
                                                                        )
                                                                    "
                                                                    info-status="danger" />
                                                            </template>
                                                        </Datepicker>
                                                    </div>
                                                    <div
                                                        class="col-lg-4 col-xl-3 col-sm-6">
                                                        <Datepicker
                                                            v-model="
                                                                purchaseForm
                                                                    .to_date
                                                                    .value
                                                            "
                                                            :min-date="
                                                                purchaseForm
                                                                    .from_date
                                                                    ?.value
                                                            "
                                                            show-now-button
                                                            now-button-label="Ahora"
                                                            auto-apply
                                                            close-on-scroll
                                                            textinput
                                                            dark
                                                            teleport-center>
                                                            <template
                                                                #dp-input="{
                                                                    value,
                                                                }">
                                                                <InputText
                                                                    label="Fecha Máxima"
                                                                    :model-value="
                                                                        value
                                                                    "
                                                                    :info-label="
                                                                        purchaseForm
                                                                            .to_date
                                                                            .errorMessage
                                                                    "
                                                                    :status="
                                                                        Boolean(
                                                                            purchaseForm
                                                                                .to_date
                                                                                .errorMessage
                                                                        )
                                                                    "
                                                                    info-status="danger" />
                                                            </template>
                                                        </Datepicker>
                                                    </div>
                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <b-form-checkbox
                                                            class="tw-text-xl"
                                                            v-model="
                                                                purchaseForm.aproved_date
                                                            "
                                                            switch>
                                                            Buscar Por Fecha de
                                                            Creación
                                                        </b-form-checkbox>
                                                    </div>
                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <b-form-checkbox
                                                            class="tw-text-xl"
                                                            v-model="
                                                                purchaseForm.invoice_date
                                                            "
                                                            name="checkbox-1"
                                                            value="true"
                                                            unchecked-value="false"
                                                            switch>
                                                            Buscar Por Fecha de
                                                            Pago
                                                        </b-form-checkbox>
                                                    </div>

                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <b-form-checkbox
                                                            class="tw-text-xl"
                                                            v-model="
                                                                purchaseForm
                                                                    .status
                                                                    .value
                                                            "
                                                            name="checkbox-2"
                                                            switch>
                                                            Buscar Compras
                                                            Enregadas
                                                        </b-form-checkbox>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div
                                                        class="col-lg-6 col-xl-3 col-sm-12 mt-auto">
                                                        <InputText
                                                            label="Código de Orden"
                                                            v-model="
                                                                purchaseForm
                                                                    .reference
                                                                    .value
                                                            "
                                                            :info-label="
                                                                purchaseForm
                                                                    .reference
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    purchaseForm
                                                                        .reference
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>
                                                    <div
                                                        class="col-lg-4 col-xl-3 col-sm-6 mt-auto">
                                                        <InputText
                                                            label="Nombre de Provedor"
                                                            v-model="
                                                                purchaseForm
                                                                    .provider_name
                                                                    .value
                                                            "
                                                            :info-label="
                                                                purchaseForm
                                                                    .provider_name
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    purchaseForm
                                                                        .provider_name
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>
                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <InputText
                                                            label="Código de pago"
                                                            v-model="
                                                                purchaseForm
                                                                    .invoice_code
                                                                    .value
                                                            "
                                                            :info-label="
                                                                purchaseForm
                                                                    .invoice_code
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    purchaseForm
                                                                        .invoice_code
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>
                                                    <div
                                                        class="col-2 mt-4 text-center">
                                                        <EButton class="">
                                                            Confirmar Busqueda
                                                        </EButton>
                                                    </div>

                                                    <div
                                                        class="col-2 col-md-3 col-sm-4 mt-4">
                                                        <e-button
                                                            @click.left="
                                                                () => {
                                                                    onReset(
                                                                        purchaseTabController,
                                                                        'purchases'
                                                                    )
                                                                    handleReset()
                                                                }
                                                            "
                                                            type="button"
                                                            variant="secondary">
                                                            Limpiar Busqueda
                                                        </e-button>
                                                    </div>
                                                </div>
                                            </ValidationForm>
                                        </ECard>
                                    </b-collapse>
                                </div>
                            </div>

                            <BTable
                                :fields="purchasesFields"
                                :items="activeWhInformation.purchases">
                                <template #cell(#)="{ index }">
                                    {{ index + 1 }}
                                </template>
                                <template #cell(FechaCreación)="{ item }">
                                    {{ truncate(item.aproved_at, 10, '') }}
                                </template>
                                <template #cell(Entregado)="{ item }">
                                    <e-button
                                        v-if="
                                            item.status ===
                                            DELIVERED_PURCHASE_STATUS
                                        "
                                        class="tw-py-1 tw-px-1"
                                        left-icon="check"
                                        type="button"
                                        variant="outline"
                                        @click.prevent>
                                        Entregado
                                    </e-button>
                                    <e-button
                                        v-else
                                        class="tw-py-1 tw-px-1"
                                        type="button"
                                        variant="primary"
                                        @click.left="
                                            purchaseConfirmHandler(item)
                                        ">
                                        Confirmar Entrega
                                    </e-button>
                                </template>
                                <template #cell(Proveedor)="{ item }">
                                    {{ item.provider.name }}
                                </template>
                                <template #cell(Pago)="{ item }">
                                    {{ item.invoice.code ?? '--' }}
                                </template>
                                <template #cell(FechaPago)="{ item }">
                                    {{
                                        truncate(
                                            item.invoice.created_at,
                                            10,
                                            ''
                                        )
                                    }}
                                </template>
                                <template #cell(Acciones)="{}">
                                    <e-button
                                        left-icon="fa-eye"
                                        type="button"
                                        variant="secondary"
                                        >Ver detalles
                                    </e-button>
                                </template>
                            </BTable>

                            <b-pagination
                                v-model="purchaseTabController.currentPage"
                                :total-rows="purchaseTabController.totalRows"
                                :per-page="whInformationPerPage"
                                aria-controls="whpurchase-table"
                                align="center"
                                @page-click.left="
                                    onPageChanged(
                                        'purchases',
                                        purchaseTabController
                                    )
                                "
                                :limit="10"
                                hide-goto-end-buttons
                                class="paginator"></b-pagination>
                        </b-tab>

                        <!--


                            TOMAS FISICAS TAB


                        -->

                        <b-tab title="Toma Física">
                            <div class="row display-inline-flex mb-1">
                                <e-button
                                    v-b-toggle.collapse-3
                                    type="button"
                                    variant="primary"
                                    class="col-2 mx-1 col-md-3 col-sm-4"
                                    >Desplegar Busqueda
                                </e-button>
                                <b-collapse id="collapse-3" class="mt-2">
                                    <ECard>
                                        <ValidationForm
                                            v-slot="{ handleReset }"
                                            @submit="
                                                onSubmit(
                                                    'tomas-fisicas',
                                                    tomasFisicasTabController
                                                )
                                            "
                                            :validation-schema="
                                                tomasFisicasForm
                                            ">
                                            <div class="row" align-v="start">
                                                <div
                                                    class="col-lg-6 col-xl-4 col-sm-6">
                                                    <Datepicker
                                                        v-model="
                                                            tomasFisicasForm
                                                                .from_date.value
                                                        "
                                                        :max-date="
                                                            tomasFisicasForm
                                                                .to_date?.value
                                                        "
                                                        show-now-button
                                                        now-button-label="Ahora"
                                                        auto-apply
                                                        close-on-scroll
                                                        textinput
                                                        dark
                                                        teleport-center>
                                                        <template
                                                            #dp-input="{
                                                                value,
                                                            }">
                                                            <InputText
                                                                label="Fecha Min de Actualizacion"
                                                                :model-value="
                                                                    value
                                                                "
                                                                :info-label="
                                                                    tomasFisicasForm
                                                                        .from_date
                                                                        .errorMessage
                                                                "
                                                                :status="
                                                                    Boolean(
                                                                        tomasFisicasForm
                                                                            .from_date
                                                                            .errorMessage
                                                                    )
                                                                "
                                                                info-status="danger" />
                                                        </template>
                                                    </Datepicker>
                                                </div>
                                                <div
                                                    class="col-lg-6 col-xl-4 col-sm-6">
                                                    <Datepicker
                                                        v-model="
                                                            tomasFisicasForm
                                                                .to_date.value
                                                        "
                                                        :min-date="
                                                            tomasFisicasForm
                                                                .from_date.value
                                                        "
                                                        show-now-button
                                                        now-button-label="Ahora"
                                                        auto-apply
                                                        close-on-scroll
                                                        textinput
                                                        dark
                                                        teleport-center>
                                                        <template
                                                            #dp-input="{
                                                                value,
                                                            }">
                                                            <InputText
                                                                label="Fecha Max de Actualizacion"
                                                                :model-value="
                                                                    value
                                                                "
                                                                :info-label="
                                                                    tomasFisicasForm
                                                                        .to_date
                                                                        .errorMessage
                                                                "
                                                                :status="
                                                                    Boolean(
                                                                        tomasFisicasForm
                                                                            .to_date
                                                                            .errorMessage
                                                                    )
                                                                "
                                                                info-status="danger" />
                                                        </template>
                                                    </Datepicker>
                                                </div>
                                                <div
                                                    class="col-lg-6 col-xl-4 col-sm-12 mt-auto">
                                                    <InputText
                                                        label="Realizada Por"
                                                        v-model="
                                                            tomasFisicasForm
                                                                .done_by_name
                                                                .value
                                                        "
                                                        :info-label="
                                                            tomasFisicasForm
                                                                .done_by_name
                                                                .errorMessage
                                                        "
                                                        :status="
                                                            Boolean(
                                                                tomasFisicasForm
                                                                    .done_by_name
                                                                    .errorMessage
                                                            )
                                                        "
                                                        placeholder="Ingrese un nombre o apellido"
                                                        info-status="danger" />
                                                </div>
                                                <div class="row">
                                                    <div
                                                        class="col-lg-6 col-xl-4 col-sm-6 mt-auto">
                                                        <InputText
                                                            label="Novedad"
                                                            v-model="
                                                                tomasFisicasForm
                                                                    .novedad
                                                                    .value
                                                            "
                                                            :info-label="
                                                                tomasFisicasForm
                                                                    .novedad
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    tomasFisicasForm
                                                                        .novedad
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>

                                                    <div
                                                        class="col-2 mt-4 col-sm-3 text-center">
                                                        <EButton class="">
                                                            Confirmar Busqueda
                                                        </EButton>
                                                    </div>

                                                    <div
                                                        class="col-2 col-md-3 col-sm-4 mt-4">
                                                        <e-button
                                                            @click.left="
                                                                () => {
                                                                    onReset(
                                                                        tomasFisicasTabController,
                                                                        'tomas-fisicas'
                                                                    )
                                                                    handleReset()
                                                                }
                                                            "
                                                            type="button"
                                                            variant="secondary">
                                                            Limpiar Busqueda
                                                        </e-button>
                                                    </div>
                                                </div>
                                            </div>
                                        </ValidationForm>
                                    </ECard>
                                </b-collapse>
                            </div>

                            <BTable
                                :fields="tomasFisFields"
                                :items="activeWhInformation.tomasFisicas">
                                <template #cell(#)="{ index }">
                                    {{ index + 1 }}
                                </template>
                                <template #cell(FechaRealizacion)="{ item }">
                                    {{ truncate(item.created_at, 10, '') }}
                                </template>
                                <template #cell(RealizadaPor)="{ item }">
                                    {{
                                        item.done_by.name +
                                        ' ' +
                                        item.done_by.lastname
                                    }}
                                </template>
                                <template #cell(Acciones)="{}">
                                    <e-button
                                        left-icon="fa-eye"
                                        type="button"
                                        variant="secondary"
                                        >Ver detalles
                                    </e-button>
                                </template>
                            </BTable>

                            <b-pagination
                                v-model="tomasFisicasTabController.currentPage"
                                :total-rows="
                                    tomasFisicasTabController.totalRows
                                "
                                :per-page="whInformationPerPage"
                                aria-controls="whpurchase-table"
                                align="center"
                                @page-click.left="
                                    onPageChanged(
                                        'tomas-fisicas',
                                        tomasFisicasTabController
                                    )
                                "
                                :limit="10"
                                hide-goto-end-buttons
                                class="paginator"></b-pagination>
                        </b-tab>

                        <b-tab title="Movimientos">
                            <!--


                            MOVIMIENTOS DE BODEGA TAB


                        -->
                            <div class="row display-inline-flex mb-1">
                                <div class="row display-inline-flex mb-1">
                                    <e-button
                                        v-b-toggle.collapse-4
                                        type="button"
                                        variant="primary"
                                        class="col-2 mx-1 col-md-3 col-sm-4"
                                        >Desplegar Busqueda
                                    </e-button>
                                    <b-collapse id="collapse-4" class="mt-2">
                                        <ECard>
                                            <ValidationForm
                                                v-slot="{ handleReset }"
                                                @submit="
                                                    onSubmit(
                                                        'movements',
                                                        movementTabController
                                                    )
                                                "
                                                :validation-schema="
                                                    movementForm
                                                ">
                                                <div
                                                    class="row"
                                                    align-v="start">
                                                    <div
                                                        class="col-lg-4 col-xl-3 col-sm-6">
                                                        <Datepicker
                                                            v-model="
                                                                movementForm
                                                                    .from_date
                                                                    .value
                                                            "
                                                            :max-date="
                                                                movementForm
                                                                    .to_date
                                                                    ?.value
                                                            "
                                                            show-now-button
                                                            now-button-label="Ahora"
                                                            auto-apply
                                                            close-on-scroll
                                                            textinput
                                                            dark
                                                            teleport-center>
                                                            <template
                                                                #dp-input="{
                                                                    value,
                                                                }">
                                                                <InputText
                                                                    label="Fecha Mínima"
                                                                    :model-value="
                                                                        value
                                                                    "
                                                                    :info-label="
                                                                        movementForm
                                                                            .from_date
                                                                            .errorMessage
                                                                    "
                                                                    :status="
                                                                        Boolean(
                                                                            movementForm
                                                                                .from_date
                                                                                .errorMessage
                                                                        )
                                                                    "
                                                                    info-status="danger" />
                                                            </template>
                                                        </Datepicker>
                                                    </div>
                                                    <div
                                                        class="col-lg-4 col-xl-3 col-sm-6">
                                                        <Datepicker
                                                            v-model="
                                                                movementForm
                                                                    .to_date
                                                                    .value
                                                            "
                                                            :min-date="
                                                                movementForm
                                                                    .from_date
                                                                    ?.value
                                                            "
                                                            show-now-button
                                                            now-button-label="Ahora"
                                                            auto-apply
                                                            close-on-scroll
                                                            textinput
                                                            dark
                                                            teleport-center>
                                                            <template
                                                                #dp-input="{
                                                                    value,
                                                                }">
                                                                <InputText
                                                                    label="Fecha Máxima"
                                                                    :model-value="
                                                                        value
                                                                    "
                                                                    :info-label="
                                                                        movementForm
                                                                            .to_date
                                                                            .errorMessage
                                                                    "
                                                                    :status="
                                                                        Boolean(
                                                                            movementForm
                                                                                .to_date
                                                                                .errorMessage
                                                                        )
                                                                    "
                                                                    info-status="danger" />
                                                            </template>
                                                        </Datepicker>
                                                    </div>
                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <b-form-checkbox
                                                            class="tw-text-xl"
                                                            v-model="
                                                                movementForm.entrada
                                                            "
                                                            value="true"
                                                            unchecked-value="false"
                                                            switch>
                                                            Buscar Entradas a
                                                            Bodega
                                                        </b-form-checkbox>
                                                    </div>
                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <InputText
                                                            label="Estado"
                                                            v-model="
                                                                movementForm
                                                                    .status
                                                                    .value
                                                            "
                                                            :info-label="
                                                                movementForm
                                                                    .status
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    movementForm
                                                                        .status
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div
                                                        class="col-lg-6 col-xl-3 col-sm-12 mt-auto">
                                                        <InputText
                                                            label="Notas"
                                                            v-model="
                                                                movementForm
                                                                    .notes.value
                                                            "
                                                            :info-label="
                                                                movementForm
                                                                    .notes
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    movementForm
                                                                        .notes
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>

                                                    <div
                                                        class="col-2 mt-4 text-center">
                                                        <EButton class="">
                                                            Confirmar Busqueda
                                                        </EButton>
                                                    </div>

                                                    <div
                                                        class="col-2 col-md-3 col-sm-4 mt-4">
                                                        <e-button
                                                            @click.left="
                                                                () => {
                                                                    onReset(
                                                                        movementTabController,
                                                                        'movements'
                                                                    )
                                                                    handleReset()
                                                                }
                                                            "
                                                            type="button"
                                                            variant="secondary">
                                                            Limpiar Busqueda
                                                        </e-button>
                                                    </div>
                                                </div>
                                            </ValidationForm>
                                        </ECard>
                                    </b-collapse>
                                </div>
                            </div>

                            <BTable
                                :fields="movementsFields"
                                :items="activeWhInformation.movements">
                                <template #cell(#)="{ index }">
                                    {{ index + 1 }}
                                </template>

                                <template #cell(Creada)="{ item }">
                                    {{ truncate(item.created_at, 10, '') }}
                                </template>
                                <template #cell(RealizadaPor)="{ item }">
                                    {{
                                        item.created_by.name +
                                        ' ' +
                                        item.created_by.lastname
                                    }}
                                </template>
                                <template #cell(BodegaRelacionada)="{ item }">
                                    {{
                                        item.warehouse_destiny.id ==
                                        activeWhInformation.bodega.id
                                            ? item.warehouse_origin.name
                                            : item.warehouse_destiny.name
                                    }}
                                </template>
                                <template #cell(TipoDeMovimiento)="{ item }">
                                    {{
                                        item.warehouse_destiny.id ==
                                        activeWhInformation.bodega.id
                                            ? 'Salida'
                                            : 'Entrada'
                                    }}
                                </template>
                                <template #cell(Notas)="{ item }">
                                    {{ truncate(item.notes, 10, '...') }}
                                </template>
                                <template #cell(Acciones)="{}">
                                    <e-button
                                        left-icon="fa-eye"
                                        type="button"
                                        variant="primary"
                                        >Ver detalles
                                    </e-button>
                                </template>
                            </BTable>

                            <b-pagination
                                v-model="movementTabController.currentPage"
                                :total-rows="movementTabController.totalRows"
                                :per-page="whInformationPerPage"
                                aria-controls="whpurchase-table"
                                align="center"
                                @page-click.left="
                                    onPageChanged(
                                        'movements',
                                        movementTabController
                                    )
                                "
                                :limit="10"
                                hide-goto-end-buttons
                                class="paginator"></b-pagination>
                        </b-tab>
                    </b-tabs>
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
