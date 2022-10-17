<script setup lang="ts">
import EButton from '@components/custom/EButton.vue'
import ECard from '@components/custom/ECard.vue'
import { useWarehouseStore } from '@store/warehouse'
import WaitOverlay from '../../components/custom/WaitOverlay.vue'
import type { Warehouse, WarehouseQuery } from '/../store/models/warehouseModels'
import { ref } from 'vue'

const showWaitOverlay = ref(true)

const whPageCount = ref(15)
let currentPage = ref(1)
let whRows = ref(0)
let paginatedWarehouse = ref()
let searchInput = ref("")
const showAllWarehouses = ref(true)
let activeWharehouse = ref(-1)

const warehouse = useWarehouseStore()

function paginate(page_size: number, page_number: number) {

    let itemsToParse = warehouse.getWarehouseList ?? []

    paginatedWarehouse.value = itemsToParse.slice(
        page_number * page_size,
        (page_number + 1) * page_size
    );
}

function filteredList() {
    return (warehouse.getWarehouseList ?? []).filter((warehouse) =>
        warehouse.name.toLowerCase().includes(searchInput.value.toLowerCase())
    );
}

function onPageChanged(event: any, page: number) {
    paginate(whPageCount.value, page - 1);
}

function wharehouseButtonPressed(event: any, whId: number) {
    showAllWarehouses.value = false

    activeWharehouse.value = whId

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

                        <b-list-group-item :class="{ active: activeWharehouse === -1}" button
                            @click="showAllWarehouses = true;activeWharehouse= -1"> Todas las bodegas
                        </b-list-group-item>
                        <b-list-group-item v-for="wh, index in paginatedWarehouse " button
                            :class="{ active: wh.id === activeWharehouse}" :key="wh.id" :id="'whbtn-' + wh.id"
                            @click="($event)=> { wharehouseButtonPressed($event,wh.id)}">
                            {{wh.name}}

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

                </div>

                <!-- Specific warehouse card  -->

                <div v-else class="col-md" style="background-color: white; border-radius: 5px">
                    <div class="row" style="background-color: white; padding: 10px">
                        <h1 style="font-size: 35px; color: black">Bodega 1</h1>
                    </div>

                    <b-tabs active-tab-class="" content-class="mt-3" pills>

                        <b-tab title="Inventario" active>

                            <button type="button" class="btn btn-outline-dark btn-lg">
                                Limpiar Filtros
                            </button>


                        </b-tab>

                        <b-tab title="Historial de Pedidos">

                            <button type="button" class="btn btn-outline-dark btn-lg">
                                Limpiar Filtros
                            </button>


                        </b-tab>

                        <b-tab title="Toma Física" disabled>
                            <!-- TODO cuando esten las migraciones-->


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
