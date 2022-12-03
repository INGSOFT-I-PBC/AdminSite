<script setup lang="ts">
    import type Item from '@/interfaz/items'
    import ItemDataService from '@/store/item'
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import ECol from '@components/custom/ECol.vue'
    import ERow from '@components/custom/ERow.vue'
    import InputText from '@components/custom/InputText.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import Table from '@components/holders/Table.vue'
    import type { PaginatedResponse } from '@store-types'
    import type { IEmployee, Inventory } from '@store/types'
    import type { BvEvent, TableField } from 'bootstrap-vue-3'
    import moment from 'moment'

    import { useRouter } from 'vue-router'
    import { useToast } from 'vue-toastification'

    import WaitOverlay from '../../components/custom/WaitOverlay.vue'

    const toast = useToast()
    const router = useRouter()
    const showWaitOverlay = ref<boolean>(true)

    type SearchParam = PaginationOptions
    //Paginated
    const searchParam: SearchParam = {
        page: 1,

        per_page: 10,
    }

    const filterOption = ref<
        {
            label: string
            value: 'name' | 'category' | 'code' | 'stock'
        }[]
    >([
        { label: 'Código', value: 'code' },
        { label: 'Nombre', value: 'name' },
        { label: 'Categoría', value: 'category' },
        { label: 'Stock', value: 'stock' },
    ])
    const filterName = ref(filterOption.value[0])
    const filterText = ref<string>('')
    const inventoryForm: Record<string, any> = ref({
        stock: 0,
        name: '',
        category: '',
        code: '',
    })
    const model = ref({})
    const form = ref<Form>({
        items: [],
    })

    type Form = {
        items: Inventory[]
    }
    const productModalShow = ref(false)
    const productModalDelete = ref(false)
    const num = 0
    const formFields: TableField[] = [
        '#',
        { label: 'Código', key: 'codename_Item' },
        { label: 'Nombre', key: 'nombreItem' },
        { label: 'Marca', key: 'brandItem' },
        { label: 'Modelo', key: 'modelItem' },
        { label: 'Categoría', key: 'category_name_Item' },
        { label: 'Precio', key: 'priceItem' },
        { label: 'Stock', key: 'quantity' },
        { label: 'Estado', key: 'is_active' },

        'Acciones',
    ]

    type SelectedItem = { item: Inventory | null }
    const detailSelectedItem = ref<SelectedItem>({
        item: null,
    })

    function showProduct(item: Inventory) {
        detailSelectedItem.value.item = item
        productModalShow.value = true
    }

    function removeItem(index: number) {
        console.log(index)
        form.value.items.splice(index, 1)
    }

    function onSubmit(id: number, index: number) {
        itemForm.value.id = id
        itemForm.value.index = index
        productModalDelete.value = true
    }
    function cleanFilters() {
        filterText.value = ''
        cleanQuery()

        showInvoices2(inventoryForm)
        console.log('clean')
    }
    function cleanQuery() {
        inventoryForm.category = ''
        inventoryForm.stock = 0
        inventoryForm.name = ''
        inventoryForm.code = ''
    }
    function onSubmitSearch(valor: any) {
        if (valor == 'name') {
            cleanQuery()

            inventoryForm.name = filterText.value.trim()
            showInvoices2(inventoryForm)
        }
        if (valor == 'stock') {
            cleanQuery()

            inventoryForm.stock = filterText.value.trim()
            showInvoices2(inventoryForm)
        }
        if (valor == 'code') {
            cleanQuery()
            console.log('entre')

            inventoryForm.code = filterText.value.trim()
            showInvoices2(inventoryForm)
        }
        if (valor == 'category') {
            cleanQuery()

            inventoryForm.category = filterText.value.trim()
            showInvoices2(inventoryForm)
        }
        console.log('fuerasubmir')
    }

    function showInvoices2(query: any) {
        showWaitOverlay.value = true

        const res = ItemDataService.fetchPaginatedListInventory(
            query,
            searchParam
        )
            .then(() => {
                if (
                    (
                        ItemDataService.clients
                            .value as PaginatedResponse<Inventory>
                    ).data !== undefined
                ) {
                    form.value.items = (
                        ItemDataService.clients
                            .value as PaginatedResponse<Inventory>
                    ).data
                    if (form.value.items.length == 0) {
                        toast.info('No se encontraron productos')
                    }
                }

                showWaitOverlay.value = false
            })
            .catch(() => {
                if (filterName.value.value == 'stock') {
                    toast.error('Se esperaba números en la búsqueda con stock')
                    filterText.value = ''
                } else {
                    toast.error('No se pudo realizar la búsqueda ')
                }
                showWaitOverlay.value = false
            })
        console.log('show2')
    }
    async function changeStatus(item: Inventory) {
        if (item.is_active) {
            inactivateItem(item)
        } else {
            activateItem(item)
        }
    }
    async function activateItem(item: Inventory) {
        try {
            await ItemDataService.fetchActivateItem(item.item_id)
            toast.success('Producto activado con éxito')
            item.is_active = true
        } catch (error) {
            console.log(error)
        }
    }

    async function inactivateItem(item: Inventory) {
        try {
            await ItemDataService.fetchInactivateItem(item.item_id)
            toast.success('Producto inactivado con éxito')
            item.is_active = false
        } catch (error) {
            console.log(error)
        }
    }
    function onPaginationClick(event: BvEvent, page: number) {
        searchParam.page = page
        console.log(page)

        showInvoices2(inventoryForm)
        console.log('paginated')
    }
    function go(id: number): void {
        console.log(id)
        router.push({ path: `/inventario/editar/${String(id)}` })
    }
    type DeleteInvoice = {
        id: number
        index: number
    }

    const itemForm = ref<DeleteInvoice>({
        id: 0,
        index: 0,
    })
    function acceptace(): void {
        ItemDataService.deleteItem(itemForm.value.id)
            .then(response => {
                console.log(response.data)
                removeItem(itemForm.value.index)
            })

            .catch((e: Error) => {
                console.log(e)
            })
    }

    function goAgregar(): void {
        router.push({ path: '/inventario/agregar' })
    }
    showInvoices2(inventoryForm)
</script>

<template>
    <main>
        <ModalDialog v-model:show="productModalShow" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl"
                    >Detalle del Producto
                    {{ detailSelectedItem.item?.nombreItem }}</b
                >
            </template>
            <div class="container">
                <div
                    class="row tw-pb-3 align-content-center justify-content-center gy-2">
                    <template
                        v-for="(k, d) in detailSelectedItem.item"
                        :key="k">
                        <div class="row" v-if="d.toString() == 'codename_Item'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Código:</span
                            >
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div class="row" v-if="d.toString() == 'nombreItem'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Nombre:</span
                            >
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div class="row" v-if="d.toString() == 'brandItem'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Marca:</span
                            >
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div class="row" v-if="d.toString() == 'modelItem'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Modelo:</span
                            >
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div
                            class="row"
                            v-if="d.toString() == 'category_name_Item'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Categoria:</span
                            >
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div class="row" v-if="d.toString() == 'priceItem'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Precio:</span
                            >
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div class="row" v-if="d.toString() == 'quantity'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Stock:</span
                            >
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div
                            class="row"
                            v-if="d.toString() == 'created_by_Item'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Creado por:</span
                            >
                            <span class="col-6"
                                >{{ (k as IEmployee).name }}
                                {{ (k as IEmployee).lastname }}</span
                            >
                        </div>
                        <div class="row" v-if="d.toString() == 'created_at'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Fecha de creación:</span
                            >
                            <span class="col-6"
                                >{{ moment(k as string).format('DD/MM/YYYY') }}
                            </span>
                        </div>
                        <div class="row" v-if="d.toString() == 'created_at'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Hora de creación:</span
                            >
                            <span class="col-6"
                                >{{ moment(k as string).format('HH:mm:ss') }}
                            </span>
                        </div>
                    </template>
                </div>
            </div>
        </ModalDialog>
        <ModalDialog
            id="product-modal"
            v-model:show="productModalDelete"
            title="Eliminar Producto"
            ok-text="Eliminar"
            @ok="acceptace"
            button-type="ok-cancel">
            <h1 style="font-size: 15px; color: black; text-align: left">
                ¿Está seguro de eliminar el Producto?
            </h1>
        </ModalDialog>

        <ECard>
            <ERow>
                <h1 style="font-size: 35px; color: black">Inventario</h1>
            </ERow>
            <nav class="navbar">
                <div class="container-fluid">
                    <EButton variant="secondary" @click="goAgregar"
                        >+ Agregar producto
                    </EButton>
                    <ECol cols="3" md="3" xl="3">
                        <ListBox
                            :clearable="true"
                            v-model="filterName"
                            top-label="Filtrar por:"
                            :options="filterOption" />
                    </ECol>
                    <ECol cols="3" md="3" xl="3">
                        <InputText
                            v-model="filterText"
                            label="Cuadro de búsqueda"
                            :placeholder="`Búsqueda por ${filterName.label}`" />
                    </ECol>
                    <EButton @click="onSubmitSearch(`${filterName.value}`)"
                        >Buscar</EButton
                    >
                    <EButton @click="cleanFilters">Limpiar</EButton>
                </div>
            </nav>

            <!-- <ERow>
                <ECol cols="12"> -->
            <WaitOverlay :show="showWaitOverlay">
                <BTable :fields="formFields" :items="form.items">
                    <template #cell(#)="{ index }">{{ index + 1 }} </template>

                    <template #cell(is_active)="{ index }">
                        <div class="form-check form-switch">
                            <input
                                class="form-check-input"
                                name="status"
                                type="checkbox"
                                role="switch"
                                :checked="form.items[index].is_active"
                                @change="changeStatus(form.items[index])" />
                        </div>
                    </template>
                    <template #cell(Acciones)="{ item, index }">
                        <div class="t-button-group">
                            <e-button
                                left-icon="fa-eye"
                                variant="secondary"
                                @click="showProduct(item)"
                                >Ver detalles</e-button
                            >
                            <e-button
                                left-icon="fa-edit"
                                variant="success"
                                @click="go(item['id'])"
                                >Editar</e-button
                            >
                            <e-button
                                left-icon="fa-trash-can"
                                variant="cancel"
                                @click="onSubmit(item['item_id'], index)">
                                Eliminar
                            </e-button>
                        </div>
                    </template>
                </BTable>

                <div class="row">
                    <BPagination
                        align="center"
                        v-model="searchParam.page"
                        :total-rows="ItemDataService.clients.value?.total ?? 1"
                        :per-page="searchParam.per_page ?? 10"
                        next-text="Siguiente"
                        prev-text="Anterior"
                        class="paginator"
                        hide-goto-end-buttons
                        @page-click="onPaginationClick" />
                </div>
            </WaitOverlay>

            <!-- </ECol>h
            </ERow> -->
        </ECard>
    </main>
</template>
