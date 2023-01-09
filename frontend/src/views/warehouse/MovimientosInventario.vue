<script setup lang="ts">
    import { useItemStore } from '@store'
    import { useMovementStore } from '@store/movement'
    import { type Warehouse, isMessage } from '@store/types'
    import type {
        Movement,
        MovementDetail,
        MovementQuery,
        MovementStatus,
        PaginatedResponse,
        ProductProps,
        ProductVariant,
        SimpleProduct,
    } from '@store/types'
    import { useWarehouseStore } from '@store/warehouse'
    import Datepicker from '@vuepic/vue-datepicker'
    import type {
        BBadge,
        BTable,
        ColorVariant,
        TableField,
    } from 'bootstrap-vue-3'
    import moment from 'moment'
    import { Form as ValidationForm, useField } from 'vee-validate'
    import * as yup from 'yup'

    import { ref, watch } from 'vue'
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

    moment.updateLocale('es', {
        weekdays: 'Domingo_Lunes_Martes_Miércoles_Jueves_Viernes_Sábado'.split(
            '_'
        ),
    })

    const itemStore = useItemStore()

    type FullMovement = Movement & {
        details: MovementDetail[]
        status_list?: MovementStatus[]
    }

    const movement = useMovementStore()

    const toast = useToast()
    const warehouse = useWarehouseStore()

    const showWaitOverlay = ref(true)

    const stopWatcher = ref(false)

    const searchString = ref('')

    const selectedMovement = ref<FullMovement>()
    const paginatedMovementDetails = ref<MovementDetail[]>()

    const currentDetailPage = ref<number>(1)

    const movementPerPage = ref<number>(25)
    const currentMainPage = ref<number>(1)
    const mainDataArr = ref<Movement[]>()
    const mainDataTotalRows = ref<number>(0)

    const selectedStatus = ref<{ name: string; display: string }>()
    const showSpecificMovement = ref<boolean>(false)

    const productInfoShow = ref<boolean>(false)
    const showStatus = ref<boolean>(false)

    type SelectedItem = {
        product: SimpleProduct
        variant: ProductVariant
        props: ProductProps[]
    }
    const detailSelectedProduct = ref<SelectedItem>()
    const loadingProps = ref<boolean>(false)

    const movementsFields: TableField[] = [
        '#',
        'FechaCreación',
        'RealizadaPor',
        'BodegaOrigen',
        'BodegaDestino',
        'Estado',
        'Notas',
        'Acciones',
    ]

    const detailsFields: TableField[] = [
        '#',
        'Código(SKU)',
        'Nombre',
        'Marca',
        'PrecioDeVenta',
        'Cantidad',
        'Acciones',
    ]

    const movementForm = ref({
        from_date: useField(
            'to_date',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr, orig) => (orig === '' ? null : curr))
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
        created_by_name: useField(
            'created_by_name',
            yup.string().optional().nullable(true)
        ),
        notes: useField('notes', yup.string().optional().nullable(true)),
    })

    const selectedWarehouseDestiny = ref<Warehouse>()
    const selectedWarehouseOrigin = ref<Warehouse>()

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

    async function onDetallesClicked(movement_id: number): Promise<void> {
        showWaitOverlay.value = true
        selectedMovement.value = undefined
        movement
            .fetchMovementInformation({ id: movement_id })
            .then(it => {
                if (isMessage(it)) {
                    toast.error('Erro de carga de detalles', { timeout: 2500 })
                    showWaitOverlay.value = false
                    return
                }

                selectedMovement.value = it[0]
                paginatedMovementDetails.value = selectedMovement.value.details
                showSpecificMovement.value = true
                showWaitOverlay.value = false
                filterData()
                movement
                    .fetchMovementStatus({
                        transaction_id: selectedMovement.value.id,
                    })
                    .then(it => {
                        if (isMessage(it)) {
                            toast.error('Erro de carga de detalles', {
                                timeout: 2500,
                            })
                            showWaitOverlay.value = false
                            return
                        }
                        if (selectedMovement.value) {
                            selectedMovement.value.status_list = it
                        }
                    })
                    .catch(() => {
                        toast.error('Error al cargar estados del movimiento', {
                            timeout: 2500,
                        })
                    })
            })
            .catch(() => {
                toast.error('Error de carga de detalles(servidor)', {
                    timeout: 2500,
                })
                showWaitOverlay.value = false
            })
    }

    function onReset(): void {
        movementForm.value.from_date.resetField()
        movementForm.value.to_date.resetField()
        movementForm.value.created_by_name.resetField()
        movementForm.value.notes.resetField()
        movementForm.value.status_from_date.resetField()
        movementForm.value.status_to_date.resetField()
        selectedWarehouseDestiny.value = undefined
        selectedWarehouseOrigin.value = undefined
        selectedStatus.value = undefined
    }

    async function onBuscarClick(): Promise<void> {
        showWaitOverlay.value = true
        stopWatcher.value = true

        const query: MovementQuery = {}
        const f = movementForm.value

        if (
            f.from_date.errorMessage ||
            f.to_date.errorMessage ||
            f.created_by_name.errorMessage ||
            f.notes.errorMessage ||
            f.status_from_date.errorMessage ||
            f.status_to_date.errorMessage
        ) {
            toast.error('Verifique los datos antes buscar')
            showWaitOverlay.value = false
            return
        }
        if (
            selectedWarehouseOrigin.value &&
            selectedWarehouseDestiny.value &&
            selectedWarehouseOrigin.value?.id ==
                selectedWarehouseDestiny.value?.id
        ) {
            toast.error('Bodega origen y destino no pueden ser iguales', {
                timeout: 4500,
            })
            return
        }
        query.from_date = f.from_date.value
        query.to_date = f.to_date.value
        query.created_by_name = f.created_by_name.value
        query.notes = f.notes.value
        query.warehouse_origin = selectedWarehouseOrigin.value?.id
        query.warehouse_destiny = selectedWarehouseDestiny.value?.id
        query.status = selectedStatus.value?.name
        query.status_from_date = f.status_from_date.value
        query.status_to_date = f.status_to_date.value
        movement
            .fetchPaginatedMovement(query, {
                page: 1,
                per_page: movementPerPage.value,
            })
            .then(it => {
                if (isMessage(it)) {
                    return
                }
                if (it.data.length == 0) {
                    toast.error('No se ha encontrado registros')
                    return
                }
                mainDataArr.value = it.data
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
                currentMainPage.value = 1
                showWaitOverlay.value = false
                stopWatcher.value = false
            })
    }

    async function showProduct(picked: MovementDetail): Promise<void> {
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

    function filterData(): void {
        stopWatcher.value = true
        if (searchString.value.length > 0 && selectedMovement.value?.details) {
            currentDetailPage.value = 1
            paginatedMovementDetails.value = selectedMovement.value?.details
                .filter(d => {
                    return (
                        d.product.product_name.includes(searchString.value) ||
                        d.variant.variant_name.includes(searchString.value) ||
                        d.variant.sku.includes(searchString.value)
                    )
                })
                .slice(
                    (currentDetailPage.value - 1) * movementPerPage.value,
                    currentDetailPage.value * movementPerPage.value
                )
            stopWatcher.value = false
        } else {
            paginatedMovementDetails.value =
                selectedMovement.value?.details.slice(
                    (currentDetailPage.value - 1) * movementPerPage.value,
                    currentDetailPage.value * movementPerPage.value
                )
            stopWatcher.value = false
        }
    }

    const loadMovements = async (): Promise<void> => {
        if (!stopWatcher.value) {
            showWaitOverlay.value = true

            warehouse
                .fetchPaginatedWarehouseMovements(
                    {},
                    {
                        page: currentMainPage.value,
                        per_page: movementPerPage.value,
                    }
                )
                .then((res): void => {
                    if (isMessage(res)) {
                        toast.error(res.message)
                        return
                    }
                    res = res as PaginatedResponse<Movement>

                    mainDataArr.value = res.data
                    mainDataTotalRows.value = res.total
                    showWaitOverlay.value = false
                })
                .catch((): void => {
                    toast.error(
                        'Error al cargar movimientos, intentelo más tarde',
                        { timeout: 5000 }
                    )
                    showWaitOverlay.value = false
                })
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

    function statusMovementColor(status?: string): ColorVariant {
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

    warehouse
        .fetchPaginatedWarehouseMovements({}, { page: 1, per_page: 25 })
        .then((res): void => {
            if (isMessage(res)) {
                toast.error(res.message)
                return
            }
            res = res as PaginatedResponse<Movement>

            mainDataArr.value = res.data
            mainDataTotalRows.value = res.total
            showWaitOverlay.value = false
        })
        .catch((): void => {
            toast.error('Error al cargar movimientos, intentelo más tarde', {
                timeout: 5000,
            })
            showWaitOverlay.value = false
        })
    warehouse.fetchWarehouses()

    watch(currentMainPage, loadMovements)
    watch(currentDetailPage, filterData)
    watch(searchString, filterData)
</script>

<template>
    <WaitOverlay :show="showWaitOverlay">
        <ECard>
            <div class="container" v-if="!showSpecificMovement">
                <div class="row mt-3">
                    <h1 class="title tw-font-bold mt-2 col-4 my-3">
                        Lista de todos los Movimientos
                    </h1>
                    <b-collapse
                        id="collapse-1"
                        class="mt-2 inline-flex tw-rounded tw-ring-1 dark-mode-text tw-ring-yellow-400 tw-py-2">
                        <h2
                            class="tw-text-3xl dark-mode-text tw-font-bold mx-3 my-2">
                            Búsqueda de pedidos
                        </h2>
                        <ECard>
                            <ValidationForm
                                @submit="onBuscarClick"
                                :validation-schema="movementForm">
                                <div class="row" align-v="start">
                                    <div class="row">
                                        <ListBox
                                            class="col-4"
                                            top-label="Bodega Orgigen"
                                            v-model="selectedWarehouseOrigin"
                                            placeholder="Filtro por bodega origen"
                                            label="name"
                                            :options="
                                                warehouse.getWarehouseList ?? []
                                            " />

                                        <ListBox
                                            class="col-4"
                                            top-label="Bodega Destino"
                                            v-model="selectedWarehouseDestiny"
                                            placeholder="Filtro por bodega destino"
                                            label="name"
                                            :options="
                                                warehouse.getWarehouseList ?? []
                                            " />
                                        <div
                                            class="col-3 col-lg-4 col-xl-4 col-sm-6 mt-auto">
                                            <InputText
                                                v-model="
                                                    movementForm.created_by_name
                                                        .value
                                                "
                                                :info-label="
                                                    movementForm.created_by_name
                                                        .errorMessage
                                                "
                                                :status="
                                                    Boolean(
                                                        movementForm
                                                            .created_by_name
                                                            .errorMessage
                                                    )
                                                "
                                                info-status="danger"
                                                label="Nombre del empleado que solicitó el movimiento" />
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-lg-4 col-xl-4 col-sm-6">
                                            <Datepicker
                                                v-model="
                                                    movementForm.from_date.value
                                                "
                                                :max-date="
                                                    movementForm.to_date?.value
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
                                                        label="Fecha Mínima De Creación"
                                                        :model-value="value"
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

                                        <div class="col-lg-4 col-xl-4 col-sm-6">
                                            <Datepicker
                                                v-model="
                                                    movementForm.to_date.value
                                                "
                                                :min-date="
                                                    movementForm.from_date
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
                                                        label="Fecha Máxima De Creación"
                                                        :model-value="value"
                                                        :info-label="
                                                            movementForm.to_date
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
                                    </div>
                                    <div class="row">
                                        <ListBox
                                            class="col-4"
                                            top-label="Último Estado"
                                            v-model="selectedStatus"
                                            placeholder="Filtro por estado de la compra"
                                            label="display"
                                            :options="
                                                movement.getPurchaseStatus()
                                            " />

                                        <div
                                            class="col-4 col-lg-4 col-xl-4 col-sm-6">
                                            <Datepicker
                                                v-model="
                                                    movementForm
                                                        .status_from_date.value
                                                "
                                                :max-date="
                                                    movementForm.status_to_date
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
                                                            movementForm
                                                                .status_from_date
                                                                .errorMessage
                                                        "
                                                        :status="
                                                            Boolean(
                                                                movementForm
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
                                                    movementForm.status_to_date
                                                        .value
                                                "
                                                :min-date="
                                                    movementForm
                                                        .status_from_date?.value
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
                                                            movementForm
                                                                .status_to_date
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
                                                @click.left="onReset"
                                                type="button"
                                                variant="secondary">
                                                Limpiar Búsqueda
                                            </e-button>
                                        </div>

                                        <h2
                                            class="dark-mode-text col-6 mt-4 tw-text-lg tw-font-bold">
                                            <span
                                                class="tw-text-amber-700 dark:tw-text-amber-400">
                                                {{ mainDataArr?.length }}
                                            </span>
                                            Registros encontrados
                                        </h2>
                                    </div>
                                </div>
                            </ValidationForm>
                        </ECard>
                    </b-collapse>
                    <e-button
                        v-b-toggle.collapse-1
                        type="button"
                        variant="primary"
                        class="col-6 mx-1 my-3 col-lg-2 col-xl-2 col-md-3 col-sm-4"
                        >Desplegar Búsqueda
                    </e-button>
                    <BTable
                        outline
                        :fields="movementsFields"
                        :items="mainDataArr">
                        <template #cell(#)="{ index }">
                            {{
                                index +
                                1 +
                                (currentMainPage - 1) * movementPerPage
                            }}
                        </template>

                        <template #cell(FechaCreación)="{ item }">
                            {{
                                moment(item.created_at).format(
                                    'dddd DD/MM/yyyy HH:mm:ss'
                                )
                            }}
                        </template>
                        <template #cell(RealizadaPor)="{ item }">
                            {{
                                item.created_by.name +
                                ' ' +
                                item.created_by.lastname
                            }}
                        </template>
                        <template #cell(BodegaOrigen)="{ item }">
                            {{ item.warehouse_origin.name }}
                        </template>
                        <template #cell(BodegaDestino)="{ item }">
                            {{ item.warehouse_destiny.name }}
                        </template>
                        <template #cell(Notas)="{ item }">
                            {{ truncate(item.notes, 25, '...') }}
                        </template>
                        <template #cell(Estado)="{ item }">
                            <BBadge
                                class="tw-text-md tw-capitalize"
                                :variant="statusMovementColor(item.status)">
                                {{ item.status }}
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
                        v-model="currentMainPage"
                        :total-rows="mainDataTotalRows"
                        :per-page="movementPerPage"
                        align="center"
                        :limit="10"
                        hide-goto-end-buttons
                        class="paginator"></b-pagination>
                </div>
            </div>
            <div class="container" v-else>
                <div class="row">
                    <h1 class="title my-2 tw-text-3xl col-9 dark-mode-text">
                        Información y Lista de productos del movimiento #{{
                            selectedMovement?.id
                        }}
                    </h1>
                    <e-button
                        variant="primary"
                        type="button"
                        class="col-3 my-3"
                        @click.left="showSpecificMovement = false">
                        Regresar a todas los movimientos
                    </e-button>
                </div>
                <div class="row my-2">
                    <div
                        class="tw-rounded tw-ring-2 my-2 tw-ring-yellow-400 tw-py-1 col-12 dark-mode-text tw-text-lg">
                        <div class="row">
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3 tw-font-bold">
                                Bodega Orgien:
                            </span>
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3"
                                >{{
                                    selectedMovement?.warehouse_origin.name
                                }}</span
                            >
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3 tw-font-bold">
                                Bodega Destino:
                            </span>
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3"
                                >{{
                                    selectedMovement?.warehouse_destiny.name
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
                                    truncate(
                                        selectedMovement?.notes + '',
                                        250,
                                        '...'
                                    )
                                }}</span
                            >
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3 tw-font-bold">
                                Orden revisada por:
                            </span>
                            <span
                                class="col-sm-12 col-12 col-md-6 col-xl-3 col-lg-3"
                                >{{
                                    selectedMovement?.created_by?.name +
                                    ' ' +
                                    selectedMovement?.created_by?.lastname
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
                    v-model:show="showStatus"
                    size="3xl"
                    class="dark-mode-text">
                    <div class="container">
                        <div
                            class="row mb-2 tw-ring-2 dark:tw-ring-white py-2 tw-ring-black">
                            <div class="row mb-2">
                                <div class="col-6 tw-text-md">
                                    <b>Fecha de creación: </b>
                                </div>
                                <div class="col-6 tw-font-light">
                                    <b>
                                        {{
                                            moment(
                                                selectedMovement?.created_at
                                            ).format('dddd DD/MM/yyyy HH:mm:ss')
                                        }}
                                    </b>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="row tw-text-lg tw-font-bold mb-3">
                        Estados del movimiento de bodega:
                    </div>

                    <template
                        v-for="(status, ix) in selectedMovement?.status_list"
                        :key="ix">
                        <div
                            class="row tw-ring-2 dark:tw-ring-white py-2 tw-ring-black mb-3 pt-3 tw-capitalize">
                            <div class="row col-12">
                                <BBadge
                                    class="tw-text-lg mx-2 col-5"
                                    :variant="
                                        statusMovementColor(status.status)
                                    ">
                                    {{
                                        '( ' + (ix + 1) + ' ) ' + status.status
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
                        @click="showStatus = true">
                        Ver estados del movimiento
                    </e-button>
                </div>
                <div class="row">
                    <BTable
                        :fields="detailsFields"
                        outline
                        class="tw-capitalize dark-mode-text"
                        :items="paginatedMovementDetails ?? []">
                        <template #cell(#)="{ index }">
                            {{
                                index +
                                1 +
                                (currentDetailPage - 1) * movementPerPage
                            }}
                        </template>
                        <template #cell(Código(SKU))="{ item }">
                            {{ item.variant.sku }}
                        </template>
                        <template #cell(Nombre)="{ item }">
                            {{
                                item.product.product_name +
                                ' ' +
                                item.variant.variant_name
                            }}
                        </template>
                        <template #cell(Marca)="{ item }">
                            {{ item.product.brand_name }}
                        </template>
                        <template #cell(PrecioDeVenta)="{ item }">
                            {{ Number(item.variant.price).toFixed(2) }}
                        </template>
                        <template #cell(Cantidad)="{ item }">
                            {{ item.quantity }}
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
                        v-model="currentDetailPage"
                        :total-rows="selectedMovement?.details.length"
                        :per-page="movementPerPage"
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
