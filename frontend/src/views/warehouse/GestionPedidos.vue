<script setup lang="ts">
import EButton from '@components/custom/EButton.vue'
import ECard from '@components/custom/ECard.vue'
import type { TableField } from 'bootstrap-vue-3'
import ModalDialog from '../../components/custom/ModalDialog.vue'
import { useWarehouseStore } from '@store/warehouse'
import { useItemStore } from '@/store'
import WaitOverlay from '../../components/custom/WaitOverlay.vue'
import { computed, ref } from 'vue'
//import type { Item, Warehouse, Purchase, TomaFisica, WhWithTomaFisica } from '@store/types'
import { type Item, type Warehouse, type Purchase, type TomaFisica, type WhWithTomaFisica } from '@store/types'
import type { ItemProps } from '@store/types/items.model'

/*
type SelectedItem = { item: Item | null; props: ItemProps[] }
type QuantifiedItem = Item & { quantity: number }

type warehouseInformation = {
    bodega: Warehouse
    inventory: QuantifiedItem[]
    purchases: Purchase[]
    tomasFisicas: TomaFisica[]
    movements: []
}

const showWaitOverlay = ref(true)

const warehouse = useWarehouseStore()

const itemStore = useItemStore()

const whPageCount = ref(15)

const showAllWarehouses = ref(true)

const whInformationPerPage = ref(15)

const detailSelectedItem = ref<SelectedItem>({
    item: null,
    props: [],
})

const allWarehousesFields: TableField[] = [
    '#',
    { label: 'Nombre', key: 'name' },
    { label: 'Fecha Toma Fisica', key: 'whtf_created_at' },
    'Realizada_Por',
    'Novedad',
    'Detalles',
]

const inventoryFields: TableField[] = [
    '#',
    { label: 'Codigo Producto', key: 'codename' },
    { label: 'Nombre Producto', key: 'name' },
    { label: 'Stock', key: 'quantity' },
    { label: 'Precio', key: 'price' },
    "P.Venta",
    'Acciones',
]

const purchasesFields: TableField[] = [
    '#',
    { label: 'Fecha Creación', key: 'created_at' },
    { label: 'Codigo Orden', key: 'reference' },
    { label: 'Proveedor', key: 'proveedor' },
    'Fecha Completada',
    'Entregado',
    { label: 'Pago', key: 'invoice' },
    { label: 'Fecha Pago', key: 'paid_at' },
    'Acciones',
]

const toamsFisFields: TableField[] = [
    '#',
    { label: 'Fecha Realizacion', key: 'created_at' },
    { label: 'Realizda por', key: 'employee_name' },
    { label: 'Novedad', key: 'novedad' },
    'Acciones',
]

let allWarehousesTableInformation: [] = []

let currentAsidePage = ref(1)
let whRows = ref(0)
let paginatedWarehouse = ref()
let activeWharehouseButton = ref(-1)

let currentMainPage = ref(1)
let paginatedMainTable = ref()

let activeWhInformation = ref(<warehouseInformation>{})

let currentInvPage = ref(1)
let invTableTotal = ref(15)

let currentTomasFisicasPage = ref(1)
let tomasFisTableTotal = ref(15)

let currentPurchasePage = ref(1)
let purchaseTableTotal = ref(15)

let currentMovPage = ref(1)
let movementTableTotal = ref(15)

//Specific warehouse information variables and methods

let itemInfoShow = ref(false)

function choosePurchaseIcon(purchase: Purchase) {
    if (!purchase) {
        return "question"
    }
    if (purchase.status == "pagado") {
        return "x-square"
    }
    if (purchase.status == 'confirmado') {
        return "square"
    }
    return "question"
}

function paginateAside(page_size: number, page_number: number) {
    paginatedWarehouse.value = (warehouse.getWarehouseList ?? []).slice(
        page_number * page_size,
        (page_number + 1) * page_size
    );
}

function onPageChanged(event: any, page: number) {
    paginateAside(whPageCount.value, page - 1);
}


function paginateMain(page_size: number, page_number: number) {
    paginatedMainTable.value = allWarehousesTableInformation.slice(
        page_number * page_size,
        (page_number + 1) * page_size
    );
}

function onMainPageChanged(event: any, page: number) {
    paginateMain(whPageCount.value, page - 1);
}



function resetInvData() {

    invTableTotal.value, tomasFisTableTotal.value, purchaseTableTotal.value, movementTableTotal.value = 1
    currentInvPage.value, currentTomasFisicasPage.value, currentPurchasePage.value, currentMovPage.value = 1

}


async function onPageChangedInventory(event: any, page: number) {

    showWaitOverlay.value = true

    let wh_id = activeWhInformation.value.bodega.id

    let response = await warehouse.fetchPaginatedWarehouseInventory(
        { id: wh_id }, { page: page, per_page: whInformationPerPage.value }
    )

    activeWhInformation.value.inventory = response.data.data

    invTableTotal.value = response.data.total

    showWaitOverlay.value = false

}




async function onPageChangedTomaFisicas(event: any, page: number) {

    showWaitOverlay.value = true

    let wh_id = activeWhInformation.value.bodega.id

    let response = await warehouse.fetchPaginatedWarehouseTomasFisicas(
        { id: wh_id }, { page: page, per_page: whInformationPerPage.value }
    )

    activeWhInformation.value.tomasFisicas = response.data.data

    tomasFisTableTotal.value = response.data.total

    showWaitOverlay.value = false

}




async function onPageChangedPurchase(event: any, page: number) {

    showWaitOverlay.value = true

    let wh_id = activeWhInformation.value.bodega.id

    let response = await warehouse.fetchPaginatedWarehousePurchase(
        { id: wh_id }, { page: page, per_page: whInformationPerPage.value }
    )

    activeWhInformation.value.purchases = response.data.data

    purchaseTableTotal.value = response.data.total

    showWaitOverlay.value = false

}



function wharehouseButtonPressed(event: any, whId: number, index: number) {

    showAllWarehouses.value = false

    activeWharehouseButton.value = whId

    activeWhInformation.value.bodega = (warehouse.getWarehouseList ?? [])[index]

    showWaitOverlay.value = true

    resetInvData()

    onPageChangedInventory(event, 1).then(() => {
        showWaitOverlay.value = false
    })

    onPageChangedPurchase(event, 1)

    onPageChangedTomaFisicas(event, 1)


}

async function showItem(item: Item) {
    detailSelectedItem.value.item = item
    itemInfoShow.value = true
    detailSelectedItem.value.props = await itemStore.fetchItemProperties(
        item.id
    )

}

const truncate = (text: string, length: number, suffix: string) => {

    if (typeof (text) == undefined || text == null) {
        return '---'
    }
    if (text.length > length) {
        return text.substring(0, length) + suffix;
    } else {
        return text;
    }
};

warehouse.fetchWarehouses().then(it => {
    whRows.value = (warehouse.getWarehouseList ?? []).length
    paginateAside(whPageCount.value, 0)

})

warehouse.fetchWarehousesLatestTomasFisicas().then(it => {
    allWarehousesTableInformation = it.data as WhWithTomaFisica[]
    paginateMain(whPageCount.value, 0)
    showWaitOverlay.value = false
})
*/
</script>

<!--
<template>
    <WaitOverlay :show="showWaitOverlay">
        <ECard>

            <div class="row d-inline-flex allign-content-center tw-bg-slate-50 dark:tw-bg-slate-700">
                <div class="col-2 mx-1 tw-flex-col tw-rounded-lg  tw-bg-white  dark:tw-bg-slate-800 ">

                    <h1 class="title mt-2">Bodegas Disponibles</h1>

                    <b-form class="mt-2 t-form" role="search">

                        <b-form-input class="mt-2" type="search" placeholder="Buscar" aria-label="Search" @change="">

                        </b-form-input>
                    </b-form>

                    <b-pagination v-model="currentAsidePage" :total-rows="whRows" :per-page="whPageCount"
                        aria-controls="b-list-warehouses" align="center" @page-click="onPageChanged" :limit=3
                        hide-goto-end-buttons class="paginator"></b-pagination>


                    <b-list-group :per-page="whPageCount" :current-page="currentAsidePage"
                        class="button-group smaller-btn-group">

                        <b-list-group-item :class="{ active: activeWharehouseButton === -1 }" button
                            @click="showAllWarehouses = true; activeWharehouseButton = -1"> Todas las bodegas
                        </b-list-group-item>
                        <b-list-group-item v-for="wh, index in paginatedWarehouse " button
                            :class="{ active: wh.id === activeWharehouseButton }" :key="wh.id" :id="'whbtn-' + wh.id"
                            @click="wharehouseButtonPressed($event, wh.id, index)">
                            {{ wh.name }}

                        </b-list-group-item>
                    </b-list-group>

                </div>

                <div v-if="showAllWarehouses" class="col-xl tw-bg-slate-50 dark:tw-bg-slate-700">

                    <h1 class="title tw-text-3xl tw-mt-2 mb-2">Bodegas y Últimas Tomas Físicas</h1>

                    <div class="row display-inline-flex">
                        <b-form inline class="col-3" >

                            <b-form-input id="wh-search" placeholder="Busqueda de Bodega">
                            </b-form-input>


                        </b-form>
                        <e-button @click="" type="primary" class=" col-1">Buscar
                        </e-button>

                        <b-pagination v-model="currentMainPage" :total-rows="whRows" :per-page="whPageCount"
                            aria-controls="b-list-warehouses" align="center" @page-click="onMainPageChanged" :limit=10
                            class="paginator col-6 tw-inline-flex"></b-pagination>


                        <e-button @click="" type="primary" class=" col-2">Limpiar filtros
                        </e-button>
                    </div>

                    <BTable :fields="allWarehousesFields" :items="paginatedMainTable" class="text-center">
                        <template #cell(#)="{ index }">
                            {{ index + 1 }}
                        </template>
                        <template #cell(Realizada_Por)="{ item }">
                            {{ (item?.whtf_done_by_name ?? "--") + " " + (item?.whtf_done_by_lastname ?? "--") }}
                        </template>
                        <template #cell(FechaTomaFisica)="{ item }">
                            {{ item.whtf_created_at }}
                        </template>
                        <template #cell(Novedad)="{ item }">
                            {{ truncate(item.whtf_novedad, 15, '...') }}
                        </template>
                        <template #cell(Detalles)="{ item }">

                            <e-button left-icon="fa-eye" @click="" type="primary">Ver detalles
                            </e-button>

                        </template>

                    </BTable>

                </div>


                <div v-else class="col-xl">
                    <div class="row tw-bg-slate-50 dark:tw-bg-slate-700 mt-2">
                        <h1 class="tw-text-3xl tw-font-bold">{{ activeWhInformation.bodega?.name }}</h1>
                    </div>

                    <b-tabs active-tab-class="" content-class="mt-3" pills>

                        <b-tab title="Inventario" active>

                            <ModalDialog v-model:show="itemInfoShow" size="xl">
                                <template #dialog-title>
                                    <b class="tw-text-2xl">Detalle del Ítem {{ detailSelectedItem.item?.name }}</b>
                                </template>
                                <div class="container">
                                    <h3 class="tw-text-xl tw-font-bold">Detalle</h3>
                                    <div class="row tw-pb-3 align-content-center justify-content-center gy-2">
                                        <template v-for="(d, k) in detailSelectedItem.item" :key="k">
                                            <div class="tw-rounded tw-ring-1 tw-ring-slate-500 tw-py-1 col-12 col-md-5 tw-mx-2"
                                                v-if="
                                                    !['category', 'img', 'quantity'].includes(k)
                                                ">
                                                <div class="row">
                                                    <span class="tw-w-1/2 tw-font-bold col-6">{{ k }}:</span>
                                                    <span class="col-6">{{ d }}</span>
                                                </div>
                                            </div>
                                        </template>
                                    </div>
                                    <div v-if="detailSelectedItem.props"
                                        class="tw-ring-1 tw-ring-slate-500 tw-rounded tw-pb-3 row">
                                        <h3 class="col-12 tw-text-xl tw-py-1.5">
                                            <b>Caracteríticas del Ítem</b>
                                        </h3>
                                        <template v-for="(param, idx) in detailSelectedItem.props" :key="idx">
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

                            <BTable id="whinv-table" :fields="inventoryFields" :items="activeWhInformation.inventory"
                                class="table">
                                <template #cell(#)="{ index }">
                                    {{ index + 1 }}
                                </template>
                                <template #cell(P.Venta)="{ item }">
                                    {{ item.price * item.quantity }}
                                </template>
                                <template #cell(Acciones)="{ item, index }">

                                    <e-button left-icon="fa-eye" @click="showItem(item)" type="secondary">Ver detalles
                                    </e-button>

                                </template>
                            </BTable>

                            <b-pagination v-model="currentInvPage" :total-rows="invTableTotal"
                                :per-page="whInformationPerPage" aria-controls="whinv-table" align="center"
                                @page-click="onPageChangedInventory" :limit=10 hide-goto-end-buttons
                                class="paginator"></b-pagination>


                        </b-tab>


                        <b-tab title="Historial de Compras">

                            <BTable :fields="purchasesFields" :items="activeWhInformation.purchases ?? []">
                                <template #cell(#)="{ index }">
                                    {{ index + 1 }}
                                </template>
                                <template #cell(Entregado)="{ purchase }">

                                    <b-icon :icon="choosePurchaseIcon(purchase)"> </b-icon>

                                </template>
                                <template #cell(Acciones)="{ item, index }">

                                    <e-button left-icon="fa-eye" @click="" type="secondary">Ver detalles
                                    </e-button>

                                </template>
                            </BTable>

                        </b-tab>

                        <b-tab title="Toma Física" disabled>


                            <BTable :fields="inventoryFields" :items="activeWhInformation.inventory">
                                <template #cell(#)="{ index }">
                                    {{ index + 1 }}
                                </template>
                                <template #cell(P.Venta)="{ item }">
                                    {{ item.price * item.quantity }}
                                </template>
                                <template #cell(Acciones)="{ item, index }">

                                    <e-button left-icon="fa-eye" @click="showItem(item)" type="secondary">Ver detalles
                                    </e-button>

                                </template>
                            </BTable>

                        </b-tab>

                        <b-tab title="Movimientos">
                            <button type="button" class="btn btn-outline-dark btn-lg">
                                Limpiar Filtros
                            </button>


                        </b-tab>
                    </b-tabs>
                </div>
            </div>
        </ECard>
    </WaitOverlay>
</template>
-->

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
