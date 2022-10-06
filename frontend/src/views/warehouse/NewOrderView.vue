<script setup lang="ts">
    import ECard from '../../components/custom/ECard.vue'
    import ERow from '../../components/custom/ERow.vue'
    import ECol from '../../components/custom/ECol.vue'
    import ListBox from '../../components/custom/ListBox.vue'
    import InputText from '../../components/custom/InputText.vue'
    import EButton from '../../components/custom/EButton.vue'
    import ModalDialog from '../../components/custom/ModalDialog.vue'
    import Title from '../../components/custom/Title.vue'
    import Table from '../../components/holders/Table.vue'
    import { computed, reactive } from 'vue'
    import WaitOverlay from '../../components/custom/WaitOverlay.vue'
    import { useWarehouseStore } from '@store/warehouse'
    import TextArea from '../../components/custom/TextArea.vue'
    import { isMessage, type Item, type Warehouse } from '@store/types'
    import { BTable, type TableField, BFormInput } from 'bootstrap-vue-3'
    import { useItemStore } from '@store/items'
    /**
     * Utility object definitions
     */
    const itemStore = useItemStore()

    /**
     * View Holders
     */
    const warehouse = useWarehouseStore()
    const model = ref({})
    const showWaitOverlay = ref(true)
    const productModalShow = ref(false)
    // const currentItem = ref<Item | null>(null)
    // const selectedProduct = null
    const tableSettings = reactive<TableHeaderSettings>({
        headers: [
            {
                label: 'Nombre del producto',
                attribute: 'name',
            },
            {
                label: 'Código',
                attribute: 'code',
            },
            {
                label: 'Cantidad',
                attribute: 'quantity',
            },
            {
                label: 'Detalles',
                attribute: 'detail',
            },
            {
                label: 'Opciones',
                attribute: '',
            },
        ],
        rows: [
            {
                name: 'Zapatos Marca X',
                code: '102-XFSOE',
                quantity: 10,
                detail: '',
            },
            {
                name: 'Camiseta deportiva',
                code: '102-XFSOE',
                quantity: 10,
                detail: '',
            },
            {
                name: 'Camiseta deportiva modelo c',
                code: '102-XFSOE',
                quantity: 10,
                detail: '',
            },
            {
                name: 'Zapatos Marca X',
                code: '102-XFSOE',
                quantity: 10,
                detail: '',
            },
            {
                name: 'Zapatos Marca X',
                code: '102-XFSOE',
                quantity: 10,
                detail: '',
            },
            {
                name: 'Zapatos Marca X',
                code: '102-XFSOE',
                quantity: 10,
                detail: '',
            },
            {
                name: 'Zapatos Marca X',
                code: '102-XFSOE',
                quantity: 10,
                detail: '',
            },
        ],
    })
    const cols: TableField[] = [
        '#',
        { label: 'Producto', key: 'name' },
        { label: 'Código', key: 'description' },
        { label: 'Marca', key: 'brand' },
    ]

    const subTotal = computed(() => 0)
    const iva = computed(() => subTotal.value * 0.12)
    interface productModel {
        name: string
        code: string
        quantity: number
        detail: string
    }
    let selectedProduct: Optional<productModel> = null
    function showProduct(product: productModel) {
        selectedProduct = product
        console.log(selectedProduct)
        productModalShow.value = true
    }
    function removeItem(index: number) {
        tableSettings.rows?.splice(index, 1)
    }

    type QuantifiedItem = Item & { quantity: number }

    /**
     * Definition of page-used form
     */
    type Form = {
        bodega: Optional<Warehouse>
        comentario: string
        items: QuantifiedItem[]
    }
    type ItemForm = {
        item: Item | null
        quantity: string
    }
    const formFields: TableField[] = [
        '#',
        { label: 'Nombre de producto', key: 'name' },
        { label: 'Código', key: 'descripcion' },
        { label: 'Marca', key: 'brand' },
        'Acciones',
    ]
    const form = ref<Form>({
        bodega: null,
        comentario: '',
        items: [],
    })
    const itemForm = ref<ItemForm>({
        item: null,
        quantity: '0',
    })

    const items = computed((): Item[] => {
        if (isMessage(itemStore.paginatedItems)) return []
        return itemStore.paginatedItems?.data || []
    })

    warehouse.fetchWarehouses().then(it => {
        showWaitOverlay.value = false
    })

    /**
     * Event definitions
     */
    function onShowModalClick() {
        console.log('Hola mudno')
        itemStore.fetchItemsPaginated({ page: 1 })
        productModalShow.value = true
    }

    function onRowClick(selectedItem: Item) {
        console.log('Data: ', selectedItem)
        itemForm.value.item = selectedItem
        productModalShow.value = false
    }
    function onQuantityChange() {
        console.log('haosdfasfdklaj;sdfjka;s')
    }
    function addToTable() {
        form.value.items.push({
            ...itemForm.value.item,
            quantity: Number(itemForm.value.quantity),
        } as QuantifiedItem)
        itemForm.value.item = null
        itemForm.value.quantity = '0'
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
                <BTable
                    :fields="cols"
                    sticky-header
                    hover="true"
                    striped="true"
                    :items="items"
                    responsive
                    head-variant="dark"
                    :current-page="itemStore.currentPaginatedItemPage"
                    @row-clicked="onRowClick">
                    <template #cell(#)="d">
                        <b>{{
                            itemStore.currentPaginatedItemPage! + d.index
                        }}</b>
                    </template>
                </BTable>
                <!-- </div> -->
            </ModalDialog>
            <ECard>
                <ERow align-v="start">
                    <ECol cols="12" lg="6" xl="4">
                        <ListBox
                            v-model="model"
                            top-label="Seleccione un filtro"
                            :options="warehouse.getWarehouseList ?? []"
                            label="name" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="4">
                        <div class="tw-flex tw-flex-col">
                            <label
                                class="tw-font-bold tw-text-md lg:tw-text-base tw-text-left"
                                >Comentario del pedido</label
                            >
                            <TextArea
                                v-model="form.comentario"
                                placeholder="Comentario" />
                        </div>

                        <!-- <InputText
                            type="text-area"
                            label="Comentario del pedido"
                            placeholder="Razón o comentario del pedido" /> -->
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
                    <ERow align-v="start">
                        <ECol cols="12" lg="6">
                            <InputText
                                label="Producto seleccionado"
                                :model-value="itemForm.item?.name"
                                readonly />
                        </ECol>
                        <ECol cols="12" lg="6">
                            <InputText
                                label="Código de producto"
                                :model-value="
                                    itemForm.item?.id?.toString() ??
                                    'Item no tiene código de producto'
                                "
                                readonly />
                        </ECol>
                        <ECol cols="12" lg="6">
                            <div class="tw-flex tw-flex-col">
                                <label for="prod-det" class="form-label">
                                    Detalle del producto
                                </label>
                                <TextArea
                                    id="prod-det"
                                    :model-value="
                                        itemForm.item?.category?.description ??
                                        'Item no tiene descripcion'
                                    "
                                    readonly
                                    placeholder="Cargue un ítem para ver su descripción"
                                    resize="vertical" />
                            </div>
                        </ECol>
                        <ECol cols="12" lg="5">
                            <InputText
                                label="Cantidad del Producto"
                                v-model.number="itemForm.quantity"
                                :formatter="(it: string) => it.replace(/\D/g, '')"
                                @change="onQuantityChange" />
                        </ECol>
                        <ECol cols="12" lg="auto">
                            <EButton
                                class="tw-w-full lg:tw-w-auto"
                                left-icon="plus"
                                :disabled="
                                    itemForm.item == null ||
                                    Number(itemForm.quantity) <= 0
                                "
                                @click="addToTable">
                                Añadir producto
                            </EButton>
                        </ECol>
                        <!-- <ECol></ECol>
                    <ECol></ECol> -->
                    </ERow>
                    <!-- Item quantity fields -->
                </ECard>
                <div class="tw-overflow-x-auto">
                    <BTable :fields="formFields" :items="form.items"> </BTable>
                    <Table :header="tableSettings" v-show="false">
                        <template #body-cell="{ cellData, colIdx, rowIdx }">
                            <div
                                v-if="colIdx > 3"
                                class="tw-grid tw-grid-flow-col tw-rounded tw-overflow-hidden">
                                <button
                                    class="tw-bg-blue-600 tw-px-4 tw-py-1 tw-text-white"
                                    @click="
                                        showProduct(cellData as productModel)
                                    ">
                                    Ver más detalles
                                </button>
                                <button
                                    class="tw-bg-red-600 tw-py-1 tw-text-white"
                                    @click="removeItem(rowIdx)">
                                    Eliminar
                                </button>
                            </div>
                        </template>
                    </Table>
                </div>
                <ERow>
                    <ECol class="tw-content-end tw-justify-end">
                        <div
                            v-show="false"
                            class="tw-flex tw-flex-col tw-font-bold tw-content-end tw-items-center tw-justify-between">
                            <span>Sub Total: ${{ subTotal.toFixed(3) }}</span>
                            <!-- <div> -->
                            <span>IVA 12%: ${{ iva.toFixed(3) }}</span>
                            <span
                                >Total: ${{ (subTotal + iva).toFixed(3) }}</span
                            >
                            <!-- </div> -->
                        </div>
                        <EButton left-icon="save">Guardar</EButton>
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
</style>
