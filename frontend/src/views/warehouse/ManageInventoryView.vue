<script setup lang="ts">
    import { useItemStore, useWarehouseStore } from '@store'
    import {
        type FullTomaFisicaDetail,
        type PaginatedResponse,
        type ProductProps,
        type ProductVariant,
        type SimpleProduct,
        type TomaFisicaDetail,
        type TomaSaveData,
        type Warehouse,
        isMessage,
    } from '@store/types'
    import { BPagination } from 'bootstrap-vue-3'

    import { ref, watch } from 'vue'
    import { useToast } from 'vue-toastification'

    import {
        EButton,
        ECard,
        ListBox,
        LoadingBar,
        ModalDialog,
        TextArea,
        WaitOverlay,
    } from '@custom-components'

    const warehouseStore = useWarehouseStore()
    const itemStore = useItemStore()
    const toast = useToast()

    const loadingState = ref({
        waitWarehouse: true,
        waitData: false,
    })

    const PENDING_APPROVAL = { name: 'PA', display: 'Aprobación Pendiente' }
    const ACEPTED = { name: 'AP', display: 'Aceptado' }
    const NOT_ACEPTED = { name: 'NA', display: 'Rechazado' }

    const toggle = ref<boolean>(true)

    const formOptions = ref([PENDING_APPROVAL, ACEPTED, NOT_ACEPTED])

    const searchForm = ref({
        acepted: { name: 'n/a', displau: '' },
        search_name: '',
    })

    const currentAsidePage = ref<number>(1)
    const whRows = ref<number>(0)
    const paginatedWarehouse = ref<Warehouse[]>()
    const whPageCount = ref<number>(15)
    const activeWharehouseButton = ref<number>(-1)
    const selectedWarehouse = ref<Warehouse>()
    const showConfirmChange = ref<boolean>(false)
    const isConfirmarModal = ref<boolean>(false)

    const tomaDetailsArray = ref<FullTomaFisicaDetail[]>([])

    const tomasTotal = ref<number>(0)

    const selectedTomaDetail = ref<FullTomaFisicaDetail>()

    const serverOpts = ref({
        page: 1,
        rowsPerPage: 15,
    })

    function isPreviousStockLower() {
        if (selectedTomaDetail.value) {
            return (
                selectedTomaDetail.value.previous_stock <
                selectedTomaDetail.value.new_stock
            )
        }
    }

    const paginationOptions = computed(() => ({
        page: serverOpts.value.page,
        per_page: serverOpts.value.rowsPerPage,
    }))

    const productInfoShow = ref<boolean>(false)
    type SelectedItem = {
        product: SimpleProduct
        variant: ProductVariant
        props: ProductProps[]
    }
    const detailSelectedProduct = ref<SelectedItem>()
    const loadingProps = ref<boolean>(false)

    function onSelectedTomaDetailPressed(
        toma: FullTomaFisicaDetail,
        status: 'AP' | 'NA'
    ) {
        if (status == ACEPTED.name) {
            isConfirmarModal.value = true
        } else if (status == NOT_ACEPTED.name) {
            isConfirmarModal.value = false
        }

        if (toma != selectedTomaDetail.value) {
            aceptedCommentString.value = ''
        }
        selectedChangeStatus.value = status
        selectedTomaDetail.value = toma
        showConfirmChange.value = true
    }

    function paginateAside() {
        paginatedWarehouse.value = (
            warehouseStore.getWarehouseList ?? []
        ).slice(
            (currentAsidePage.value - 1) * whPageCount.value,
            currentAsidePage.value * whPageCount.value
        )
    }

    async function onMainPaginationPressed() {
        loadingState.value.waitData = true

        const res = await warehouseStore.fetchPaginatedTomasFisicasDetails(
            {
                warehouse_id: selectedWarehouse.value?.id,
                acepted: searchForm.value.acepted.name,
            },
            paginationOptions.value
        )

        if (isMessage(res)) {
            toast.error('Error al cargar más detalles')
            loadingState.value.waitData = false
            return
        }

        tomaDetailsArray.value = res.data as FullTomaFisicaDetail[]
    }

    const selectedChangeStatus = ref<string>('AP')
    const aceptedCommentString = ref<string>('')

    function updateCambioStatus() {
        if (!isConfirmarModal.value && !aceptedCommentString.value) {
            toast.error(
                'Debe ingresar la razón del rechazo, vuelva a intentarlo'
            )
            return
        }

        const isOverMaxChars: boolean = aceptedCommentString.value.length
            ? aceptedCommentString.value.length > 150
            : false

        if (isOverMaxChars) {
            toast.error('Máximo de caracteres excedido, vuelva a intentarlo', {
                timeout: 2300,
            })
            return
        }

        if (selectedTomaDetail.value && selectedWarehouse.value) {
            loadingState.value.waitWarehouse = true
            if (selectedTomaDetail.value.id) {
                const difference =
                    selectedTomaDetail.value.new_stock -
                    selectedTomaDetail.value.previous_stock
                if (
                    selectedTomaDetail.value.warehouse_stock + difference < 0 &&
                    selectedChangeStatus.value == 'AP'
                ) {
                    toast.error(
                        'Stock de bodega cambio y no puede ser negativo, revise el cambio de inventario',
                        { timeout: 4500 }
                    )
                    loadingState.value.waitWarehouse = false
                    return
                }

                warehouseStore
                    .updateTomaFisicaDetail({
                        warehouse_id: selectedWarehouse.value.id,
                        previous_stock: selectedTomaDetail.value.previous_stock,
                        new_stock: selectedTomaDetail.value.new_stock,
                        id: selectedTomaDetail.value.id,
                        product: selectedTomaDetail.value?.product.id,
                        variant: selectedTomaDetail.value?.variant.id,
                        acepted: selectedChangeStatus.value,
                        acepted_comment:
                            aceptedCommentString.value.length > 0
                                ? aceptedCommentString.value
                                : undefined,
                    })
                    .then(it => {
                        if (selectedTomaDetail.value) {
                            selectedTomaDetail.value.acepted =
                                selectedChangeStatus.value
                        }

                        toast.success('Cambio actualizado con éxito')
                        loadingState.value.waitWarehouse = false

                        if (
                            selectedTomaDetail.value &&
                            selectedChangeStatus.value == 'AP'
                        ) {
                            const sameProductArray =
                                tomaDetailsArray.value.filter(
                                    t =>
                                        t.variant.id ==
                                            selectedTomaDetail.value?.variant
                                                .id &&
                                        t.product.id ==
                                            selectedTomaDetail.value?.product.id
                                )

                            for (const toma of sameProductArray) {
                                toma.warehouse_stock += difference
                            }
                        }
                    })
                    .catch(it => {
                        toast.error(
                            'No se pudo realizar la actualización / ' + it.code
                        )
                        loadingState.value.waitWarehouse = false
                    })
            }
        }
    }

    async function showProduct(picked: FullTomaFisicaDetail): Promise<void> {
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
    function onSelectedStatusChange() {
        loadingState.value.waitWarehouse = true

        tomaDetailsArray.value = []
        if (selectedWarehouse.value) {
            warehouseStore
                .fetchPaginatedTomasFisicasDetails(
                    {
                        warehouse_id: selectedWarehouse.value.id,
                        acepted: searchForm.value.acepted.name,
                    },
                    paginationOptions.value
                )
                .then((it): void => {
                    if (isMessage(it)) {
                        toast.error('Error')
                    } else {
                        tomaDetailsArray.value = it.data
                        tomasTotal.value = it.total
                    }
                    if (tomaDetailsArray.value.length == 0) {
                        toast.error('No se han encontrado registros')
                    }

                    loadingState.value.waitWarehouse = false
                })
                .catch((e): void => {
                    toast.error(e.message)
                    loadingState.value.waitWarehouse = false
                })
                .finally(() => {
                    loadingState.value.waitWarehouse = false
                })
        }
    }

    function wharehouseButtonPressed(wh: Warehouse, index: number) {
        activeWharehouseButton.value = index

        selectedWarehouse.value = wh

        loadingState.value.waitWarehouse = true

        tomaDetailsArray.value = []

        warehouseStore
            .fetchPaginatedTomasFisicasDetails(
                { warehouse_id: wh.id, acepted: 'PA' },
                paginationOptions.value
            )
            .then((it): void => {
                if (isMessage(it)) {
                    toast.error('Error')
                } else {
                    tomaDetailsArray.value = it.data
                    tomasTotal.value = it.total
                }

                if (tomaDetailsArray.value.length == 0) {
                    toast.warning('No hay cambios pendientes para esta bodega')
                }

                loadingState.value.waitWarehouse = false
            })
            .catch((e): void => {
                toast.error(e.message)
                loadingState.value.waitWarehouse = false
            })
            .finally(() => {
                loadingState.value.waitWarehouse = false
            })
    }

    warehouseStore
        .fetchWarehouses()
        .then((): void => {
            whRows.value = (warehouseStore.getWarehouseList ?? []).length
            paginateAside()
            loadingState.value.waitWarehouse = false
        })
        .catch((): void => {
            toast.error('Error en la carga de datos')
            loadingState.value.waitWarehouse = false
        })
    watch(serverOpts.value, onMainPaginationPressed)
    watch(currentAsidePage, paginateAside)
</script>

<template>
    <WaitOverlay :show="loadingState.waitWarehouse">
        <ECard>
            <div
                class="row d-inline-flex allign-content-center tw-bg-slate-50 dark:tw-bg-slate-600">
                <div
                    v-if="toggle"
                    class="col-sm-12 col-md-12 col-xl-2 tw-flex-col tw-rounded-lg tw-bg-white dark:tw-bg-slate-800 justify-center">
                    <h1 class="title my-2">Bodegas Disponibles</h1>

                    <e-button
                        @click.left="
                            () => {
                                toggle = false
                            }
                        "
                        class="tw-text-slate-800 col-lg-3 col-md-3 col-sm-6 col-xl-6 mx-3 mb-3"
                        left-icon="chevrons-left"
                        icon-provider="feather">
                    </e-button>

                    <b-pagination
                        v-model="currentAsidePage"
                        :total-rows="whRows"
                        :per-page="whPageCount"
                        aria-controls="b-list-warehouses"
                        :limit="3"
                        hide-goto-end-buttons
                        class="paginator mb-2"></b-pagination>

                    <b-list-group
                        :per-page="whPageCount"
                        :current-page="currentAsidePage"
                        class="button-group smaller-btn-group col-lg-12 col-md-6 col-sm-6">
                        <b-list-group-item
                            :class="{ active: activeWharehouseButton === -1 }"
                            button
                            @click.left="
                                () => {
                                    activeWharehouseButton = -1
                                }
                            ">
                            Inicio
                        </b-list-group-item>
                        <b-list-group-item
                            v-for="(wh, index) in paginatedWarehouse"
                            button
                            :class="{
                                active: wh.id === activeWharehouseButton,
                            }"
                            :key="wh.id"
                            :id="'whbtn-' + wh.id"
                            @click.left="wharehouseButtonPressed(wh, index)">
                            {{ wh.name }}
                        </b-list-group-item>
                    </b-list-group>
                </div>
                <div
                    class="col-xl align-middle d-flex justify-content-center tw-mt-5"
                    v-if="activeWharehouseButton == -1">
                    <h1 class="dark-mode-text tw-text-2xl tw-align-middle">
                        Seleccione una bodega para empezar
                    </h1>
                </div>
                <div v-else class="col-xl tw-bg-slate-50 dark:tw-bg-slate-700">
                    <div
                        class="row align-middle d-flex justify-content-center tw-mt-2">
                        <e-button
                            v-if="!toggle"
                            @click.left="
                                () => {
                                    toggle = true
                                }
                            "
                            class="tw-text-slate-800 tw-text-sm mx-1 col-1"
                            left-icon="chevrons-right"
                            icon-provider="feather">
                        </e-button>
                        <h1 class="tw-text-3xl tw-font-bold col-9">
                            {{ selectedWarehouse?.name }}
                        </h1>

                        <h2
                            class="dark-mode-text col-3 tw-text-lg tw-font-bold">
                            <span
                                class="tw-text-amber-700 dark:tw-text-amber-400">
                                {{ tomaDetailsArray?.length }}
                            </span>
                            Registros encontrados
                        </h2>
                    </div>

                    <ECard>
                        <ModalDialog
                            v-model:show="productInfoShow"
                            size="3xl"
                            class="dark-mode-text">
                            <template #dialog-title>
                                <b class="tw-text-2xl"
                                    >Detalle del producto
                                    {{
                                        detailSelectedProduct?.product
                                            .product_name +
                                        ' ' +
                                        detailSelectedProduct?.variant
                                            .variant_name
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
                                        ) in detailSelectedProduct?.variant"
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
                                                    >{{
                                                        keyNaturalName(k)
                                                    }}:</span
                                                >
                                                <span
                                                    v-if="k == 'price'"
                                                    class="col-4">
                                                    {{
                                                        Number(d).toFixed(2)
                                                    }}</span
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
                                                    detailSelectedProduct
                                                        ?.product.brand_name
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
                                                    detailSelectedProduct
                                                        ?.product
                                                        .short_description
                                                }}
                                            </p>
                                        </div>
                                    </div>
                                </div>

                                <LoadingBar
                                    v-show="loadingProps"
                                    class="tw-mt-5" />
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
                            id="purchase-modal"
                            v-model:show="showConfirmChange"
                            title="Confirmar cambio de inventario"
                            ok-text="Confirmar"
                            size="2xl"
                            @ok="updateCambioStatus()"
                            button-type="ok-cancel">
                            <h1
                                class="tw-text-3xl tw-text-black dark:tw-text-white">
                                ¿Quiere
                                <span v-if="isConfirmarModal"> confirmar </span>
                                <span v-else> rechazar </span>
                                el cambio de inventario?
                            </h1>

                            <div v-if="!isConfirmarModal" clas="row">
                                <h1
                                    class="tw-text-lg my-3 tw-font-light tw-text-black dark:tw-text-white">
                                    Debe ingrese la razón para rechazar el
                                    cambio
                                </h1>

                                <TextArea
                                    v-model="aceptedCommentString"
                                    trim
                                    class="col-12"
                                    placeholder="Ingrese la razón"
                                    resize="vertical"
                                    :color="
                                        aceptedCommentString.length > 150
                                            ? 'danger'
                                            : 'auto'
                                    " />
                                <p class="dark-mode-text">
                                    Caracteres:
                                    <span
                                        :class="{
                                            'tw-text-red-600':
                                                aceptedCommentString.length >
                                                150
                                                    ? 'tw-text-red-600'
                                                    : undefined,
                                        }">
                                        {{
                                            aceptedCommentString
                                                ? aceptedCommentString.length
                                                : 0
                                        }}
                                    </span>
                                    (Máximo de caracteres: 150)
                                </p>
                            </div>

                            <h2
                                class="tw-text-xl tw-text-black dark:tw-text-white"
                                v-if="isConfirmarModal">
                                Se
                                <span v-if="isPreviousStockLower()">
                                    sumará
                                </span>
                                <span v-else> restará </span>

                                {{
                                    Math.abs(
                                        (selectedTomaDetail?.previous_stock
                                            ? selectedTomaDetail?.previous_stock
                                            : 0) -
                                            (selectedTomaDetail?.new_stock
                                                ? selectedTomaDetail?.new_stock
                                                : 0)
                                    )
                                }}

                                al stock de bodega.
                            </h2>
                            <h2 v-else class="mt-2">
                                <span class="tw-font-bold">Importante:</span> No
                                se afectará el stock en el inventario
                            </h2>
                        </ModalDialog>

                        <div
                            class="row align-middle d-flex justify-content-center tw-mt-2">
                            <div class="col-7">
                                <h1 class="tw-text-xl tw-font-bold">
                                    Lista de observaciones de Inventario
                                </h1>
                            </div>

                            <ListBox
                                class="col-4"
                                top-label="Búsqueda por estado de obsevación"
                                v-model="searchForm.acepted"
                                placeholder="Estado de observación"
                                label="display"
                                :options="formOptions"
                                @change="onSelectedStatusChange" />
                        </div>
                        <div class="row">
                            <WaitOverlay
                                :show="loadingState.waitData"
                                class="dark-mode-text">
                                <b-pagination
                                    v-model="serverOpts.page"
                                    :total-rows="tomasTotal"
                                    :per-page="serverOpts.rowsPerPage"
                                    align="center"
                                    :limit="10"
                                    hide-goto-end-buttons
                                    class="paginator">
                                </b-pagination>

                                <template
                                    v-for="(toma, ix) of tomaDetailsArray"
                                    :key="ix">
                                    <div
                                        class="row tw-ring-2 dark:tw-ring-white py-2 tw-ring-black mb-3 pt-3 tw-capitalize">
                                        <div class="row col-12">
                                            <BBadge
                                                v-if="
                                                    toma.acepted == ACEPTED.name
                                                "
                                                class="tw-text-lg mx-2 col-5"
                                                variant="success">
                                                {{ 'Aceptado' }}
                                            </BBadge>
                                            <BBadge
                                                v-if="
                                                    toma.acepted ==
                                                    NOT_ACEPTED.name
                                                "
                                                class="tw-text-lg mx-2 col-5"
                                                variant="danger">
                                                {{ 'No aceptado' }}
                                            </BBadge>
                                            <BBadge
                                                v-if="
                                                    toma.acepted ==
                                                    PENDING_APPROVAL.name
                                                "
                                                class="tw-text-lg mx-2 col-5"
                                                variant="warning">
                                                {{ 'Revisión Pendiente' }}
                                            </BBadge>
                                            <h2
                                                class="dark-mode-text tw-text-xl col-6">
                                                Produto:
                                                <b>
                                                    {{
                                                        toma.product
                                                            .product_name +
                                                        ' / ' +
                                                        toma.variant
                                                            .variant_name
                                                    }}
                                                </b>
                                            </h2>
                                        </div>
                                        <div
                                            class="row mb-2 allign-content-end mt-2">
                                            <div class="col-3 tw-text-md">
                                                <b
                                                    >Stock en el momento de la
                                                    toma:
                                                </b>
                                            </div>
                                            <div class="col-3 tw-font-bold">
                                                <b>
                                                    {{ toma.previous_stock }}
                                                </b>
                                            </div>
                                            <div class="col-3 tw-text-md">
                                                <b
                                                    >Stock revisado en la toma:
                                                </b>
                                            </div>
                                            <div class="col-3 tw-font-bold">
                                                <b>
                                                    {{ toma.new_stock }}
                                                </b>
                                            </div>
                                        </div>
                                        <div
                                            class="row mb-2 allign-content-end mt-2">
                                            <div class="col-3 tw-text-md">
                                                <b> Stock actual en bodega: </b>
                                            </div>
                                            <div class="col-3 tw-font-bold">
                                                <b>
                                                    {{ toma.warehouse_stock }}
                                                </b>
                                            </div>
                                            <div class="col-3 tw-text-md">
                                                <b>Código(Sku): </b>
                                            </div>
                                            <div class="col-3 tw-font-light">
                                                <b>
                                                    {{ toma.variant.sku }}
                                                </b>
                                            </div>
                                        </div>
                                        <div
                                            class="row mb-2 allign-content-end mt-2">
                                            <div class="col-3 tw-text-md">
                                                <b>Razón / Comentario: </b>
                                            </div>
                                            <div
                                                class="col-8 tw-font-light text-break text-wrap">
                                                <b>
                                                    {{ toma.novedad }}
                                                </b>
                                            </div>
                                        </div>
                                        <div
                                            class="row mb-2 allign-content-end mt-2">
                                            <div class="col-3">
                                                <e-button
                                                    variant="primary"
                                                    type="button"
                                                    @click.left="
                                                        showProduct(toma)
                                                    ">
                                                    Ver Detalles Del Producto
                                                </e-button>
                                            </div>
                                            <div
                                                class="col-9 tw-font-light"
                                                v-if="toma.acepted == 'PA'">
                                                <e-button
                                                    class="col-5 mx-1"
                                                    variant="primary"
                                                    type="button"
                                                    @click.left="
                                                        onSelectedTomaDetailPressed(
                                                            toma,
                                                            'AP'
                                                        )
                                                    ">
                                                    Aceptar cambio de inventario
                                                </e-button>
                                                <e-button
                                                    class="col-5 tw-font-light"
                                                    variant="cancel"
                                                    type="button"
                                                    @click.left="
                                                        () => {
                                                            onSelectedTomaDetailPressed(
                                                                toma,
                                                                'NA'
                                                            )
                                                        }
                                                    ">
                                                    Rechazar cambio de
                                                    inventario
                                                </e-button>
                                            </div>
                                        </div>
                                    </div>
                                </template>
                            </WaitOverlay>
                        </div>
                    </ECard>
                    <div class="tw-overflow-x-auto"></div>
                </div>
            </div>
        </ECard>
    </WaitOverlay>
</template>

<style lang="scss">
    warning-text {
    }

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
