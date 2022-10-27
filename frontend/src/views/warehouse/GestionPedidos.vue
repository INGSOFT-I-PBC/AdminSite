<script setup lang="ts">
import EButton from '@components/custom/EButton.vue'
import ECard from '@components/custom/ECard.vue'
import type { TableField } from 'bootstrap-vue-3'
import ModalDialog from '../../components/custom/ModalDialog.vue'
import { useWarehouseStore } from '@store/warehouse'
import { useItemStore } from '@/store'
import WaitOverlay from '../../components/custom/WaitOverlay.vue'
import { ref } from 'vue'
import { type Item, type Warehouse, type Purchase, type TomaFisica } from '@store/types'
import { table } from 'console'
import type { ItemProps } from '@store/types/items.model'

type SelectedItem = { item: Item | null; props: ItemProps[] }
type QuantifiedItem = Item & { quantity: number }
type warehouseInformation = {
    bodega?: Warehouse
    inventory?: QuantifiedItem[]
    purchases?: Purchase[]
    tomasFisicas?: TomaFisica[]
    movements?: []
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
    { label: 'Fecha Creación', key: 'codename' },
    { label: 'Codigo Orden', key: 'reference' },
    { label: 'Proveedor', key: 'proveedor' },
    { label: 'Fecha Completada', key: 'completed_at' },
    'Entregado',
    { label: 'Pago', key: 'invoice' },
    { label: 'Fecha Pago', key: 'paid_at'},
    'Acciones',
]

const toamsFisFields: TableField[] = [
    '#',
    { label: 'Fecha Realizacion', key: 'created_at' },
    { label: 'Realizda por', key: 'employee_name' },
    { label: 'Novedad', key: 'novedad' },
    'Acciones',
]

let activeWhInformation = ref(<warehouseInformation>{
    id: 0,
    name: '',
    status: {
        description: '',
        name: '',
        id: ''
    }
}
)


let currentPage = ref(1)
let whRows = ref(0)
let paginatedWarehouse = ref()
let searchInput = ref("")
let activeWharehouseButton = ref(-1)

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


function paginate(page_size: number, page_number: number) {

    let itemsToParse = warehouse.getWarehouseList ?? []

    paginatedWarehouse.value = itemsToParse.slice(
        page_number * page_size,
        (page_number + 1) * page_size
    );
}

function onPageChanged(event: any, page: number) {
    //Loading tru
    //fetch => paginiatedWarehouse
    //
    paginate(whPageCount.value, page - 1);
}

function resetInvData() {

    invTableTotal.value, tomasFisTableTotal.value, purchaseTableTotal.value, movementTableTotal.value  = 1
    currentInvPage.value, currentTomasFisicasPage.value, currentPurchasePage.value , currentMovPage.value = 1

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

async function onPageChangedTomaFisicas(event:any , page:number){

    showWaitOverlay.value = true

    let wh_id = activeWhInformation.value.bodega.id

    let response = await warehouse.fetchPaginatedWarehousesTomasFisicas(
        { id: wh_id }, { page: page, per_page: whInformationPerPage.value }
    )

    activeWhInformation.value.tomasFisicas = response.data.data

    tomasFisTableTotal.value = response.data.total

    showWaitOverlay.value = false

}

async function onPageChangedPurchase(event:any,page:number){

    showWaitOverlay.value = true

    let wh_id = activeWhInformation.value.bodega.id

    let response = await warehouse.fetchPaginatedWarehousesPurchase(
        { id: wh_id }, { page: page, per_page: whInformationPerPage.value }
    )

    activeWhInformation.value.purchases = response.data.data

    purchaseTableTotal.value = response.data.total

    showWaitOverlay.value = false

}

// async function onPageChangedMovements(event:any,page:number){

//     showWaitOverlay.value = true

//     let wh_id = activeWhInformation.value.bodega.id

//     let response = await warehouse.fetchPaginatedWarehousesMovements(
//         { id: wh_id }, { page: page, per_page: whInformationPerPage.value }
//     )

//     activeWhInformation.value.movements = response.data.data

//     movementTableTotal.value = response.data.total

//     showWaitOverlay.value = false

// }


function wharehouseButtonPressed(event: any, whId: number, index: number) {

    showAllWarehouses.value = false

    activeWharehouseButton.value = whId

    activeWhInformation.value.bodega = (warehouse.getWarehouseList[index] ?? { name: 'Error' })

    showWaitOverlay.value = true

    resetInvData()

    onPageChangedInventory(event, 1).then(() => {
        showWaitOverlay.value = false
    })

    onPageChangedTomaFisicas(event, 1)

    onPageChangedPurchase(event, 1)

    //onPageChangeMovement(event,1)

}

async function showItem(item: Item) {
    detailSelectedItem.value.item = item
    console.log(item)
    itemInfoShow.value = true
    detailSelectedItem.value.props = await itemStore.fetchItemProperties(
        item.id
    )

}

warehouse.fetchWarehouses().then(it => {

    whRows.value = (warehouse.getWarehouseList ?? []).length

    paginate(whPageCount.value, 0)

    showWaitOverlay.value = false

})

</script>

<template>
    <WaitOverlay :show="showWaitOverlay">
        <ECard>

            <div class="row d-inline-flex allign-content-center">
                <div class="col-2 mx-1" style="background-color: white">

                    <h2 class="mt-2">Bodegas Disponibles</h2>

                    <b-form class="mt-2" role="search">

                        <b-form-input class="form-control me-2" type="search" placeholder="Buscar" aria-label="Search"
                            @change="">

                        </b-form-input>
                    </b-form>

                    <b-pagination v-model="currentPage" :total-rows="whRows" :per-page="whPageCount"
                        aria-controls="b-list-warehouses" align="center" @page-click="onPageChanged" :limit=3
                        hide-goto-end-buttons></b-pagination>


                    <b-list-group :per-page="whPageCount" :current-page="currentPage">

                        <b-list-group-item :class="{ active: activeWharehouseButton === -1 }" button
                            @click="showAllWarehouses = true; activeWharehouseButton = -1"> Todas las bodegas
                        </b-list-group-item>
                        <b-list-group-item v-for="wh, index in paginatedWarehouse " button
                            :class="{ active: wh.id === activeWharehouseButton }" :key="wh.id" :id="'whbtn-' + wh.id"
                            @click="($event: any) => { wharehouseButtonPressed($event, wh.id, index) }">
                            {{ wh.name }}

                        </b-list-group-item>
                    </b-list-group>

                </div>

                <div v-if="showAllWarehouses" class="col-md" style="background-color: white; border-radius: 5px">

                    <h1 class="my-1" style="font-size: 35px; color: black">Bodegas disponible</h1>

                    <EButton class="">Limpiar Filtros</EButton>

                    <b-form inline>

                        <b-form-input id="wh-search" class="" placeholder="Busqueda de Bodega">
                        </b-form-input>

                    </b-form>

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

                </div>

                <!-- Specific warehouse card  -->

                <div v-else class="col-md" style="background-color: white; border-radius: 5px">
                    <div class="row" style="background-color: white; padding: 10px">
                        <h1 style="font-size: 35px; color: black">{{ activeWhInformation.bodega?.name }}</h1>
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

                            <BTable id = "whinv-table" :fields="inventoryFields" :items="activeWhInformation.inventory">
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
                                @page-click="onPageChangedInventory" :limit=10 hide-goto-end-buttons></b-pagination>


                        </b-tab>

                        <!--  Historial de pedidos TAB    -->

                        <b-tab title="Historial de Pedidos">


                        </b-tab>

                        <b-tab title="Toma Física" disabled>
                            <!-- TODO cuando esten las migraciones-->

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
