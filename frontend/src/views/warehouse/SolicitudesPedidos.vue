<script setup lang="ts">
    //import type { Warehouse } from '@store/types';
    import EButton from '@components/custom/EButton.vue'
    import InputText from '@components/custom/InputText.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import type { WarehouseQuery } from '@store/models/warehouseModels'
    //import { type Item, type Warehouse, type Purchase, type TomaFisica, type WhWithTomaFisica } from '@store/types'
    import type {
        Item,
        Purchase,
        TomaFisica,
        Warehouse,
        WhWithTomaFisica,
    } from '@store/types'
    import type { ItemProps } from '@store/types/items.model'
    import type {
        OrderSaveData,
        OrderSaveData2,
    } from '@store/types/orders.model'
    import { useWarehouseStore } from '@store/warehouse'
    import type { TableField } from 'bootstrap-vue-3'
    import {
        BCol,
        BContainer,
        BFormGroup,
        BInputGroup,
        BRow,
        BTable,
    } from 'bootstrap-vue-3'

    import { useRouter } from 'vue-router'

    import WaitOverlay from '../../components/custom/WaitOverlay.vue'

    const router = useRouter()

    const warehouse = useWarehouseStore()
    const showWaitOverlay = ref<boolean>(true)
    //let activeWhInformation = ref(<warehouseInformation>{})
    const invTableTotal = ref(15)

    const currentMainPage = ref(1)
    const currentAsidePage = ref(1)
    const whRows = ref(0)
    const whPageCount = ref(15)
    const whInformationPerPage = ref(15)
    const itemInfoShow = ref(false)

    type SelectedItem = { item: Item | null; props: ItemProps[] }
    const detailSelectedItem = ref<SelectedItem>({
        item: null,
        props: [],
    })

    type QuantifiedItem = Item & { quantity: number }

    type Form = {
        bodega?: Warehouse
        comentario: string
        items: []
    }

    const form = ref<Form>({
        bodega: undefined,
        comentario: '',
        items: [],
    })

    /*
    type arr_ordens = {
        nameWarehouse: number
        fechaPedido: string
        solicitadoPor: string
        estado: string
        elementos: []
        ordenes: OrderSaveData[]
    }
    */

    type warehouseInformation = {
        bodega: Warehouse
        inventory: QuantifiedItem[]
        purchases: Purchase[]
        tomasFisicas: TomaFisica[]
        movements: []
        ordenes2?: OrderSaveData2[]
        //ord: OrderSaveData3[]
    }

    const formFields: TableField[] = [
        { label: 'ID Orden', key: 'id' },
        { label: 'Nombre Bodega ', key: 'warehouse' },
        { label: 'Fecha Pedido', key: 'requested_at' },
        { label: 'Nombre Solicitador', key: 'requested_by' },
        //{ label: 'Detalles', key: 'status' },
        'Acciones',
    ]

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
        ordenes2: [],
    })
    type FilterOption = {
        label: string
        value: 'bodega' | 'solicitador'
    }
    const filterOption = ref<FilterOption[]>([
        { label: 'Bodega', value: 'bodega' },
        { label: 'Solicitador', value: 'solicitador' },
    ])

    const filterName = ref(filterOption.value[0])
    const filterText = ref<string>('')

    async function lastOrders() {
        showWaitOverlay.value = true

        const busqueda = filterText.value != '' ? filterText.value : ''
        const filtro = filterName.value.value

        const response = await warehouse.fetchOrdersWarehouse(
            null,
            busqueda,
            filtro
        )

        console.log(response)
        console.log('hola', typeof activeWhInformation.value?.ordenes2)
        console.log(activeWhInformation.value?.ordenes2)
        console.log(activeWhInformation.value?.ordenes2 == undefined)
        //console.log(order1.warehouse)
        console.log(activeWhInformation.value.ordenes2)

        //if (activeWhInformation.value?.ordenes2 == undefined) return

        activeWhInformation.value.ordenes2 = response
        //return
        console.log('hola')
        //activeWhInformation.value?.ordenes2 = response
        console.log(activeWhInformation.value?.ordenes2)

        console.log('hola')
        showWaitOverlay.value = false
    }

    lastOrders()

    function goEdit(id: number): void {
        console.log(id)
        router.push({
            path: `/bodegas/tablas-solicitudes-pedidos/${String(id)}`,
        })
    }

    function prueba1() {
        console.log(filterName.value.value)
    }
</script>

<template>
    <main>
        <div
            class="row tw-bg-slate-50 dark:tw-bg-slate-600 mt-2 mb-2"
            style="background-color: rgb(60, 60, 60); border-radius: 5px">
            <div>
                <b-container fluid>
                    <div
                        class="container"
                        style="
                            background-color: rgb(60, 60, 60);
                            border-radius: 5px;
                        ">
                        <b-row>
                            <b-col lg="6" class="my-1">
                                <ListBox
                                    :clearable="true"
                                    v-model="filterName"
                                    top-label="Filtrar por:"
                                    :options="filterOption" />
                                <EButton
                                    style="
                                        margin-top: 10px;
                                        margin-bottom: 10px;
                                    "
                                    class="tw-min-w-full"
                                    @click="lastOrders"
                                    >Buscar</EButton
                                >
                            </b-col>
                            <InputText
                                v-model="filterText"
                                label="Cuadro de búsqueda"
                                :placeholder="`Búsqueda por ${filterName.label}`" />
                        </b-row>
                    </div>

                    <WaitOverlay :show="showWaitOverlay"></WaitOverlay>
                    <BTable
                        :fields="formFields"
                        :items="activeWhInformation?.ordenes2"
                        class="table text-center text-bg-dark"
                        id="whinv-table">
                        <template #cell(Acciones)="{ item }">
                            <div class="t-button-group">
                                <e-button
                                    left-icon="fa-eye"
                                    type="button"
                                    @click="goEdit(item['id'])"
                                    >Ver Detalles</e-button
                                >
                            </div>
                        </template>
                    </BTable>
                </b-container>
            </div>

            <div class="container"></div>
        </div>
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
