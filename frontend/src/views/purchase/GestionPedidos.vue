<script setup lang="ts">
    import { useItemStore } from '@store'
    import { useOrderStore } from '@store'
    import { usePurchaseStore } from '@store/purchase'
    import {
        type FullPurchase,
        type FullPurchaseDetails,
        type PaginatedResponse,
        type ProductProps,
        type ProductVariant,
        type Purchase,
        type PurchaseQuery,
        type SimpleProduct,
        type Status,
        type Warehouse,
        isMessage,
    } from '@store/types'
    import type { SimpleOrderStatus } from '@store/types/orders.model'
    import { useWarehouseStore } from '@store/warehouse'
    import Datepicker from '@vuepic/vue-datepicker'
    import {
        BBadge,
        BPagination,
        BTable,
        type ColorVariant,
        type TableField,
    } from 'bootstrap-vue-3'
    import moment from 'moment'
    import { Form as ValidationForm, useField } from 'vee-validate'
    import * as yup from 'yup'

    import { onMounted, watch } from 'vue'
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

    const showWaitOverlay = ref(true)
    const router = useRoute()
    const itemStore = useItemStore()
    const orderStore = useOrderStore()

    moment.locale('es', {
        weekdays: 'Domingo_Lunes_Martes_Miércoles_Jueves_Viernes_Sábado'.split(
            '_'
        ),
    })
    const purchaseStore = usePurchaseStore()
    const warehouse = useWarehouseStore()
    const toast = useToast()

    const paginatedPurchaseList = ref<Purchase[]>()
    const currentPage = ref(1)
    const purchasePerPage = ref(25)
    const totalPurchaseCount = ref(0)

    type SelectedItem = {
        product: SimpleProduct
        variant: ProductVariant
        props: ProductProps[]
    }
    const detailSelectedProduct = ref<SelectedItem>()

    const isPurchaseSelected = ref<boolean>(false)
    const selectedPurchase = ref<FullPurchase>()
    const productInfoShow = ref<boolean>(false)
    const loadingProps = ref<boolean>(false)

    const purchaseDetailsArr = ref<FullPurchaseDetails[]>()
    const paginatedPurchaseDetailsArr = ref<FullPurchaseDetails[]>()
    const currentDetailsPage = ref(1)
    const searchString = ref('')

    const providerList = ref<{ id: number; name: string }[]>([])
    const selectedProvider = ref<{ id: number; name: string }>()

    const purchaseForm = ref({
        from_date: useField(
            'to_date',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? null : curr
                )
                .typeError('Fecha Invalida')
        ),
        to_date: useField(
            'to_date',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? null : curr
                )
                .typeError('Fecha Invalida')
        ),
        status_from_date: useField(
            'status_to_date',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? null : curr
                )
                .typeError('Fecha Invalida')
        ),
        status_to_date: useField(
            'status_to_date',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? null : curr
                )
                .typeError('Fecha Invalida')
        ),
        provider_name: useField(
            'provider_name',
            yup.string().optional().nullable(true)
        ),
        reference: useField(
            'reference',
            yup
                .number()
                .optional()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? undefined : curr
                )
                .typeError('Ingrese un número entero')
        ),
    })

    const selectedStatus = ref<Status>()
    const selectedWarehouse = ref<Warehouse>()

    const purchasesFields: TableField[] = [
        '#',
        'BodegaDestino',
        'FechaAprobación',
        { label: 'Código Orden', key: 'reference' },
        'AprobadoPor',
        'RazónDeCompra',
        'Estado',
        'Acciones',
    ]

    const detailsFields: TableField[] = [
        '#',
        'Código',
        'Nombre',
        'PrecioDeCompra',
        'PrecioDeVenta',
        'Cantidad',
        'Proveedor',
        'Acciones',
    ]

    const showStatusAndChilds = ref<boolean>(false)

    async function onDetallesClicked(pid: number) {
        showWaitOverlay.value = true

        const res = await purchaseStore.fetchPurchaseInformation(
            { purchase_id: pid },
            { page: 1 }
        )

        if (isMessage(res)) {
            toast.error(
                'No se puedo cargar commpra, vuelva a internalo mas tarde',
                { timeout: 4500 }
            )
            showWaitOverlay.value = false
            return
        }

        selectedPurchase.value = res.data[0] as FullPurchase
        const arrPromise: Promise<any>[] = []

        purchaseDetailsArr.value = []
        providerList.value = []

        providerList.value.push({ id: -1, name: 'Todos los productos' })

        for (const p_child of selectedPurchase.value.childs) {
            providerList.value.push(
                p_child.provider ? p_child.provider : { id: -2, name: 'N/A' }
            )
            arrPromise.push(
                purchaseStore
                    .fetchPurchaseDetails({ purchase_child_id: p_child.id })
                    .then(res => {
                        if (purchaseDetailsArr.value && !isMessage(res))
                            for (const obj of res) {
                                obj.provider = p_child.provider
                                purchaseDetailsArr.value.push(obj)
                            }
                    })
                    .catch(() => {
                        toast.error(
                            'Error al cargar informacion de la compra',
                            { timeout: 3500 }
                        )
                        return
                    })
            )
        }

        try {
            let order_res = await orderStore.fetchRequests({
                order_id: selectedPurchase.value.order_origin.id,
                page: 1,
                per_page: 100,
            })

            if (isMessage(order_res)) {
                toast.error('Error al cargar estados de la orden')
            } else {
                order_res = order_res as PaginatedResponse<SimpleOrderStatus>
                selectedPurchase.value.order_origin.status_list = order_res.data
            }
        } catch {
            toast.error('Error al cargar estados de la orden')
        }

        Promise.all(arrPromise)
            .then(() => {
                showWaitOverlay.value = false
                isPurchaseSelected.value = true
                purchaseDetailsArr.value?.sort()
                filterData()
                setInfoChildPurchase()
            })
            .finally(() => {
                showWaitOverlay.value = false
                filterData()
            })
    }

    async function showProduct(picked: FullPurchaseDetails): Promise<void> {
        const object = {
            product: picked.product,
            variant: picked.variant,
            props: [],
        }
        detailSelectedProduct.value = object
        productInfoShow.value = true
        detailSelectedProduct.value.props = []
        loadingProps.value = true
        let res = await itemStore.fetchProductProperties({
            variant_id: picked.variant.id,
        })
        if (isMessage(res)) {
            loadingProps.value = false
            detailSelectedProduct.value.props[0] = {
                name: 'Error',
                value: 'No se pudo cargar los detalles',
            }
            return
        }

        res = res as PaginatedResponse<ProductProps>
        detailSelectedProduct.value.props = res.data
        loadingProps.value = false
    }

    async function onBuscarClick(): Promise<void> {
        showWaitOverlay.value = true
        stopWatcher.value = true

        const query: PurchaseQuery = {}
        const f = purchaseForm.value

        if (
            f.from_date.errorMessage ||
            f.to_date.errorMessage ||
            f.status_from_date.errorMessage ||
            f.status_to_date.errorMessage ||
            f.provider_name.errorMessage ||
            f.reference.errorMessage
        ) {
            toast.error('Verifique los datos antes buscar')
            showWaitOverlay.value = false
            return
        }
        if (f.to_date.value || f.from_date.value) {
            query.approved_date = true
        }
        query.from_date = f.from_date.value
        query.to_date = f.to_date.value
        query.provider_name = f.provider_name.value
        query.status = selectedStatus.value?.name
        query.status_from_date = f.status_from_date.value
        query.status_to_date = f.status_to_date.value
        query.warehouse_id = selectedWarehouse.value?.id
        query.reference = f.reference.value as number
        purchaseStore
            .fetchPaginatedPurchases(query, {
                page: 1,
                per_page: purchasePerPage.value,
            })
            .then(it => {
                if (isMessage(it)) {
                    return
                }
                if (it.data.length == 0) {
                    toast.error('No se ha encontrado registros')
                    return
                }
                paginatedPurchaseList.value = it.data
                toast.success('Búsqueda exitosa')
            })
            .catch(err => {
                if (isMessage(err)) {
                    toast.error(err.message)
                } else {
                    toast.error('Error')
                }
            })
            .finally((): void => {
                currentPage.value = 1
                showWaitOverlay.value = false
                stopWatcher.value = false
            })
    }

    function filterData(): void {
        stopWatcher.value = true
        if (searchString.value.length > 0 && purchaseDetailsArr.value) {
            currentDetailsPage.value = 1
            paginatedPurchaseDetailsArr.value = purchaseDetailsArr.value
                .filter(d => {
                    return (
                        d.product.product_name.includes(searchString.value) ||
                        d.variant.variant_name.includes(searchString.value) ||
                        d.provider?.name.includes(searchString.value) ||
                        d.variant.sku.includes(searchString.value)
                    )
                })
                .slice(
                    (currentDetailsPage.value - 1) * purchasePerPage.value,
                    currentDetailsPage.value * purchasePerPage.value
                )
            stopWatcher.value = false
        } else {
            paginatedPurchaseDetailsArr.value = purchaseDetailsArr.value?.slice(
                (currentDetailsPage.value - 1) * purchasePerPage.value,
                currentDetailsPage.value * purchasePerPage.value
            )
            stopWatcher.value = false
        }
    }

    function filterProvider(): void {
        if (selectedProvider.value?.id != -1 && purchaseDetailsArr.value) {
            currentDetailsPage.value = 1
            paginatedPurchaseDetailsArr.value = purchaseDetailsArr.value
                .filter(d => {
                    return d.provider?.name.includes(
                        selectedProvider.value?.name
                            ? selectedProvider.value?.name
                            : ''
                    )
                })
                .slice(
                    (currentDetailsPage.value - 1) * purchasePerPage.value,
                    currentDetailsPage.value * purchasePerPage.value
                )
            stopWatcher.value = false
        } else {
            paginatedPurchaseDetailsArr.value = purchaseDetailsArr.value?.slice(
                (currentDetailsPage.value - 1) * purchasePerPage.value,
                currentDetailsPage.value * purchasePerPage.value
            )
            stopWatcher.value = false
        }
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

    function keyNaturalName(key: string) {
        switch (key) {
            case 'id':
                return 'Código'
            case 'product_name':
                return 'Producto'
            case 'variant_name':
                return 'Nombre de Variante'
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
                return 'SKU'
        }
        return key
    }
    function statusPurchaseColor(status?: string): ColorVariant {
        switch (status) {
            case 'entregado':
                return 'success'
            case 'aprovado':
                return 'primary'
            case 'transito':
                return 'warning'
            case 'rechazado':
                return 'danger'
            case 'cancelado':
                return 'dark'
            case 'pagado':
                return 'light'
            default:
                return 'info'
        }
    }

    function statusOrderColor(status?: string): ColorVariant {
        switch (status) {
            case 'AP':
                return 'success'
            case 'PA':
                return 'warning'
            case 'NG':
                return 'danger'
            default:
                return 'dark'
        }
    }
    function parseStatus(status?: string): string {
        switch (status) {
            case 'AP':
                return 'Aprobado'
            case 'PA':
                return 'Pendiente aprobación'
            case 'CR':
                return 'Necesita Corrección'
            case 'NG':
                return 'Desaprobado'
            default:
                return 'Desconocido'
        }
    }
    function getDisplayStatus(status_name: string) {
        const status_list = purchaseStore.getPurchaseStatus()
        const display_status = status_list?.find(s => s.name == status_name)
        return display_status ? display_status.display : 'Estado no reconocido'
    }

    const arrInfoChildPurchase =
        ref<{ total: number; num_variants: number }[]>()

    function setInfoChildPurchase(): void {
        for (const child of purchaseDetailsArr.value ?? []) {
            const filtered_arr = purchaseDetailsArr.value?.filter(
                product => product.provider?.name == child.provider?.name
            )
            let stock = 0
            for (const product of filtered_arr ?? []) {
                stock += product.quantity
            }

            const variants = filtered_arr ? filtered_arr.length : 0

            arrInfoChildPurchase.value?.push({
                total: stock,
                num_variants: variants,
            })
        }
    }

    const stopWatcher = ref(false)

    function paginateData() {
        if (!stopWatcher.value) {
            purchaseStore
                .fetchPaginatedPurchases(
                    {},
                    { page: currentPage.value, per_page: purchasePerPage.value }
                )
                .then(it => {
                    if (!isMessage(it)) {
                        paginatedPurchaseList.value = it.data
                    }
                    showWaitOverlay.value = false
                })
                .catch(() => {
                    showWaitOverlay.value = false
                    toast.error('Error al cargar los datos', { timeout: 4500 })
                })
        }
    }

    warehouse.fetchWarehouses().catch((): void => {
        toast.error('Error de carga de bodegas', { timeout: 3000 })
        showWaitOverlay.value = false
    })
    purchaseStore
        .fetchPaginatedPurchases(
            {},
            { page: 1, per_page: purchasePerPage.value }
        )
        .then(it => {
            if (!isMessage(it)) {
                paginatedPurchaseList.value = it.data
                totalPurchaseCount.value = it.total
            }
            showWaitOverlay.value = false
        })
        .catch(() => {
            showWaitOverlay.value = false
            toast.error('Error al cargar los datos', { timeout: 4500 })
        })

    watch(currentPage, paginateData)
    watch(currentDetailsPage, filterData)
    watch(searchString, filterData)

    onMounted(() => {
        const purchase_id = router.params.id
        if (purchase_id) {
            onDetallesClicked(Number(purchase_id))
        }
    })
</script>

<template>
    <WaitOverlay :show="showWaitOverlay">
        <ECard>
            <div class="container" v-if="!isPurchaseSelected">
                <b-collapse
                    id="collapse-1"
                    class="mt-2 inline-flex tw-rounded tw-ring-1 dark-mode-text tw-ring-yellow-400 tw-py-2">
                    <h2
                        class="tw-text-3xl dark-mode-text tw-font-bold mx-3 my-2">
                        Busqueda de pedidos
                    </h2>
                    <ECard>
                        <ValidationForm
                            v-slot="{ handleReset }"
                            @submit="onBuscarClick"
                            :validation-schema="purchaseForm">
                            <div class="row" align-v="start">
                                <div class="row">
                                    <ListBox
                                        class="col-4"
                                        top-label="Bodega"
                                        v-model="selectedWarehouse"
                                        placeholder="Filtro por bodega"
                                        label="name"
                                        :options="
                                            warehouse.getWarehouseList ?? []
                                        " />

                                    <div class="col-lg-4 col-xl-4 col-sm-6">
                                        <Datepicker
                                            v-model="
                                                purchaseForm.from_date.value
                                            "
                                            :max-date="
                                                purchaseForm.to_date?.value
                                            "
                                            show-now-button
                                            now-button-label="Ahora"
                                            auto-apply
                                            close-on-scroll
                                            textinput
                                            dark
                                            teleport-center>
                                            <template #dp-input="{ value }">
                                                <InputText
                                                    label="Fecha Mínima De Aprobación"
                                                    :model-value="value"
                                                    :info-label="
                                                        purchaseForm.from_date
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

                                    <div class="col-lg-4 col-xl-4 col-sm-6">
                                        <Datepicker
                                            v-model="purchaseForm.to_date.value"
                                            :min-date="
                                                purchaseForm.from_date?.value
                                            "
                                            show-now-button
                                            now-button-label="Ahora"
                                            auto-apply
                                            close-on-scroll
                                            textinput
                                            dark
                                            teleport-center>
                                            <template #dp-input="{ value }">
                                                <InputText
                                                    label="Fecha Máxima De Aprobación"
                                                    :model-value="value"
                                                    :info-label="
                                                        purchaseForm.to_date
                                                            .errorMessage
                                                    "
                                                    :status="
                                                        Boolean(
                                                            purchaseForm.to_date
                                                                .errorMessage
                                                        )
                                                    "
                                                    info-status="danger" />
                                            </template>
                                        </Datepicker>
                                    </div>
                                </div>
                                <div class="row">
                                    <ListBox
                                        class="col-4"
                                        top-label="Último Estado"
                                        v-model="selectedStatus"
                                        placeholder="Filtro por estado de la compra"
                                        label="display"
                                        :options="
                                            purchaseStore.getPurchaseStatus() ??
                                            []
                                        " />

                                    <div
                                        class="col-4 col-lg-4 col-xl-4 col-sm-6">
                                        <Datepicker
                                            v-model="
                                                purchaseForm.status_from_date
                                                    .value
                                            "
                                            :max-date="
                                                purchaseForm.status_to_date
                                                    ?.value
                                            "
                                            show-now-button
                                            now-button-label="Ahora"
                                            auto-apply
                                            close-on-scroll
                                            textinput
                                            dark
                                            teleport-center>
                                            <template #dp-input="{ value }">
                                                <InputText
                                                    label="Fecha Mínima Del Registro De Estado"
                                                    :model-value="value"
                                                    :info-label="
                                                        purchaseForm
                                                            .status_from_date
                                                            .errorMessage
                                                    "
                                                    :status="
                                                        Boolean(
                                                            purchaseForm
                                                                .status_from_date
                                                                .errorMessage
                                                        )
                                                    "
                                                    info-status="danger" />
                                            </template>
                                        </Datepicker>
                                    </div>

                                    <div
                                        class="col-3 col-lg-4 col-xl-4 col-sm-6">
                                        <Datepicker
                                            v-model="
                                                purchaseForm.status_to_date
                                                    .value
                                            "
                                            :min-date="
                                                purchaseForm.status_from_date
                                                    ?.value
                                            "
                                            show-now-button
                                            now-button-label="Ahora"
                                            auto-apply
                                            close-on-scroll
                                            textinput
                                            dark
                                            teleport-center>
                                            <template #dp-input="{ value }">
                                                <InputText
                                                    label="Fecha Máxima Del Registro De Estado"
                                                    :model-value="value"
                                                    :info-label="
                                                        purchaseForm
                                                            .status_to_date
                                                            .errorMessage
                                                    "
                                                    :status="
                                                        Boolean(
                                                            purchaseForm.to_date
                                                                .errorMessage
                                                        )
                                                    "
                                                    info-status="danger" />
                                            </template>
                                        </Datepicker>
                                    </div>
                                </div>

                                <div class="row">
                                    <div
                                        class="col-3 col-lg-6 col-xl-4 col-sm-12 mt-auto">
                                        <InputText
                                            v-model="
                                                purchaseForm.reference.value
                                            "
                                            :info-label="
                                                purchaseForm.reference
                                                    .errorMessage
                                            "
                                            :status="
                                                Boolean(
                                                    purchaseForm.reference
                                                        .errorMessage
                                                )
                                            "
                                            info-status="danger"
                                            label="Código de Compra" />
                                    </div>
                                    <div
                                        class="col-3 col-lg-4 col-xl-4 col-sm-6 mt-auto">
                                        <InputText
                                            v-model="
                                                purchaseForm.provider_name.value
                                            "
                                            :info-label="
                                                purchaseForm.provider_name
                                                    .errorMessage
                                            "
                                            :status="
                                                Boolean(
                                                    purchaseForm.provider_name
                                                        .errorMessage
                                                )
                                            "
                                            info-status="danger"
                                            label="Nombre de Provedor" />
                                    </div>
                                    <div class="row">
                                        <div
                                            class="col-2 mt-4 col-md-3 col-sm-4 mt-4 col-xl-2 col-lg-2 text-center">
                                            <e-button class="">
                                                Confirmar Búsqueda
                                            </e-button>
                                        </div>
                                        <div
                                            class="col-2 mt-4 col-md-3 col-sm-4 mt-4 col-xl-2 col-lg-2">
                                            <e-button
                                                @click.left="handleReset"
                                                type="button"
                                                variant="secondary">
                                                Limpiar Búsqueda
                                            </e-button>
                                        </div>
                                        <h2
                                            class="dark-mode-text col-6 mt-4 tw-text-lg tw-font-bold">
                                            <span
                                                class="tw-text-amber-700 dark:tw-text-amber-400">
                                                {{
                                                    (
                                                        paginatedPurchaseList ??
                                                        []
                                                    ).length
                                                }}
                                            </span>
                                            Registros encontrados
                                        </h2>
                                    </div>
                                </div>
                            </div>
                        </ValidationForm>
                    </ECard>
                </b-collapse>
                <div class="row mt-3">
                    <h1 class="title tw-font-bold mt-2 col-4 my-3">
                        Lista de todos los pedidos
                    </h1>
                    <e-button
                        v-b-toggle.collapse-1
                        type="button"
                        variant="primary"
                        class="col-6 mx-1 my-3 col-lg-2 col-xl-2 col-md-3 col-sm-4"
                        >Desplegar Búsqueda
                    </e-button>
                    <BTable
                        outline
                        :fields="purchasesFields"
                        :items="paginatedPurchaseList ?? []"
                        class="tw-capitalize dark-mode-text">
                        <template #cell(#)="{ index }">
                            {{
                                index + 1 + (currentPage - 1) * purchasePerPage
                            }}
                        </template>
                        <template #cell(BodegaDestino)="{ item }">
                            {{ item.warehouse.name }}
                        </template>
                        <template #cell(FechaAprobación)="{ item }">
                            {{ truncate(item.approved_at, 10, '') }}
                        </template>
                        'AprobadoPor',
                        <template #cell(AprobadoPor)="{ item }">
                            {{
                                item.order_origin.revised_by?.name
                                    ? truncate(
                                          item.order_origin.revised_by.name +
                                              ' ' +
                                              item.order_origin.revised_by
                                                  .lastname,
                                          20,
                                          '...'
                                      )
                                    : '--'
                            }}
                        </template>
                        <template #cell(RazónDeCompra)="{ item }">
                            {{
                                item.order_origin.comment
                                    ? truncate(
                                          item.order_origin.comment,
                                          25,
                                          '...'
                                      )
                                    : '---'
                            }}
                        </template>
                        <template #cell(Estado)="{ item }">
                            <BBadge
                                class="tw-text-md"
                                :variant="statusPurchaseColor(item.status)">
                                {{ getDisplayStatus(item.status) }}
                            </BBadge>
                        </template>
                        <template #cell(Acciones)="{ item }">
                            <e-button
                                left-icon="fa-eye"
                                type="button"
                                variant="primary"
                                @click.left="onDetallesClicked(item.id)"
                                >Ver detalles
                            </e-button>
                        </template>
                    </BTable>
                    <b-pagination
                        v-model="currentPage"
                        :total-rows="totalPurchaseCount"
                        :per-page="purchasePerPage"
                        align="center"
                        :limit="10"
                        hide-goto-end-buttons
                        class="paginator">
                    </b-pagination>
                </div>
            </div>
            <div class="container" v-else>
                <div class="row">
                    <h1 class="title my-2 tw-text-3xl col-9 dark-mode-text">
                        Información y Lista de productos en la compra #{{
                            selectedPurchase?.reference
                        }}
                    </h1>
                    <e-button
                        variant="primary"
                        type="button"
                        class="col-3 my-3"
                        @click.left="isPurchaseSelected = false">
                        Regresar a todas las compras
                    </e-button>
                </div>
                <div class="row my-2">
                    <div
                        class="tw-rounded tw-ring-2 my-2 tw-ring-yellow-400 tw-py-1 col-12 dark-mode-text tw-text-lg">
                        <div class="row">
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3 tw-font-bold">
                                Bodega Destino:
                            </span>
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3"
                                >{{ selectedPurchase?.warehouse?.name }}</span
                            >
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3 tw-font-bold">
                                Fecha de aprobación:
                            </span>
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3"
                                >{{
                                    moment(
                                        selectedPurchase?.approved_at
                                    ).format('dddd DD/MM/yyyy HH:mm:ss')
                                }}</span
                            >
                        </div>
                        <div class="row">
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3 tw-font-bold">
                                Comentarios de la orden
                            </span>
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3 text-break"
                                >{{
                                    selectedPurchase?.order_origin.comment
                                        ? selectedPurchase?.order_origin.comment
                                        : '(No se ingresó comentarios)'
                                }}</span
                            >
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3 tw-font-bold">
                                Orden revisada por:
                            </span>
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3"
                                >{{
                                    selectedPurchase?.order_origin.revised_by
                                        ?.name +
                                    ' ' +
                                    selectedPurchase?.order_origin.revised_by
                                        ?.lastname
                                }}</span
                            >
                        </div>
                    </div>
                </div>
                <ModalDialog
                    v-model:show="productInfoShow"
                    size="3xl"
                    class="dark-mode-text">
                    <template #dialog-title>
                        <b class="tw-text-2xl"
                            >Detalle del producto
                            {{
                                detailSelectedProduct?.product.product_name +
                                ' ' +
                                detailSelectedProduct?.variant.variant_name
                            }}</b
                        >
                    </template>
                    <div class="container">
                        <h3 class="tw-text-xl tw-font-bold">Detalle</h3>
                        <div
                            class="row tw-pb-3 align-content-center justify-content-center gy-2">
                            <template
                                v-for="(d, k) in detailSelectedProduct?.variant"
                                :key="k">
                                <div
                                    class="col-12"
                                    v-if="
                                        ![
                                            'base_price',
                                            'created_at',
                                            'updated_at',
                                            'is_active',
                                            'deleted_at',
                                        ].includes(k)
                                    ">
                                    <div class="row">
                                        <span class="tw-font-bold col-4"
                                            >{{ keyNaturalName(k) }}:</span
                                        >
                                        <span v-if="k == 'price'" class="col-4">
                                            {{ Number(d).toFixed(2) }}</span
                                        >
                                        <span v-else class="col-4">{{
                                            d
                                        }}</span>
                                    </div>
                                </div>
                            </template>

                            <div class="col-12">
                                <div class="row">
                                    <span class="col-4 tw-font-bold">
                                        Marca:
                                    </span>
                                    <span class="col-4">
                                        {{
                                            detailSelectedProduct?.product
                                                .brand_name
                                        }}
                                    </span>
                                </div>
                            </div>
                            <div class="row"></div>
                            <div class="col-12"></div>
                            <div class="col-12 mb-2">
                                <div class="row">
                                    <span class="col-4 tw-font-bold">
                                        Descripcion corta:
                                    </span>
                                    <p class="col-4 tw-text-ellipsis">
                                        {{
                                            detailSelectedProduct?.product
                                                .short_description
                                        }}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <LoadingBar v-show="loadingProps" class="tw-mt-5" />
                        <div
                            v-if="detailSelectedProduct?.props"
                            class="tw-ring-1 tw-ring-slate-500 tw-rounded tw-pb-3 row">
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
                                    class="col-6 col-md-3 col-xl-2 tw-text-md dark-mode-text">
                                    <b>{{ param.name }}:</b>
                                </div>
                                <div
                                    class="col-6 col-md-3 col-xl-2 dark-mode-text">
                                    <b>{{ param.value }}</b>
                                </div>
                            </template>
                        </div>
                    </div>
                </ModalDialog>
                <ModalDialog
                    v-model:show="showStatusAndChilds"
                    size="3xl"
                    class="dark-mode-text">
                    <div class="container">
                        <div
                            class="row mb-2 tw-ring-2 dark:tw-ring-white py-2 tw-ring-black">
                            <div class="col-3 tw-text-md">
                                <b>Orden origen de la compra:</b>
                            </div>
                            <div class="col-3 tw-font-light">
                                <b> #{{ selectedPurchase?.order_origin.id }}</b>
                            </div>
                            <div class="col-3 tw-text-md">
                                <b>Revisada por: </b>
                            </div>
                            <div class="col-3 tw-font-light">
                                <b>
                                    {{
                                        selectedPurchase?.order_origin
                                            .revised_by?.name +
                                        ' ' +
                                        selectedPurchase?.order_origin
                                            .revised_by?.lastname
                                    }}
                                </b>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="col-6 tw-text-md">
                                <b>Fecha de revisión: </b>
                            </div>
                            <div class="col-6 tw-font-light">
                                <b>
                                    {{
                                        moment(
                                            selectedPurchase?.order_origin
                                                .revised_at
                                        ).format('dddd DD/MM/yyyy HH:mm:ss')
                                    }}
                                </b>
                            </div>
                        </div>

                        <div class="row mb-2">
                            <div class="col-6 tw-text-md dark-mode-text">
                                <b>Commentario de la orden:</b>
                            </div>
                            <div
                                class="col-6 tw-font-light text-break text-wrap">
                                <b>
                                    ({{
                                        selectedPurchase?.order_origin.comment
                                            ? selectedPurchase?.order_origin
                                                  .comment
                                            : 'Sin comentarios'
                                    }})
                                </b>
                            </div>
                        </div>
                    </div>
                    <e-button
                        v-b-toggle.order-collapse
                        variant="primary"
                        type="button"
                        class="col-4 mb-2">
                        Ver Estados De La Orden
                    </e-button>
                    <b-collapse id="order-collapse">
                        <template
                            v-for="(order, ix) of selectedPurchase?.order_origin
                                .status_list"
                            :key="ix">
                            <div
                                class="row tw-ring-2 dark:tw-ring-white py-2 tw-ring-black mb-3 pt-3 tw-capitalize">
                                <div class="row col-12">
                                    <BBadge
                                        class="tw-text-lg mx-2 col-5"
                                        :variant="
                                            statusOrderColor(order.status)
                                        ">
                                        {{
                                            '( ' +
                                            (ix + 1) +
                                            ' ) ' +
                                            parseStatus(order.status)
                                        }}
                                    </BBadge>

                                    <div class="col-3 tw-text-md">
                                        <b>Creado por: </b>
                                    </div>
                                    <div class="col-3 tw-font-light">
                                        <b>
                                            {{
                                                order.created_by?.name +
                                                ' ' +
                                                order.created_by?.lastname
                                            }}
                                        </b>
                                    </div>
                                </div>
                                <div class="row mb-2 allign-content-end mt-2">
                                    <div class="col-3 tw-text-md">
                                        <b>Fecha : </b>
                                    </div>
                                    <div class="col-6 tw-font-light">
                                        <b>
                                            {{
                                                moment(order.created_at).format(
                                                    'dddd DD/MM/yyyy HH:mm:ss'
                                                )
                                            }}
                                        </b>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </b-collapse>

                    <div class="row tw-text-lg tw-font-bold mb-3">
                        Estados de la compra:
                    </div>

                    <template
                        v-for="(status, ix) in selectedPurchase?.status_list"
                        :key="ix">
                        <div
                            class="row tw-ring-2 dark:tw-ring-white py-2 tw-ring-black mb-3 pt-3 tw-capitalize">
                            <div class="row col-12">
                                <BBadge
                                    class="tw-text-lg mx-2 col-5"
                                    :variant="
                                        statusPurchaseColor(status.status)
                                    ">
                                    {{
                                        '( ' +
                                        (ix + 1) +
                                        ' ) ' +
                                        getDisplayStatus(status.status)
                                    }}
                                </BBadge>

                                <div class="col-3 tw-text-md">
                                    <b>Creado por: </b>
                                </div>
                                <div class="col-3 tw-font-light">
                                    <b>
                                        {{
                                            status.created_by?.name +
                                            ' ' +
                                            status.created_by?.lastname
                                        }}
                                    </b>
                                </div>
                            </div>
                            <div class="row mb-2 allign-content-end mt-2">
                                <div class="col-3 tw-text-md">
                                    <b>Fecha : </b>
                                </div>
                                <div class="col-6 tw-font-light">
                                    <b>
                                        {{
                                            moment(status.created_at).format(
                                                'dddd DD/MM/yyyy HH:mm:ss'
                                            )
                                        }}
                                    </b>
                                </div>
                            </div>
                        </div>
                    </template>
                </ModalDialog>
                <div class="row">
                    <InputText
                        v-model="searchString"
                        label="Búsqueda de producto"
                        class="col-3" />

                    <e-button
                        variant="primary"
                        class="col-3 my-4"
                        @click="showStatusAndChilds = true">
                        Ver estados de la Compra
                    </e-button>
                    <ListBox
                        class="col-4 mx-2"
                        top-label="Proveedor"
                        v-model="selectedProvider"
                        placeholder="Filtro por proveedor"
                        label="name"
                        @change="filterProvider"
                        :options="providerList ?? []" />
                </div>
                <div class="row">
                    <BTable
                        :fields="detailsFields"
                        outline
                        class="tw-capitalize dark-mode-text"
                        :items="paginatedPurchaseDetailsArr ?? []">
                        <template #cell(#)="{ index }">
                            {{
                                index +
                                1 +
                                (currentDetailsPage - 1) * purchasePerPage
                            }}
                        </template>
                        <template #cell(Código)="{ item }">
                            {{ item.variant.sku }}
                        </template>
                        <template #cell(Nombre)="{ item }">
                            {{
                                item.product.product_name +
                                ' ' +
                                item.variant.variant_name
                            }}
                        </template>
                        <template #cell(PrecioDeCompra)="{ item }">
                            {{ Number(item.price).toFixed(2) }}
                        </template>
                        <template #cell(PrecioDeVenta)="{ item }">
                            {{ Number(item.variant.price).toFixed(2) }}
                        </template>
                        <template #cell(Cantidad)="{ item }">
                            {{ item.quantity }}
                        </template>
                        <template #cell(Proveedor)="{ item }">
                            {{ item.provider.name }}
                        </template>
                        <template #cell(Acciones)="{ item }">
                            <e-button
                                type="button"
                                variant="primary"
                                @click.left="showProduct(item)">
                                Ver Detalles
                            </e-button>
                        </template>
                    </BTable>
                    <b-pagination
                        v-model="currentDetailsPage"
                        :total-rows="purchaseDetailsArr?.length"
                        :per-page="purchasePerPage"
                        align="center"
                        :limit="10"
                        hide-goto-end-buttons
                        class="paginator">
                    </b-pagination>
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
