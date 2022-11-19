<script setup lang="ts">

//import type { Warehouse } from '@store/types';
import ModalDialog from '@components/custom/ModalDialog.vue'
import InputText from '@components/custom/InputText.vue'
import type { OrderSaveData } from '@store/types/orders.model';
import { useWarehouseStore } from '@store/warehouse';
import type { TableField } from 'bootstrap-vue-3';
import { BCol, BContainer, BFormGroup, BInputGroup, BRow, BTable } from 'bootstrap-vue-3';
import WaitOverlay from '../../components/custom/WaitOverlay.vue';
import EButton from '@components/custom/EButton.vue';
//import { type Item, type Warehouse, type Purchase, type TomaFisica, type WhWithTomaFisica } from '@store/types'
import type {  Item,  Warehouse,  Purchase,  TomaFisica,  WhWithTomaFisica } from '@store/types'
import type { ItemProps } from '@store/types/items.model'
import type { WarehouseQuery } from '@store/models/warehouseModels';
import { useRouter } from 'vue-router'
    const router = useRouter()

    const warehouse = useWarehouseStore()
    const showWaitOverlay = ref<boolean>(true)
    //let activeWhInformation = ref(<warehouseInformation>{})
    let invTableTotal = ref(15)

    let currentMainPage = ref(1)
    let currentAsidePage = ref(1)
    let whRows = ref(0)
    const whPageCount = ref(15)
    const whInformationPerPage = ref(15)
    let itemInfoShow = ref(false)

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
    ordenes2: OrderSaveData[]
    }

    const formFields: TableField[] = [
        {label: 'ID Orden', key: 'id'},
        { label: 'Numero Bodega ', key: 'warehouse' },
        { label: 'Fecha Pedido', key: 'requested_at' },
        { label: 'Id De Solicitador', key: 'requested_by' },
        //{ label: 'Detalles', key: 'status' },
        'Acciones',
    ]

    let activeWhInformation = ref(<warehouseInformation>{})
    let ordenes = ref(<arr_ordens>{})


    async function lastOrders(){
        showWaitOverlay.value = true

        //let wh_name = activeWhInformation.value.bodega.id
        let response = await warehouse.fetchOrdersWarehouse()

        //activeWhInformation.value.arr_orders = response.data.data
        //ordenes.value.ordenes= response.data.data
        console.log(response)
        activeWhInformation.value.ordenes2 = response

        //invTableTotal.value = response.data.total
        showWaitOverlay.value = false
    }

    lastOrders()


function goEdit(id: number): void {
        console.log(id)
        router.push({ path: `/bodegas/tablas-solicitudes-pedidos/${String(id)}` })
    }



</script>

<template>
    <main>
        <div
        class="row tw-bg-slate-50 dark:tw-bg-slate-600 mt-2 mb-2"
            style="background-color:rgb(60, 60, 60); border-radius: 5px">

            <div >

                <b-container fluid>

                    <div class="container"
            style="background-color:rgb(60, 60, 60); border-radius: 5px">
                        <b-row>
                            <b-col lg="6" class="my-1">
                                <InputText label="Cuadro de búsqueda" :placeholder="`Búsqueda por `" />
                                <EButton class="tw-min-w-full" @click="">Buscar</EButton>
                            </b-col>
                        </b-row>
                    </div>


                    <WaitOverlay :show="showWaitOverlay"></WaitOverlay>
                    <BTable :fields="formFields" :items="activeWhInformation.ordenes2" class="table text-center text-bg-dark" id="whinv-table">
                        <template #cell(Acciones)="{item}">
                        <div class="t-button-group">
                            <e-button
                                left-icon="fa-eye"
                                type="success"
                                @click="goEdit(item['id'])"
                                >Ver Detalles</e-button
                            >
                        </div>
                    </template>

                    </BTable>

                </b-container>
            </div>

            <div class="container">

            </div>
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
    --bs-list-group-item-padding-x: 0.80rem;
    --bs-list-group-item-padding-y: 0.3rem;
}

.table {
    >thead {
        @apply tw-bg-secondary tw-text-white tw-font-bold tw-text-sm;
    }

    >tbody {
        @apply tw-text-xs
    }

    @media (prefers-color-scheme: dark) {
        color: white !important;
        --bs-table-striped-color: theme(colors.zinc.400);
        --bs-table-hover-color: theme('colors.primary.light');
        --bs-table-hover-bg: theme(colors.primary.light / 15%);
    }
}
</style>


