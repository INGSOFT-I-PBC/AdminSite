<script setup lang="ts">
    import { useItemStore, useWarehouseStore } from '@store'
    import { useOrderStore } from '@store/order'
    import {
        type PurchaseFromOrderData,
        usePurchaseStore,
    } from '@store/purchase'
    import {
        type OrderRequestInfo,
        type PaginatedResponse,
        type ProductProps,
        type ProductProvider,
        type VarinatProductI,
        type Warehouse,
        isMessage,
    } from '@store/types'
    import type {
        FullOrderDetail,
        OrderQuery,
        OrderRequestStatus,
        SaveOrderDetail,
    } from '@store/types/orders.model'
    import {
        BBadge,
        BPagination,
        BTable,
        type ColorVariant,
        type TableField,
    } from 'bootstrap-vue-3'
    import moment from 'moment'

    import { computed, onMounted, watch } from 'vue'
    import { useRouter } from 'vue-router'
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

    const router = useRouter()

    const toast = useToast()

    const warehouseStore = useWarehouseStore()

    moment.updateLocale('es', {
        weekdays: 'Domingo_Lunes_Martes_Miércoles_Jueves_Viernes_Sábado'.split(
            '_'
        ),
    })

    const tableFields: TableField[] = [
        '#',
        { label: 'Código', key: 'id' },
        'BodegaDestino',
        'FechaDelPedido',
        'NombreSolicitador',
        'Estado',
        'Acciones',
    ]

    const detailsFields: TableField[] = [
        '#',
        'CódigoProducto',
        'NombreProducto',
        'Precio',
        'Stock',
        'Marca',
        'Acciones',
        'Cantidad',
    ]

    const orderStore = useOrderStore()

    const purchaseStore = usePurchaseStore()

    const itemStore = useItemStore()

    const showWaitOverlay = ref<boolean>(true)

    const selectedWarehouse = ref<Warehouse>()

    const selectedOrder = ref<OrderRequestInfo>()

    const productInfoShow = ref<boolean>(false)

    const stopWatcher = ref<boolean>(false)

    const searchProductString = ref<string>('')

    type DetailTableData = FullOrderDetail & {
        selected_provider?: ProductProvider
        index: number
    }

    const orderTableDetailsArr = ref<DetailTableData[]>([])

    const paginatedDetailsArr = ref<DetailTableData[]>()

    const providerList = ref<ProductProvider[]>([])

    const selectedProvider = ref<ProductProvider>()

    const selectedDetail = ref<DetailTableData>()

    const currentDetailsPage = ref<number>(1)
    const detailsPaginatedCurrentPage = computed(() => ({
        page: currentDetailsPage.value,
    }))

    const serverOpts = ref({
        page: 1,
        per_page: 15,
    })

    const paginationOptions = computed<PaginationOptions>(() => ({
        page: serverOpts.value.page,
        per_page: serverOpts.value.per_page,
    }))

    const searchOptions = ref<OrderQuery>({
        id: undefined,
        warehouse_id: undefined,
        requested_by_name: undefined,
    })

    const searchNameString = ref<string>('')

    const totalRows = ref<number>(0)

    const orderRequestArray = ref<OrderRequestInfo[]>([])

    const detailsShow = ref<boolean>(false)

    type SelectedItem = {
        item: VarinatProductI
        props: ProductProps[]
    }
    const detailSelectedProduct = ref<SelectedItem>()

    const loadingProps = ref<boolean>(false)

    async function cleanSearch() {
        searchOptions.value.id = undefined
        searchOptions.value.warehouse_id = undefined
        searchOptions.value.requested_by_name = undefined
        searchNameString.value = ''
        fetchOrderRequest()
    }

    function filterData(): void {
        stopWatcher.value = true
        if (selectedProvider.value && orderTableDetailsArr.value) {
            currentDetailsPage.value = 1
            paginatedDetailsArr.value = orderTableDetailsArr.value
                .filter(d => {
                    return d.selected_provider?.provider.name.includes(
                        selectedProvider.value?.provider.name
                            ? selectedProvider.value?.provider.name
                            : ''
                    )
                })
                .slice(
                    (detailsPaginatedCurrentPage.value.page - 1) *
                        serverOpts.value.per_page,
                    detailsPaginatedCurrentPage.value.page *
                        serverOpts.value.per_page
                )
        } else if (
            searchProductString.value.length > 0 &&
            orderTableDetailsArr.value
        ) {
            currentDetailsPage.value = 1
            paginatedDetailsArr.value = orderTableDetailsArr.value
                .filter(d => {
                    return d.selected_provider?.provider.name.includes(
                        selectedProvider.value?.provider.name
                            ? selectedProvider.value?.provider.name
                            : ''
                    )
                })
                .slice(
                    (detailsPaginatedCurrentPage.value.page - 1) *
                        serverOpts.value.per_page,
                    detailsPaginatedCurrentPage.value.page *
                        serverOpts.value.per_page
                )
        } else {
            paginatedDetailsArr.value = paginatedDetailsArr.value?.slice(
                (detailsPaginatedCurrentPage.value.page - 1) *
                    serverOpts.value.per_page,
                detailsPaginatedCurrentPage.value.page *
                    serverOpts.value.per_page
            )
        }

        stopWatcher.value = false
    }

    function onDetailsPageChange() {
        if (!stopWatcher.value) {
            filterData()
        }
    }

    async function fetchOrderRequest() {
        showWaitOverlay.value = true

        if (selectedWarehouse.value) {
            searchOptions.value.warehouse_id = selectedWarehouse.value.id
        }
        if (searchNameString.value) {
            searchOptions.value.requested_by_name = searchNameString.value
        }

        let response = await orderStore.fetchOrdersRequestWithInfo({
            ...paginationOptions.value,
            ...searchOptions.value,
        })

        if (isMessage(response)) {
            toast.error('Error al cargar ordenes')
            showWaitOverlay.value = false
            totalRows.value = 0
            return
        }

        response = response as PaginatedResponse<OrderRequestInfo>

        if (response.data.length == 0) {
            toast.error('No se han encontrado solicitudes')
            showWaitOverlay.value = false
            totalRows.value = 0
            return
        }

        toast.success('Se han encontrado ' + response.total + ' solicitudes')

        orderRequestArray.value = response.data

        totalRows.value = response.total

        showWaitOverlay.value = false
    }

    function onOrderSelected(order: OrderRequestInfo): void {
        selectedOrder.value = order
        showWaitOverlay.value = true
        orderStore
            .fetchOrdersDetails({ order_id: order.id })
            .then(it => {
                if (isMessage(it)) {
                    toast.error('No se puedo cargar los detalles')

                    router.push({
                        path: `/bodegas/tablas-solicitudes-pedidos}`,
                    })
                    showWaitOverlay.value = false
                    return
                }
                for (let i = 0; i < it.length; i++) {
                    orderTableDetailsArr.value.push({ ...it[i], index: i })
                }
                if (orderTableDetailsArr.value.length == 0) {
                    toast.error('No se han encontrado registros')
                    showWaitOverlay.value = false
                    return
                }
                detailsShow.value = true
            })
            .catch(() => {
                toast.error('Error de carga')
                showWaitOverlay.value = false
            })
        showWaitOverlay.value = false
    }

    //Details functions

    function chooseProvider(provider: ProductProvider) {
        if (!selectedDetail.value) {
            toast.error('Error, vuelva a elegir un producto de la tabla')
            return
        }

        if (selectedDetail.value.selected_provider) {
            providerList.value.splice(
                providerList.value.findIndex(
                    p =>
                        p.provider.name ==
                        selectedDetail.value?.selected_provider?.provider.name
                ),
                1
            )
        }

        selectedDetail.value.selected_provider = provider
        orderTableDetailsArr.value[
            selectedDetail.value.index
        ].selected_provider = provider

        if (paginatedDetailsArr.value) {
            const idx = paginatedDetailsArr.value.findIndex(
                d => d.index == selectedDetail.value?.index
            )

            if (idx > 0) {
                paginatedDetailsArr.value[idx].selected_provider = provider
            }
        }
        toast.success('Selección de proveedor confirmado')
    }

    async function confirmPurchase() {
        if (!selectedOrder.value) {
            toast.error('Error, intente seleccionar una orden de nuevo')
            return
        }
        const details: {
            provider: number
            products: SaveOrderDetail[]
        }[] = []

        const proxyProviders: number[] = []
        const proxyDetails: SaveOrderDetail[][] = []

        for (const detail of orderTableDetailsArr.value) {
            if (!detail.selected_provider) {
                toast.error(
                    'Seleccione el provedor del producto: ' +
                        detail.item.product.product_name +
                        '/' +
                        detail.item.variant_name,
                    { timeout: 4500 }
                )
                return
            }

            const index = proxyProviders.indexOf(
                detail.selected_provider.provider.id
            )

            if (index < 0) {
                proxyProviders.push(detail.selected_provider.provider.id)
                const push_data: SaveOrderDetail[] = [
                    {
                        item: detail.item.id,
                        price: detail.selected_provider.price,
                        quantity: detail.quantity,
                    },
                ]
                proxyDetails.push(push_data)
            } else {
                proxyDetails[index].push({
                    item: detail.item.id,
                    price: detail.selected_provider.price,
                    quantity: detail.quantity,
                })
            }
        }

        for (let idx = 0; idx < proxyProviders.length; idx++) {
            details.push({
                provider: proxyProviders[idx],
                products: proxyDetails[idx],
            })
        }

        const saveOrederData: PurchaseFromOrderData = {
            warehouse_id: selectedOrder.value.warehouse.id,
            order_id: selectedOrder.value.id,
            details: details,
        }

        purchaseStore.savePurchaseFromOrder(saveOrederData).then(it => {
            if (isMessage(it)) {
                if (it.code == '200') {
                    toast.success('Compra aprobada con éxito')
                }
            }
        })
    }

    async function showProduct(picked: FullOrderDetail): Promise<void> {
        const object = {
            item: picked.item,
            props: [],
        }
        detailSelectedProduct.value = object
        productInfoShow.value = true
        loadingProps.value = true
        let res = await itemStore.fetchProductProperties({
            variant_id: picked.item.id,
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

    function statusColor(status?: OrderRequestStatus): ColorVariant {
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
    function parseStatus(status?: OrderRequestStatus): string {
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

    onMounted(() => {
        warehouseStore.fetchWarehouses()
        fetchOrderRequest()
    })

    watch(serverOpts, fetchOrderRequest)
    watch(currentDetailsPage, onDetailsPageChange)
</script>

<template>
    <main>
        <ECard>
            <WaitOverlay :show="showWaitOverlay">
                <div v-if="!detailsShow">
                    <div class="row">
                        <h1 class="dark-mode-text tw-text-xl">
                            Últimas solicitudes de compras
                        </h1>
                    </div>
                    <div class="row">
                        <div class="col-3">
                            <ListBox
                                :options="warehouseStore.getWarehouseList ?? []"
                                v-model="selectedWarehouse"
                                top-label="Búsqueda por bodega"
                                placeholder="No ha seleccionado una bodega"
                                label="name" />
                        </div>

                        <div class="col-3">
                            <InputText
                                v-model="searchNameString"
                                label="Búsqueda por nombre de solicitante"
                                placeholder="Ingrese un nombre o apellido" />
                        </div>

                        <div class="col-3 mt-4">
                            <EButton
                                @click.left="fetchOrderRequest"
                                type="button"
                                varinat="primary">
                                Buscar
                            </EButton>
                        </div>

                        <div class="col-3 mt-4">
                            <EButton
                                @click.left="cleanSearch"
                                variant="secondary"
                                type="button">
                                Limpiar Búsqueda
                            </EButton>
                        </div>

                        <h2
                            class="dark-mode-text col-6 mt-4 tw-text-lg tw-font-bold">
                            <span
                                class="tw-text-amber-700 dark:tw-text-amber-400">
                                {{ totalRows }}
                            </span>
                            Registros encontrados
                        </h2>
                    </div>

                    <div class="row">
                        <BPagination
                            v-model="serverOpts.page"
                            :total-rows="totalRows"
                            :per-page="serverOpts.per_page"
                            align="center"
                            :limit="10"
                            hide-goto-end-buttons
                            class="paginator">
                        </BPagination>
                    </div>

                    <div
                        class="row align-content-center justify-content-center mt-3"
                        v-if="totalRows == 0">
                        <h1 class="tw-text-2xl dark-mode-text">
                            No se han encontrado registros, intente otra
                            búsqueda.
                        </h1>
                    </div>

                    <div class="row" v-else>
                        <BTable
                            :items="orderRequestArray"
                            :fields="tableFields"
                            class="table"
                            hover>
                            <template #cell(#)="{ index }">
                                {{ index + 1 }}
                            </template>
                            <template #cell(BodegaDestino)="{ item }">
                                {{ item.warehouse.name }}
                            </template>
                            <template #cell(NombreSolicitador)="{ item }">
                                {{
                                    item.requested_by.name +
                                    ' ' +
                                    item.requested_by.lastname
                                }}
                            </template>
                            <template #cell(FechaDelPedido)="{ item }">
                                <b>
                                    {{
                                        moment(item.requested_at).format(
                                            'dddd DD/MM/yyyy HH:mm:ss'
                                        )
                                    }}
                                </b>
                            </template>
                            <template #cell(Estado)="{ item }">
                                <BBadge
                                    :variant="statusColor(item.status)"
                                    class="tw-text-sm">
                                    {{ parseStatus(item.status) }}
                                </BBadge>
                            </template>

                            <template #cell(Acciones)="{ item }">
                                <EButton @click.left="onOrderSelected(item)">
                                    Ver Detalles
                                </EButton>
                            </template>
                        </BTable>
                    </div>
                </div>
                <div v-else>
                    <div class="row">
                        <h1 class="dark-mode-text tw-text-xl col-8">
                            Detalles de la solicitud
                        </h1>
                    </div>
                    <e-button
                        variant="primary"
                        type="button"
                        class="col-3 my-3"
                        @click.left="detailsShow = false">
                        Regresar a todas las solicitudes
                    </e-button>
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
                                    >{{ selectedOrder?.warehouse?.name }}</span
                                >
                                <span
                                    class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3 tw-font-bold">
                                    Fecha de creación:
                                </span>
                                <span
                                    class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3"
                                    >{{
                                        moment(
                                            selectedOrder?.requested_at
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
                                        selectedOrder?.comment
                                            ? selectedOrder.comment
                                            : '(No se ingresó comentarios)'
                                    }}</span
                                >
                                <template v-if="selectedOrder?.revised_at">
                                    <span
                                        class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3 tw-font-bold">
                                        Orden revisada por:
                                    </span>
                                    <span
                                        class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3"
                                        >{{
                                            selectedOrder.revised_by?.name +
                                            ' ' +
                                            selectedOrder.revised_by?.lastname
                                        }}</span
                                    >
                                </template>
                            </div>
                        </div>
                    </div>
                    <ModalDialog
                        v-model:show="productInfoShow"
                        size="3xl"
                        class="dark-mode-text">
                        <template>
                            <b class="tw-text-2xl"
                                >Detalle del producto
                                {{
                                    detailSelectedProduct?.item.product
                                        .product_name +
                                    ' ' +
                                    detailSelectedProduct?.item.variant_name
                                }}</b
                            >
                        </template>
                        <div class="container">
                            <h3 class="tw-text-xl tw-font-bold">Detalle</h3>
                            <div
                                class="row tw-pb-3 align-content-center justify-content-center gy-2">
                                <template
                                    v-for="(
                                        d, k
                                    ) in detailSelectedProduct?.item"
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
                                                'product',
                                            ].includes(k)
                                        ">
                                        <div class="row">
                                            <span class="tw-font-bold col-4"
                                                >{{ keyNaturalName(k) }}:</span
                                            >
                                            <span
                                                v-if="k == 'price'"
                                                class="col-4">
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
                                                detailSelectedProduct?.item
                                                    .product.brand_name
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
                                                detailSelectedProduct?.item
                                                    .product.short_description
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
                    <div class="row">
                        <InputText
                            v-model="searchProductString"
                            label="Búsqueda de producto"
                            class="col-3" />
                        <ListBox
                            class="col-4 mx-2"
                            top-label="Proveedor"
                            v-model="selectedProvider"
                            placeholder="Filtro por proveedor"
                            label="name"
                            @change="filterData"
                            :options="providerList ?? []" />
                    </div>
                    <div class="row">
                        <BTable
                            :fields="detailsFields"
                            outline
                            class="tw-capitalize dark-mode-text"
                            :items="paginatedDetailsArr ?? []">
                            <template #cell(#)="{ index }">
                                {{
                                    index +
                                    1 +
                                    (detailsPaginatedCurrentPage.page - 1) *
                                        serverOpts.per_page
                                }}
                            </template>
                            <template #cell(CódigoProducto)="{ item }">
                                {{ item.sku }}
                            </template>
                            <template #cell(NombreProducto)="{ item }">
                                {{
                                    item.item.product.product_name +
                                    ' ' +
                                    item.variant_name
                                }}
                            </template>
                            <template #cell(PrecioDeCompra)="{ item }">
                                {{ Number(item.provider.price).toFixed(2) }}
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
                            :total-rows="orderTableDetailsArr.length"
                            :per-page="serverOpts.per_page"
                            align="center"
                            :limit="10"
                            hide-goto-end-buttons
                            class="paginator">
                        </b-pagination>
                    </div>
                </div>
            </WaitOverlay>
        </ECard>
    </main>
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
            @apply tw-text-xs;
        }

        @media (prefers-color-scheme: dark) {
            color: white !important;
            --bs-table-striped-color: theme(colors.zinc.400);
            --bs-table-hover-color: theme('colors.primary.light');
            --bs-table-hover-bg: theme(colors.primary.light / 15%);
        }
    }
</style>
