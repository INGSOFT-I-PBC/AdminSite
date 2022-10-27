<script setup lang="ts">
    import ECard from '../../components/custom/ECard.vue'
    import ERow from '../../components/custom/ERow.vue'
    import ECol from '../../components/custom/ECol.vue'
    import ListBox from '../../components/custom/ListBox.vue'
    import InputText from '../../components/custom/InputText.vue'
    import EButton from '../../components/custom/EButton.vue'
    import ModalDialog from '../../components/custom/ModalDialog.vue'
    import Title from '../../components/custom/Title.vue'
    import { computed, watch } from 'vue'
    import WaitOverlay from '../../components/custom/WaitOverlay.vue'
    import { useWarehouseStore } from '@store/warehouse'
    import TextArea from '../../components/custom/TextArea.vue'
    import {
        isMessage,
        type Item,
        type MessageResponse,
        type Warehouse,
    } from '@store/types'
    import type { TableField } from 'bootstrap-vue-3'
    import { useItemStore } from '@store/items'
    import { useToast } from 'vue-toastification'
    import type { ServerOptions } from 'vue3-easy-data-table'
    import type { ItemProps } from '@store/types/items.model'
    import type { OrderSaveData } from '@store/types/orders.model'
    import { useOrderStore } from '@store/order'
    /**
     * Utility object definitions
     */
    const itemStore = useItemStore()
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
    const itemPaginationOptions = computed<PaginationOptions>(() => ({
        page: serverOpts.value.page,
        per_page: serverOpts.value.rowsPerPage,
    }))

    const itemPageLength = computed(() => {
        const items = itemStore.paginatedItems
        if (items == null || isMessage(items)) return 0
        return items.total
    })
    type QuantifiedItem = Item & { quantity: number }
    type SelectedItem = { item: Item | null; props: ItemProps[] }
    const detailSelectedItem = ref<SelectedItem>({
        item: null,
        props: [],
    })

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
    const itemHeader = [
        { text: 'Código', value: 'id' },
        { text: 'Nombre de producto', value: 'name' },
        { text: 'Marca', value: 'brand' },
        { text: 'Modelo', value: 'model' },
        { text: 'Categoría', value: 'category.name' },
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

    const items = computed((): Item[] => {
        if (isMessage(itemStore.paginatedItems)) return []
        return itemStore.paginatedItems?.data || []
    })

    warehouse.fetchWarehouses().then(it => {
        showWaitOverlay.value = false
    })

    const iformShow = computed(() => ({
        nombre: itemForm.value.item?.name ?? '',
        detalle: itemForm.value.item?.category?.description ?? '',
        codigo: itemForm.value.item?.id?.toString(),
    }))
    const loadItems = async () => {
        itemLoading.value = true
        await itemStore.fetchItemsPaginated(itemPaginationOptions.value)
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

    function onRowClick(selectedItem: Item) {
        console.log('Data: ', selectedItem)
        itemForm.value.item = selectedItem
        productModalShow.value = false
    }
    function addToTable() {
        const targetItem = itemForm.value.item
        if (!targetItem) {
            toast.error('Seleccione un ítem para añadirlo a la tabla')
            return
        }
        if (form.value.items.findIndex(it => targetItem.id == it.id) >= 0) {
            toast.warning('El ítem ya está añadido')
            return
        }
        form.value.items.push({
            ...itemForm.value.item,
            quantity: Number(itemForm.value.quantity),
        } as QuantifiedItem)
        itemForm.value.item = null
        itemForm.value.quantity = '0'
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
    async function showItem(item: Item) {
        detailSelectedItem.value.item = item
        detailSelectedItem.value.props = await itemStore.fetchItemProperties(
            item.id
        )
        itemInfoShow.value = true
    }
    watch(serverOpts, loadItems)
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
                    :headers="itemHeader"
                    :items="items"
                    buttons-pagination
                    :rows-items="[5, 10, 15, 20]"
                    v-model:server-options="serverOpts"
                    :server-items-length="itemPageLength"
                    table-class-name="custom-data-table"
                    :loading="itemLoading"
                    @click-row="onRowClick" />
            </ModalDialog>
            <ModalDialog v-model:show="itemInfoShow" size="xl">
                <template #dialog-title>
                    <b class="tw-text-2xl"
                        >Detalle del Ítem {{ detailSelectedItem.item?.name }}</b
                    >
                </template>
                <div class="container">
                    <h3 class="tw-text-xl tw-font-bold">Detalle</h3>
                    <div
                        class="row tw-pb-3 align-content-center justify-content-center gy-2">
                        <template
                            v-for="(d, k) in detailSelectedItem.item"
                            :key="k">
                            <div
                                class="tw-rounded tw-ring-1 tw-ring-slate-500 tw-py-1 col-12 col-md-5 tw-mx-2"
                                v-if="
                                    !['category', 'img', 'quantity'].includes(k)
                                ">
                                <div class="row">
                                    <span class="tw-w-1/2 tw-font-bold col-6"
                                        >{{ k }}:</span
                                    >
                                    <span class="col-6">{{ d }}</span>
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
                            v-for="(param, idx) in detailSelectedItem.props"
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
                                placeholder="Seleccione un ítem"
                                :model-value="iformShow.nombre"
                                readonly />
                        </ECol>
                        <ECol cols="12" lg="6">
                            <InputText
                                label="Código de producto"
                                placeholder="Código no disponible (Seleccione un ítem)"
                                :model-value="iformShow.codigo"
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
                        <ECol cols="12" lg="5">
                            <InputText
                                label="Cantidad del Producto"
                                v-model.number="itemForm.quantity"
                                :formatter="(it: string) => it.replace(/\D/g, '')" />
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
                    <BTable :fields="formFields" :items="form.items">
                        <template #cell(#)="{ index }">
                            {{ index + 1 }}
                        </template>
                        <template #cell(Acciones)="{ item, index }">
                            <div class="t-button-group">
                                <e-button
                                    left-icon="fa-eye"
                                    @click="showItem(item)"
                                    type="secondary"
                                    >Ver detalles</e-button
                                >
                                <e-button
                                    left-icon="fa-trash-can"
                                    type="cancel"
                                    @click="removeItem(index)">
                                    <span
                                        class="tw-invisible md:tw-visible tw-font-bold"
                                        >Eliminar</span
                                    ></e-button
                                >
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
</style>
