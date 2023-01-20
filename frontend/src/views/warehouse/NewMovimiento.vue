<script setup lang="ts">
    import { useMovementStore } from '@store/movement'
    import { useProductStore } from '@store/product'
    import {
        type Item,
        type MessageResponse,
        type MovementDetail,
        type MovementSaveData,
        type ProductProps,
        type Warehouse,
        type WarehouseStock,
        isMessage,
    } from '@store/types'
    import {
        type FullStockWithCompromised,
        useWarehouseStore,
    } from '@store/warehouse'
    import type { TableField } from 'bootstrap-vue-3'
    import { Form as ValidationForm, useField } from 'vee-validate'
    import * as yup from 'yup'

    import { computed, watch } from 'vue'
    import type { ServerOptions } from 'vue3-easy-data-table'
    import { useToast } from 'vue-toastification'

    import {
        EButton,
        ECard,
        ECol,
        ERow,
        InputText,
        ListBox,
        ModalDialog,
        TextArea,
        Title,
        WaitOverlay,
    } from '@custom-components'

    /**
     * Utility object definitions
     */
    const productStore = useProductStore()
    const toast = useToast()

    /**
     * View Holders
     */
    const warehouse = useWarehouseStore()
    const movement = useMovementStore()
    const showWaitOverlay = ref<boolean>(true)
    const productModalShow = ref<boolean>(false)
    const itemInfoShow = ref<boolean>(false)
    const serverOpts = ref<ServerOptions>({
        page: 1,
        rowsPerPage: 10,
    })
    const itemLoading = ref(false)
    const paginationOptions = computed<PaginationOptions>(() => ({
        page: serverOpts.value.page,
        per_page: serverOpts.value.rowsPerPage,
    }))

    const detailSelectedProduct = ref<FullStockWithCompromised>()

    const pickedProduct = ref<FullStockWithCompromised>()

    const productStock = ref<WarehouseStock[]>([])

    const productPageLength = ref<number>(0)

    /**
     * Definition of page-used form
     */

    type DisplayedItem = FullStockWithCompromised & { quantity: number }
    type Form = {
        warehouse_origin?: Warehouse
        warehouse_destiny?: Warehouse
        notes: string
        items: DisplayedItem[]
    }
    type ItemForm = {
        item: Item | null
        quantity: any
    }

    type LoadedStock = ServerOptions & {
        warehouse_id: number
        stock: FullStockWithCompromised[]
    }

    const loadedProducts = ref<LoadedStock[]>([])

    const selectedProxyWh = ref<Warehouse>()

    const productFields: TableField[] = [
        '#',
        'Código',
        'NombreProducto',
        'Marca',
        { label: 'Stock', key: 'stock_level' },
        'StockComprometido',
        'Detalles',
    ]

    const formFields: TableField[] = [
        '#',
        'Código',
        'NombreProducto',
        'Marca',
        { label: 'Stock En Bodega', key: 'stock_level' },
        { label: 'Stock A Mover', key: 'quantity' },
        { label: 'StockComprometido', key: 'compromised_stock' },
        'Detalles',
        'Acciones',
    ]

    const form = ref<Form>({
        warehouse_origin: undefined,
        warehouse_destiny: undefined,
        notes: '',
        items: [],
    })

    const showChangeWhModal = ref<boolean>(false)

    const showGuardarModal = ref<boolean>(false)

    let stopWatcher = false

    const itemForm = ref<ItemForm>({
        item: null,
        quantity: useField(
            'new_stock',
            yup
                .number()
                .min(0, 'Tiene que ser mayor a 0')
                .transform((curr: any, orig: any): any =>
                    orig === '' ? undefined : curr
                )
                .required('Ingrese el número de productos a mover')
                .typeError('Ingrese un número entero positivo')
        ),
    })
    const quantity_message = ref<string>()
    const quantityRangeError = (): void => {
        const f = itemForm.value
        if (f.quantity.value != '' && pickedProduct.value) {
            if (
                Number(f.quantity.value) >
                pickedProduct.value.stock_level -
                    (pickedProduct.value.compromised_stock
                        ? pickedProduct.value.compromised_stock
                        : 0)
            ) {
                quantity_message.value = `Stock a mover tiene que ser menor a ${
                    pickedProduct.value.stock_level -
                    (pickedProduct.value.compromised_stock
                        ? pickedProduct.value.compromised_stock
                        : 0)
                }`
                return
            }
        }
        quantity_message.value = f.quantity.errorMessage
    }
    warehouse.fetchWarehouses().then(() => {
        showWaitOverlay.value = false
    })

    const iformShow = computed(() => ({
        nombre: pickedProduct.value
            ? pickedProduct.value?.product.product_name +
              ' - ' +
              pickedProduct.value?.variant.variant_name
            : '',
        detalle: pickedProduct.value?.product.summary,
        props: pickedProduct.value?.props
            .map((it: ProductProps) => it.name + ' : ' + it.value)
            .join(',  '),
        variante: pickedProduct.value?.variant,
        marca: pickedProduct.value?.product.brand_name,
    }))

    const loadItems = async () => {
        itemLoading.value = true

        const loadedIdx: number = loadedProducts.value.findIndex(p => {
            itemLoading.value = false
            return (
                p.page == serverOpts.value.page &&
                p.rowsPerPage == serverOpts.value.rowsPerPage &&
                p.warehouse_id == form.value.warehouse_origin?.id
            )
        })
        if (loadedIdx >= 0) {
            itemLoading.value = false
            productStock.value = loadedProducts.value[loadedIdx].stock
            return
        }

        const res = await warehouse.fetchFullStockWithCompromised(
            { warehouse_id: form.value.warehouse_origin?.id },
            paginationOptions.value
        )
        itemLoading.value = false
        if (isMessage(res)) {
            toast.error('Error de carga de stock')
            itemLoading.value = false
            return
        }

        productPageLength.value = res.total
        productStock.value = res.data
        const whid = form.value.warehouse_origin?.id
            ? form.value.warehouse_origin.id
            : 0
        loadedProducts.value.push({
            ...serverOpts.value,
            warehouse_id: whid,
            stock: res.data,
        })
    }

    /**
     * Event definitions
     */
    function removeItem(index: number) {
        form.value.items.splice(index, 1)
    }
    function onShowModalClick() {
        productModalShow.value = true
    }

    async function onRowClick(selectedItem: FullStockWithCompromised) {
        pickedProduct.value = selectedItem
        productModalShow.value = false
    }

    function addToTable() {
        const targetProduct = pickedProduct.value
        if (!targetProduct) {
            toast.error('Seleccione un producto para añadirlo a la tabla')
            return
        }
        if (
            form.value.items.findIndex(
                it => targetProduct.variant.id == it.variant.id
            ) >= 0
        ) {
            toast.warning('El producto ya está añadido')
            return
        }
        form.value.items.push({
            product: targetProduct.product,
            variant: targetProduct.variant,
            quantity: Number(itemForm.value.quantity.value),
            props: targetProduct.props,
            stock_level: targetProduct.stock_level,
        } as DisplayedItem)

        itemForm.value.item = null
        itemForm.value.quantity.resetField()

        pickedProduct.value = undefined
        toast.success('Producto añadido a la tabla')
    }

    function changeModalManager() {
        if (stopWatcher) {
            stopWatcher = false
            return
        }

        if (form.value.warehouse_origin) {
            showChangeWhModal.value = true
        } else {
            form.value.warehouse_origin = selectedProxyWh.value
            loadItems()
        }
    }
    function cancelarCambio() {
        stopWatcher = true
        selectedProxyWh.value = form.value.warehouse_origin
    }
    function confirmarCambio() {
        form.value.warehouse_origin = selectedProxyWh.value
        detailSelectedProduct.value = undefined
        pickedProduct.value = undefined
        form.value.items = []
        showChangeWhModal.value = false
        loadItems()
        toast.success('Cambio realizado')
    }

    function saveMovement() {
        const { value: data } = form
        if (
            data.warehouse_origin?.id == null ||
            data.warehouse_destiny?.id == null ||
            data.items.length == 0
        ) {
            toast.error(
                data.items.length == 0
                    ? 'No hay productos en la tabla para guardar'
                    : 'Seleccione las bodegas para continuar'
            )
            return
        }
        const saveData: MovementSaveData = {
            warehouse_origin: data.warehouse_origin.id,
            warehouse_destiny: data.warehouse_destiny.id,
            notes: data.notes,
            details: data.items.map(it => ({
                product: it.product,
                variant: it.variant,
                quantity: it.quantity,
            })),
        }
        showWaitOverlay.value = true
        movement
            .saveMovement(saveData)
            .then(() => {
                toast.success('Order registrada correctamente')
                data.notes = ''
                data.warehouse_destiny = undefined
                data.warehouse_origin = undefined
                data.items.splice(0, data.items.length)
                selectedProxyWh.value = undefined
                loadedProducts.value = []
            })
            .catch((it: MessageResponse) => {
                toast.error(`No se pudo guardar la orden [${it.code}]`)
            })
            .finally(() => {
                showWaitOverlay.value = false
            })
        return
    }

    function onGuardarClicked() {
        showGuardarModal.value = true
    }

    async function showItem(item: FullStockWithCompromised) {
        detailSelectedProduct.value = item
        itemInfoShow.value = true
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

    watch(serverOpts.value, loadItems)
    watch(selectedProxyWh, changeModalManager)
    watch(pickedProduct, quantityRangeError)
</script>

<template>
    <main>
        <WaitOverlay :show="showWaitOverlay">
            <ModalDialog
                id="product-modal"
                class="dark-mode-text tw-min-h-[70%] tw-font-bold"
                v-model:show="productModalShow"
                size="full"
                title="Haga Click en el producto para seleccionar">
                <WaitOverlay :show="itemLoading">
                    <div class="tw-container tw-flex mb-3">
                        <b-pagination
                            v-model="serverOpts.page"
                            :total-rows="productPageLength"
                            :per-page="serverOpts.rowsPerPage"
                            align="center"
                            :limit="10"
                            hide-goto-end-buttons
                            class="paginator">
                        </b-pagination>
                        <!--  TODO Fix reload table after row size change
                    <label class="form-label">
                        Productos Por Página:
                    </label>
                    <b-form-select
                    v-model="serverOpts.rowsPerPage"
                    class=" tw-w-1/12 mx-2"
                    :options="[5,10,15]"
                    placeholder="Productos por página"
                    /> -->
                    </div>

                    <div class="row" style="height: 450px">
                        <BTable
                            :fields="productFields"
                            :items="productStock"
                            outline
                            hover
                            selectable
                            @row-selected="onRowClick">
                            <template #cell(selected)="{}"> </template>
                            <template #cell(#)="{ index }">
                                {{
                                    index +
                                    1 +
                                    (serverOpts.page - 1) *
                                        serverOpts.rowsPerPage
                                }}
                            </template>
                            <template #cell(Código)="{ item }">
                                {{ item.variant.sku }}
                            </template>
                            <template #cell(Marca)="{ item }">
                                {{ item.product.brand_name }}
                            </template>
                            <template #cell(NombreProducto)="{ item }">
                                {{
                                    item.product.product_name +
                                    ' - ' +
                                    item.variant.variant_name
                                }}
                            </template>
                            <template #cell(Detalles)="{ item }">
                                {{
                                    item.props
                                        .map(
                                            (it: ProductProps) =>
                                                it.name + ' : ' + it.value
                                        )
                                        .join(',  ')
                                }}
                            </template>
                            <template #cell(StockComprometido)="{ item }">
                                {{
                                    item.compromised_stock
                                        ? item.compromised_stock
                                        : 0
                                }}
                            </template>
                        </BTable>
                    </div>
                </WaitOverlay>
            </ModalDialog>
            <ModalDialog
                v-model:show="itemInfoShow"
                size="3xl"
                ok-text="Cerrar"
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
                                    <span v-else class="col-4">{{ d }}</span>
                                </div>
                            </div>
                        </template>

                        <div class="col-12">
                            <div class="row">
                                <span class="col-4 tw-font-bold"> Marca: </span>
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

                    <div
                        v-if="detailSelectedProduct?.props"
                        class="tw-ring-1 tw-ring-slate-500 tw-rounded tw-pb-3 row">
                        <h3 class="col-12 tw-text-xl tw-py-1.5 dark-mode-text">
                            <b>Características del Producto</b>
                        </h3>
                        <template
                            v-for="(param, idx) in detailSelectedProduct?.props"
                            :key="idx">
                            <div
                                class="col-6 col-md-3 col-xl-2 tw-text-md dark-mode-text">
                                <b>{{ param.name }}:</b>
                            </div>
                            <div class="col-6 col-md-3 col-xl-2 dark-mode-text">
                                <b>{{ param.value }}</b>
                            </div>
                        </template>
                    </div>
                </div>
            </ModalDialog>
            <ECard>
                <ERow align-v="start">
                    <ECol cols="12" lg="6" xl="4">
                        <ListBox
                            v-model="selectedProxyWh"
                            top-label="Seleccione La Bodega Origen"
                            placeholder="No ha seleccionado una bodega"
                            :options="warehouse.getWarehouseList ?? []"
                            label="name" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="4">
                        <ListBox
                            v-model="form.warehouse_destiny"
                            top-label="Seleccione La Bodega Destino"
                            placeholder="No ha seleccionado una bodega"
                            :options="
                                (warehouse.getWarehouseList ?? []).filter(
                                    w => w.id != form.warehouse_origin?.id
                                )
                            "
                            label="name" />
                    </ECol>
                    <ModalDialog
                        id="change-modal"
                        v-model:show="showChangeWhModal"
                        title="Confirmar Cambio de Inventario"
                        ok-text="Cambiar"
                        @ok="confirmarCambio()"
                        @cancel="cancelarCambio()"
                        class="dark-mode-text"
                        button-type="ok-cancel">
                        <h1
                            class="tw-text-3xl tw-text-black dark:tw-text-white">
                            ¿Está seguro que quiere cambiar la bodega origen del
                            movimiento?
                        </h1>
                        <h2
                            class="tw-text-2xl tw-text-red-700 dark:tw-text-red-600">
                            Perderá la lista de productos ingresados hasta el
                            momento.
                        </h2>
                    </ModalDialog>
                    <ECol cols="12" lg="6" xl="4">
                        <div class="tw-flex tw-flex-col">
                            <label
                                class="tw-font-bold tw-text-md lg:tw-text-base tw-text-left">
                                Comentario del movimiento
                            </label>
                            <TextArea
                                v-model="form.notes"
                                placeholder="Comentario" />
                        </div>
                    </ECol>
                </ERow>

                <div class="tw-flex">
                    <div class="tw-w-[1.5rem]">&ZeroWidthSpace;</div>
                </div>

                <!-- <ERow>
                <ECol cols="12"> -->
                <ECard>
                    <EButton
                        class="tw-w-1/4"
                        :class="{
                            'tw-bg-primary/50 tw-text-secondary/60':
                                !form.warehouse_origin,
                        }"
                        @click="onShowModalClick"
                        :disabled="!form.warehouse_origin">
                        Seleccionar producto
                    </EButton>
                    <Title size="2xl"> Datos del Ítem seleccionado </Title>
                    <ERow align-v="middle">
                        <ECol cols="12" lg="6">
                            <InputText
                                label="Producto seleccionado"
                                placeholder="Seleccione un ítem"
                                :model-value="iformShow.nombre"
                                readonly />
                        </ECol>
                        <ECol cols="12" lg="6">
                            <InputText
                                label="Código de producto"
                                placeholder="Seleccione una variante para visualizar"
                                :model-value="iformShow.variante?.sku"
                                readonly />
                        </ECol>
                        <ECol cols="12" lg="8">
                            <div class="tw-flex tw-flex-col tw-h-40">
                                <label for="prod-det" class="form-label">
                                    Detalles del producto
                                </label>
                                <TextArea
                                    id="prod-det"
                                    :model-value="iformShow.detalle"
                                    readonly
                                    placeholder="Cargue un producto para ver su descripción"
                                    resize="vertical" />
                                <TextArea
                                    class="my-2"
                                    id="prod-det"
                                    :model-value="iformShow.props"
                                    readonly
                                    placeholder="Cargue un producto para ver los detalles"
                                    resize="vertical" />
                            </div>
                        </ECol>
                        <ECol cols="12" lg="3">
                            <InputText
                                label="Stock Disponible Para Mover"
                                :model-value="
                                    (
                                        (pickedProduct?.stock_level
                                            ? pickedProduct.stock_level
                                            : 0) -
                                        (pickedProduct?.compromised_stock
                                            ? pickedProduct.compromised_stock
                                            : 0)
                                    ).toString()
                                "
                                readonly />
                            <label
                                for="f-quantity"
                                class="form-label dark:tw-text-secondary-light tw-bg-primary tw-rounded-lg py-1 px-1 mb-2">
                                Cantidad de stock a mover
                            </label>
                            <InputText
                                id="f-quantity"
                                v-model="itemForm.quantity.value"
                                :info-label="quantity_message"
                                :status="Boolean(quantity_message)"
                                placeholder="Ingrese la cantidad a mover"
                                info-status="danger"
                                @input="quantityRangeError" />
                        </ECol>
                        <ECol cols="12" lg="auto" class=" ">
                            <EButton
                                class="tw-w-full lg:tw-w-auto"
                                :class="{
                                    'tw-bg-primary/50 tw-text-secondary/60':
                                        pickedProduct == undefined ||
                                        itemForm.quantity.value == undefined ||
                                        Number(itemForm.quantity.value) <= 0 ||
                                        Boolean(quantity_message),
                                }"
                                left-icon="plus"
                                :disabled="
                                    pickedProduct == undefined ||
                                    itemForm.quantity.value == undefined ||
                                    Number(itemForm.quantity.value) <= 0 ||
                                    Boolean(quantity_message)
                                "
                                @click="addToTable">
                                Añadir producto
                            </EButton>
                        </ECol>
                    </ERow>
                </ECard>
                <div class="tw-overflow-x-auto">
                    <BTable :fields="formFields" :items="form.items">
                        <template #cell(#)="{ index }">
                            {{ index + 1 }}
                        </template>
                        <template #cell(Código)="{ item }">
                            {{ item.variant.sku }}
                        </template>
                        <template #cell(Marca)="{ item }">
                            {{ item.product.brand_name }}
                        </template>
                        <template #cell(NombreProducto)="{ item }">
                            {{
                                item.product.product_name +
                                ' - ' +
                                item.variant.variant_name
                            }}
                        </template>
                        <template #cell(Detalles)="{ item }">
                            {{
                                item.props
                                    .map(
                                        (it: ProductProps) =>
                                            it.name + ' : ' + it.value
                                    )
                                    .join(',  ')
                            }}
                        </template>
                        <template #cell(Acciones)="{ item, index }">
                            <div class="t-button-group">
                                <EButton
                                    left-icon="fa-eye"
                                    @click="showItem(item)"
                                    variant="secondary">
                                    Ver detalles
                                </EButton>

                                <EButton
                                    left-icon="fa-trash-can"
                                    variant="cancel"
                                    @click="removeItem(index)">
                                    <span
                                        class="tw-invisible md:tw-visible tw-font-bold">
                                        Eliminar
                                    </span>
                                </EButton>
                            </div>
                        </template>
                    </BTable>
                </div>
                <ModalDialog
                    id="change-modal"
                    v-model:show="showGuardarModal"
                    title="Confirmar Cambio de Inventario"
                    ok-text="Guardar"
                    @ok="saveMovement()"
                    class="dark-mode-text"
                    button-type="ok-cancel">
                    <h1 class="tw-text-3xl dark-mode-text">
                        ¿Está seguro que quiere guardar el movimiento?
                    </h1>
                    <h2
                        v-if="form.notes.length <= 0"
                        class="tw-text-2xl dark-mode-text my-3">
                        Es recomendable que resgistre un comentario del
                        movimiento
                    </h2>
                </ModalDialog>
                <ERow>
                    <ECol class="tw-content-end tw-justify-end">
                        <EButton
                            left-icon="fa-floppy-disk"
                            icon-provider="awesome"
                            @click="onGuardarClicked">
                            Guardar
                        </EButton>
                    </ECol>
                </ERow>
                <!-- </ECol>
            </ERow> -->
            </ECard>
        </WaitOverlay>
    </main>
</template>
<style lang="scss">
    .dark-mode-text {
        @apply dark:tw-text-white tw-text-secondary-dark;
    }

    .table {
        > thead {
            @apply tw-bg-secondary tw-text-white tw-font-bold;
        }
        @media (prefers-color-scheme: dark) {
            color: white !important;
            --bs-table-striped-color: theme(colors.zinc.400);
            --bs-table-hover-color: theme('colors.primary.light');
            --bs-table-hover-bg: theme(colors.primary.light / 15%);
        }
    }
    .custom-data-table {
        --easy-table-header-background-color: theme(colors.secondary.DEFAULT);
        --easy-table-header-font-color: theme(colors.white);
        --easy-table-border: transparentize();
        --easy-table-footer-background-color: theme(colors.secondary.DEFAULT);
        --easy-table-footer-font-color: white;

        @media (prefers-color-scheme: dark) {
            --easy-table-body-row-background-color: theme(
                colors.secondary.light
            );
            --easy-table-body-row-font-color: white;
            --easy-table-row-border: theme(colors.secondary.DEFAULT);
        }
    }
    .t-button-group {
        max-width: fit-content !important;
        @apply tw-rounded tw-overflow-hidden tw-flex tw-place-content-stretch tw-place-items-stretch;
        > t-button,
        > button {
            border-radius: 0.3rem;
            margin-left: 0.5rem;
            min-width: auto;
            max-width: 100%;
        }
    }
    .pagination__rows-per-page {
        .select-items {
            @apply tw-z-50;
        }
    }
    .easy-data-table__rows-selector {
        @apply tw-flex tw-relative;
    }
</style>
