<script setup lang="ts">
    import { useOrderStore } from '@store/order'
    import { useProductStore } from '@store/product'
    import {
        type Item,
        type MessageResponse,
        type Warehouse,
        isMessage,
    } from '@store/types'
    import type { OrderSaveData } from '@store/types/orders.model'
    import type {
        Product,
        ProductAttribute,
        ProductVariant,
        SimpleProductStock,
    } from '@store/types/product'
    import { useWarehouseStore } from '@store/warehouse'
    import type { TableField } from 'bootstrap-vue-3'

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
    const order = useOrderStore()
    const showWaitOverlay = ref<boolean>(true)
    const productModalShow = ref<boolean>(false)
    const itemInfoShow = ref<boolean>(false)
    const serverOpts = ref<ServerOptions>({
        page: 1,
        rowsPerPage: 5,
    })
    const itemLoading = ref(false)
    const paginationOptions = computed<PaginationOptions>(() => ({
        page: serverOpts.value.page,
        per_page: serverOpts.value.rowsPerPage,
    }))

    const detailParamsDictionary: {
        [name: string]: keyof ProductVariantInformation
    } = {
        Código: 'id',
        SKU: 'sku',
        'Nombre de Variante': 'variant_name',
        'Cantidad en stock': 'stock_level',
    }

    const pickedProduct = ref<Product>()

    const productStock = ref<SimpleProductStock[]>([])

    const productPageLength = computed(() => {
        const items = productStore.products
        if (isMessage(items) || !items) return 0
        return items.total
    })
    type ProductVariantInformation = ProductVariant & {
        parent: Product
        all_attributes: ProductAttribute[]
    }
    type QuantifiedItem = ProductVariantInformation & { quantity: number }
    const detailSelectedItem = ref<ProductVariantInformation>()

    /**
     * Definition of page-used form
     */
    type Form = {
        bodega?: Warehouse
        comentario: string
        items: QuantifiedItem[]
    }
    type ItemForm = {
        item: Item | null
        quantity: string
    }

    const selectedVariant = ref<ProductVariant>()

    const productFields = [
        { text: 'Código', value: 'id' },
        { text: 'Nombre de producto', value: 'product_name' },
        { text: 'Descripción', value: 'short_description' },
        { text: 'Marca', value: 'brand_name' },
        { text: 'Variantes', value: 'variants' },
    ]

    const formFields: TableField[] = [
        '#',
        { label: 'Nombre de producto', key: 'name' },
        { label: 'Código', key: 'id' },
        { label: 'Marca', key: 'brand' },
        { label: 'Cantidad', key: 'quantity' },
        'Acciones',
    ]

    const form = ref<Form>({
        bodega: undefined,
        comentario: '',
        items: [],
    })

    const itemForm = ref<ItemForm>({
        item: null,
        quantity: '0',
    })

    const products = computed((): Product[] => {
        if (isMessage(productStore.products)) return []
        return productStore.products?.data ?? []
    })

    const currentStockInfo = computed((): SimpleProductStock | null => {
        if (!form.value.bodega || !productStock.value || !selectedVariant.value)
            return null
        const target = productStock.value.find(
            stock =>
                stock.warehouse === form.value.bodega?.id &&
                stock.variant === selectedVariant.value?.id
        )
        return target ?? null
    })

    warehouse.fetchWarehouses().then(() => {
        showWaitOverlay.value = false
    })

    const iformShow = computed(() => ({
        nombre: pickedProduct.value?.product_name,
        variantes: pickedProduct.value?.variants,
        detalle: pickedProduct.value?.summary,
        variante: selectedVariant?.value,
        marca: pickedProduct.value?.brand_name,
    }))
    const loadItems = async () => {
        itemLoading.value = true
        //await itemStore.fetchItemsPaginated(itemPaginationOptions.value)
        await productStore.fetchProducts(paginationOptions.value)
        itemLoading.value = false
    }

    /**
     * Event definitions
     */
    function removeItem(index: number) {
        form.value.items.splice(index, 1)
    }
    function onShowModalClick() {
        loadItems()
        productModalShow.value = true
    }

    async function onRowClick(selectedItem: Product) {
        pickedProduct.value = selectedItem
        selectedVariant.value = undefined
        if (selectedItem.variants.length == 1) {
            // Automatically pick the first variant
            selectedVariant.value = selectedItem.variants[0]
        }
        productModalShow.value = false
        showWaitOverlay.value = true
        const stock = await productStore.findStockByProduct(
            pickedProduct.value.id
        )
        productStock.value = stock
        showWaitOverlay.value = false
    }

    async function refreshStock() {
        if (!pickedProduct.value) return // do anything
        showWaitOverlay.value = true
        const stock = await productStore.findStockByProduct(
            pickedProduct.value.id
        )
        productStock.value = stock
        showWaitOverlay.value = false
    }

    function addToTable() {
        const targetItem = selectedVariant.value
        if (!targetItem) {
            toast.error('Seleccione un producto para añadirlo a la tabla')
            return
        }
        if (form.value.items.findIndex(it => targetItem.id == it.id) >= 0) {
            toast.warning('El ítem ya está añadido')
            return
        }
        form.value.items.push({
            ...targetItem,
            quantity: Number(itemForm.value.quantity),
            parent: pickedProduct.value,
            all_attributes: [
                ...targetItem.attributes,
                ...(pickedProduct.value?.attributes ?? []),
            ],
        } as QuantifiedItem)
        itemForm.value.item = null
        itemForm.value.quantity = '0'
        pickedProduct.value = undefined
        selectedVariant.value = undefined
        toast.success('Item añadido a la tabla')
    }

    function saveOrder() {
        const { value: data } = form
        if (data.bodega == null || data.items.length == 0) {
            toast.error(
                data.items.length == 0
                    ? 'No hay ítems en la tabla para guardar'
                    : 'Seleccione una bodega para continuar'
            )
            return
        }
        const saveData: OrderSaveData = {
            warehouse: data.bodega.id,
            comment: data.comentario,
            items: data.items.map(it => ({
                item: it.id,
                quantity: it.quantity,
            })),
        }
        showWaitOverlay.value = true
        order
            .saveOrder(saveData)
            .then(() => {
                toast.success('Order registrada correctamente')
                data.comentario = ''
                data.bodega = undefined
                data.items.splice(0, data.items.length)
            })
            .catch((it: MessageResponse) => {
                toast.error(`No se pudo guardar la orden [${it.code}]`)
            })
            .finally(() => {
                showWaitOverlay.value = false
            })
    }
    async function showItem(item: ProductVariantInformation) {
        detailSelectedItem.value = item
        itemInfoShow.value = true
    }
    watch(serverOpts, loadItems)

    function showInformation() {
        const targetItem = iformShow.value.variante
        if (!targetItem || pickedProduct.value == undefined) {
            toast.warning('No hay ítem seleccionado')
            return
        }
        const target: ProductVariantInformation = {
            parent: pickedProduct.value,
            all_attributes: [
                ...targetItem.attributes,
                ...(pickedProduct.value?.attributes ?? []),
            ],
            ...targetItem,
        }
        showItem(target)
    }
</script>

<template>
    <main>
        <WaitOverlay :show="showWaitOverlay">
            <ModalDialog
                id="product-modal"
                v-model:show="productModalShow"
                size="3xl"
                title="Lista de productos">
                <!-- <div
                    class="tw-overflow-y-auto tw-max-h-72 tw-text-black dark:tw-text-white"> -->
                <EasyDataTable
                    class="tw-z-10"
                    :headers="productFields"
                    :items="products"
                    buttons-pagination
                    :rows-items="[5, 10, 15, 20]"
                    v-model:server-options="serverOpts"
                    :server-items-length="productPageLength"
                    table-class-name="custom-data-table"
                    :loading="itemLoading"
                    @click-row="onRowClick"
                    show-index>
                    <template #item-variants="{ variants }">
                        {{
                            variants
                                .map((it: ProductVariant) => it.variant_name)
                                .join(', ')
                        }}
                    </template>
                </EasyDataTable>
            </ModalDialog>
            <ModalDialog v-model:show="itemInfoShow" size="xl" ok-text="Cerrar">
                <template #dialog-title>
                    <b class="tw-text-2xl">
                        Detalle del Ítem
                        {{
                            detailSelectedItem?.parent.product_name +
                            ' ' +
                            detailSelectedItem?.variant_name
                        }}
                    </b>
                </template>
                <div class="container">
                    <h3 class="tw-text-xl tw-font-bold">Detalle</h3>
                    <div
                        class="row tw-pb-3 align-content-center justify-content-center gy-2">
                        <template
                            v-for="(key, human_field) in detailParamsDictionary"
                            :key="key">
                            <div class="col-12">
                                <div class="row">
                                    <span class="tw-font-bold col-4">
                                        {{ human_field }}:
                                    </span>
                                    <span
                                        class="col-4"
                                        v-if="detailSelectedItem !== undefined">
                                        {{
                                            detailSelectedItem[
                                                key as keyof ProductVariantInformation
                                            ]
                                        }}
                                    </span>
                                </div>
                            </div>
                        </template>
                        <div class="col-12">
                            <div class="row">
                                <span class="col-4 tw-font-bold"> Marca: </span>
                                <span class="col-4">
                                    {{ detailSelectedItem?.parent.brand_name }}
                                </span>
                            </div>
                        </div>
                        <div class="col-12">
                            <div class="row">
                                <span class="col-4 tw-font-bold">
                                    Descripcion corta:
                                </span>
                                <p class="col-4 tw-text-ellipsis">
                                    {{
                                        detailSelectedItem?.parent
                                            .short_description
                                    }}
                                </p>
                            </div>
                        </div>
                    </div>
                    <div
                        v-if="detailSelectedItem?.all_attributes"
                        class="tw-ring-1 tw-ring-slate-500 tw-rounded tw-pb-3 row">
                        <h3 class="col-12 tw-text-xl tw-py-1.5">
                            <b>Caracteríticas del Ítem</b>
                        </h3>
                        <template
                            v-for="(
                                param, idx
                            ) in detailSelectedItem.all_attributes"
                            :key="idx">
                            <div class="col-6 col-md-3 col-xl-2 tw-text-md">
                                <b>{{ param.name }}:</b>
                            </div>
                            <div class="col-6 col-md-3 col-xl-2">
                                {{ param.value }}
                            </div>
                        </template>
                    </div>
                </div>
            </ModalDialog>
            <ECard>
                <ERow align-v="start">
                    <ECol cols="12" lg="6" xl="4">
                        <ListBox
                            v-model="form.bodega"
                            top-label="Seleccione una Bodega"
                            placeholder="No ha seleccionado una bodega"
                            :options="warehouse.getWarehouseList ?? []"
                            label="name"
                            @change="refreshStock" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="4">
                        <div class="tw-flex tw-flex-col">
                            <label
                                class="tw-font-bold tw-text-md lg:tw-text-base tw-text-left">
                                Comentario del pedido
                            </label>
                            <TextArea
                                v-model="form.comentario"
                                placeholder="Comentario" />
                        </div>
                    </ECol>
                </ERow>
                <ERow>
                    <ECol cols="12" lg="auto">
                        <EButton
                            class="tw-w-full lg:tw-w-auto"
                            @click="onShowModalClick">
                            Seleccionar producto
                        </EButton>
                    </ECol>
                </ERow>
                <div class="tw-flex">
                    <div class="tw-w-[1.5rem]">&ZeroWidthSpace;</div>
                </div>

                <!-- <ERow>
                <ECol cols="12"> -->
                <ECard>
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
                        <ECol cols="12" lg="6">
                            <div class="tw-flex tw-flex-col">
                                <label for="prod-det" class="form-label">
                                    Detalle del producto
                                </label>
                                <TextArea
                                    id="prod-det"
                                    :model-value="iformShow.detalle"
                                    readonly
                                    placeholder="Cargue un ítem para ver su descripción"
                                    resize="vertical" />
                            </div>
                        </ECol>
                        <ECol
                            cols="12"
                            lg="6"
                            v-if="(iformShow.variantes?.length ?? 0) > 1">
                            <ListBox
                                v-model="selectedVariant"
                                :options="iformShow.variantes"
                                label="variant_name"
                                top-label="Variedad a solicitar"
                                placeholder="Seleccionar variedad" />
                        </ECol>
                        <ECol cols="12" lg="5">
                            <InputText
                                label="Cantidad del Producto"
                                v-model="itemForm.quantity"
                                :formatter="(it: string) => it
                                .replace(/(\D|^0+(?=\d+))/g, '') || '0'" />
                        </ECol>
                        <ECol cols="12" lg="3" v-if="selectedVariant">
                            <InputText
                                label="Stock global"
                                :model-value="
                                    selectedVariant?.stock_level.toString()
                                "
                                :status="
                                    selectedVariant?.stock_level
                                        ? selectedVariant.stock_level > 0
                                        : null
                                "
                                readonly />
                        </ECol>
                        <ECol cols="12" lg="3" v-if="selectedVariant">
                            <InputText
                                label="Stock en bodega"
                                :model-value="
                                    currentStockInfo?.stock_level.toString() ??
                                    'no disponible'
                                "
                                readonly />
                        </ECol>
                        <ECol cols="12" lg="auto">
                            <EButton
                                class="tw-w-full lg:tw-w-auto"
                                left-icon="plus"
                                :disabled="
                                    !selectedVariant ||
                                    Number(itemForm.quantity) <= 0
                                "
                                @click="addToTable">
                                Añadir producto
                            </EButton>
                        </ECol>
                        <ECol cols="3">
                            <EButton
                                id="info-button"
                                variant="blank"
                                @click="showInformation">
                                <FontAwesomeIcon icon="circle-info" />
                                <span>&ThinSpace;</span>
                            </EButton>
                        </ECol>
                        <!-- <ECol></ECol>
                    <ECol></ECol> -->
                    </ERow>
                    <!-- Item quantity fields -->
                </ECard>
                <div class="tw-overflow-x-auto">
                    <BTable :fields="formFields" :items="form.items">
                        <template #cell(#)="{ index }">
                            {{ index + 1 }}
                        </template>
                        <template #cell(name)="{ item }">
                            {{
                                `${item.parent.product_name} - ${item.variant_name}`
                            }}
                        </template>
                        <template #cell(brand)="{ item }">
                            {{ item.parent.brand_name }}
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
                <ERow>
                    <ECol class="tw-content-end tw-justify-end">
                        <EButton
                            left-icon="fa-floppy-disk"
                            icon-provider="awesome"
                            @click="saveOrder">
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

    $message: 'Informacion del ítem';
    $l: str-length($message);

    @keyframes info_content {
        0% {
            content: '';
            opacity: 0;
        }
        10% {
            content: str-slice($message, 0, calc($l * 0.1));
        }
        50% {
            content: str-slice($message, 0, calc($l/2));
        }
        80% {
            content: str-slice($message, 0, calc($l * 0.8));
            opacity: 0.65;
        }

        100% {
            content: str-slice($message, 0, $l);
            opacity: 1;
        }
    }

    button#info-button {
        // display:inline-block;
        padding-left: 0.33rem;
        padding-right: 0.66rem;
        transition: all 0.5s;
        overflow: hidden;
        box-shadow: none;
        transition: width 1s ease-in-out;
        svg {
            transition: all 0.75s ease-in-out;
        }

        &:hover {
            padding-left: 0.1rem;
            // padding-right: 0.66rem;

            svg {
                margin-right: 0.11rem;
            }
            span::after {
                animation: info_content 0.25s normal;
                content: 'Informacion del ítem';
                opacity: 1;
                right: 0rem;
            }
        }
        span::after {
            // content: '';
            transition: all 0.75s ease-in-out;
            opacity: 0;
            right: 3rem;
        }
    }
    // button#info-button span:after {

    //     opacity: 0;
    //     top: 0;
    //     transition: all 1.5s;
    //     width: 0;
    // }
    // button#info-button:hover span:after {
    //     opacity: 1;
    //     right: 0;
    //     width: auto;
    // }
</style>
