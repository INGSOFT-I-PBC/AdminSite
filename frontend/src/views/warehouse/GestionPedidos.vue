<script setup lang="ts">
import EButton from '@components/custom/EButton.vue'
import ECard from '@components/custom/ECard.vue'
import { useWarehouseStore } from '@store/warehouse'
import WaitOverlay from '../../components/custom/WaitOverlay.vue'
import { ref } from 'vue'

const showWaitOverlay = ref(true)

const warehouse = useWarehouseStore()

const showAllWarehouses = ref(true)

warehouse.fetchWarehouses().then(it => {
    showWaitOverlay.value = false
})


</script>

<template>
    <WaitOverlay :show="showWaitOverlay">
        <ECard>

            <div class="row d-inline-flex allign-content-center">
                <div class="col-2 mx-1" style="background-color: white">
                    <form class="mt-2" role="search">
                        <input class="form-control me-2" type="search" placeholder="Buscar" aria-label="Search" />
                    </form>

                    <b-list-group>

                        <b-list-group-item active button> Todas las bodegas</b-list-group-item>
                        <b-list-group-item button v-for="wh in warehouse.getWarehouseList ?? []">

                            {{wh.name}}

                        </b-list-group-item>
                    </b-list-group>

                </div>

                <div class="col-md" style="background-color: white; border-radius: 5px">

                    <h1 class="my-1" style="font-size: 35px; color: black">Bodegas disponibles</h1>

                    <EButton class="" >Limpiar Filtros</EButton>

                    <b-form inline>

                        <b-form-input id="wh-search" class=""
                            placeholder="Busqueda de Bodega">
                        </b-form-input>

                    </b-form>

                    <b-table head-variant=light></b-table>
                </div>

                <!-- Specific warehouse card  -->

                <div v-if="!showAllWarehouses" class="col-md" style="background-color: white; border-radius: 5px">
                    <div class="row" style="background-color: white; padding: 10px">
                        <h1 style="font-size: 35px; color: black">Bodega 1</h1>
                    </div>

                    <!--GRUPO DE BOTONES-->
                    <div class="btn-group" role="group" aria-label="Basic radio toggle button group"
                        style="padding: 10px">
                        <input type="radio" class="btn-check" name="btnradio" id="btnInventario" autocomplete="off"
                            checked />
                        <label class="btn btn-outline-dark" for="btnInventario">Inventario</label>

                        <input type="radio" class="btn-check" name="btnradio" id="btnPedidos" autocomplete="off" />
                        <label class="btn btn-outline-dark" for="btnPedidos">Historia Pedidos</label>

                        <input type="radio" class="btn-check" name="btnradio" id="btnTomasF" autocomplete="off" />
                        <label class="btn btn-outline-dark" for="btnTomasF">Tomas Fisicas</label>

                        <input type="radio" class="btn-check" name="btnradio" id="btnMovimientos" autocomplete="off" />
                        <label class="btn btn-outline-dark" for="btnMovimientos">Movimientos</label>
                    </div>

                    <!--DIV DE BOTONES Y NAV-->
                    <div class="container text-center">
                        <div class="row">
                            <div class="col">
                                <button type="button" class="btn btn-outline-dark btn-lg">
                                    Limpiar Filtros
                                </button>
                            </div>

                            <div class="col">
                                <nav class="navbar">
                                    <div class="container-fluid">
                                        <form class="d-flex" role="search">
                                            <input class="form-control me-2" type="search" placeholder="Buscar"
                                                aria-label="Search" />
                                            <button class="btn btn-outline-black" type="submit">
                                                Search
                                            </button>
                                        </form>
                                    </div>
                                </nav>
                            </div>

                            <div class="col">
                                <!--RANGO MIN MAX-->
                                <h6 style="color: black">Rango de stock</h6>
                                <div class="row g-3">
                                    <div class="col">
                                        <input type="text" class="form-control" placeholder="min"
                                            aria-label="First name" />
                                    </div>
                                    <div class="col">
                                        <input type="text" class="form-control" placeholder="max"
                                            aria-label="Last name" />
                                    </div>
                                </div>
                            </div>

                            <div class="col">
                                <button type="button" class="btn btn-outline-dark btn-lg">
                                    Solicitar Nuevo Pedido
                                </button>
                            </div>
                        </div>
                    </div>

                    <!--TABLA DE BODEGAS-->
                    <div class="container" style="background-color: white">
                        <table class="table table-bordered">
                            <thead class="table-dark">
                                <tr>
                                    <th scope="col">Código del Producto</th>
                                    <th scope="col">Descripcion del Producto</th>
                                    <th scope="col">Stock</th>
                                    <th scope="col">Costo</th>
                                    <th scope="col">P.Venta</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <th>GST00236</th>
                                    <td>Calentador Nike</td>
                                    <td>10</td>
                                    <td>$35.06</td>
                                    <td>$37.06</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>
        </ECard>
    </WaitOverlay>
</template>
