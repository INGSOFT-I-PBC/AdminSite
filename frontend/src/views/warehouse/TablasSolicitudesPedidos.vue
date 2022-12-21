<script setup lang="ts">
    //import type { Warehouse } from '@store/types';
    import EButton from '@components/custom/EButton.vue'
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
        OrderDetails,
        OrderDetails2,
        OrderSaveData,
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
    import type { AnyARecord } from 'dns'

    import { useRoute, useRouter } from 'vue-router'

    import WaitOverlay from '../../components/custom/WaitOverlay.vue'

    const router = useRouter()
    const route = useRoute()
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
    const itemInfoShow2 = ref(false)

    type SelectedItem = { item: OrderDetails2 | null }
    const detailSelectedItem = ref<SelectedItem>({
        item: null,
    })

    type QuantifiedItem = Item & { quantity: number }

    const form = ref<Form>({
        items: [],
    })

    type Form = {
        items: []
    }

    //comentario
    type arr_ordens = {
        /*
        nameWarehouse: number
        fechaPedido: string
        solicitadoPor: string
        estado: string
        elementos: []
        */
    }

    type warehouseInformation = {
        bodega: Warehouse
        inventory: QuantifiedItem[]
        purchases: Purchase[]
        tomasFisicas: TomaFisica[]
        movements: []
        //ordersDetails: OrderDetails[]
        ordersDetails2: { item: Item; quantity: number }[]
    }

    const formFields: TableField[] = [
        '#',
        'CodigoProducto',
        'NombreProducto',
        'Precio',
        'Stock',
        //{ label: 'NombreProducto', key: 'item.name' },
        //{ label: 'Stock', key: 'quantity' },
        //{ label: 'Precio', key: 'item.price' },
        'Marca',
        'Modelo',
        'Categoria',
        'Estado',
        'Acciones',
    ]

    type orderDetailsElements = {
        id: number
        inventory: QuantifiedItem[]
        purchases: Purchase[]
        tomasFisicas: TomaFisica[]
        movements: []
        ordersDetails: OrderDetails[]
    }

    const activeWhInformation = ref<warehouseInformation>()
    //let ordenes = ref(<arr_ordens>{})

    async function OrderDetailsTable() {
        showWaitOverlay.value = true

        const response = await warehouse.fetchOrdersDetails(
            Number(route.params.id)
        )
        if (activeWhInformation.value == undefined) return
        activeWhInformation.value.ordersDetails2 = response.data
        console.log(response.data)
        console.log(activeWhInformation.value.ordersDetails2)
        showWaitOverlay.value = false
    }

    OrderDetailsTable()

    function goEdit(id: number): void {
        console.log(id)
        router.push({ path: `/usuarios/cliente/editar/${String(id)}` })
    }

    async function SolicitudAceptada(item: OrderDetails2) {
        detailSelectedItem.value.item = item
        itemInfoShow.value = true
    }

    async function SolicitudRechazada(item: OrderDetails2) {
        detailSelectedItem.value.item = item
        itemInfoShow2.value = true
    }

    async function datos() {
        console.log(activeWhInformation.value?.ordersDetails2)
        console.log()
    }

    async function traerDatos(event: any, index: number) {
        console.log(event)
        if (activeWhInformation.value == undefined) return
        activeWhInformation.value.ordersDetails2[index].item.price = event
        console.log(activeWhInformation.value.ordersDetails2)
    }

    async function getQuantity(event: any, index: number) {
        console.log(event)
        if (activeWhInformation.value == undefined) return
        activeWhInformation.value.ordersDetails2[index].quantity = event
        console.log(activeWhInformation.value.ordersDetails2)
    }
</script>

<template>
    <main>
        <!---->
        <ModalDialog v-model:show="itemInfoShow" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl"
                    >Detalle De Orden De Pedidos
                    {{ detailSelectedItem.item?.warehouse }}</b
                >
            </template>
            <div class="container">
                <p>
                    Se ha aceptado la solicitud de pedidos presione OK para
                    confirmar
                </p>
                <!---->
                <div
                    class="row tw-pb-3 align-content-center justify-content-center gy-2">
                    <template
                        v-for="(d, k) in detailSelectedItem.item"
                        :key="k">
                        <div class="row" v-if="k == 'cantidad'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Cantidad:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'status'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Estado:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                    </template>
                </div>
            </div>
        </ModalDialog>

        <ModalDialog v-model:show="itemInfoShow2" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl"
                    >Detalle De Orden De Pedidos
                    {{ detailSelectedItem.item?.warehouse }}</b
                >
            </template>
            <div class="container">
                <p>
                    Se ha rechazado la solicitud de pedidos presione OK para
                    confirmar
                </p>
                <!---->
                <div
                    class="row tw-pb-3 align-content-center justify-content-center gy-2">
                    <template
                        v-for="(d, k) in detailSelectedItem.item"
                        :key="k">
                        <div class="row" v-if="k == 'cantidad'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Cantidad:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'status'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Estado:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                    </template>
                </div>
            </div>
        </ModalDialog>

        <div
            class="container"
            style="background-color: rgb(60, 60, 60); border-radius: 10px">
            <div>
                <b-container fluid>
                    <b-row>
                        <b-col lg="6" class="my-1"> </b-col>
                    </b-row>

                    <!---->
                    <WaitOverlay :show="showWaitOverlay"></WaitOverlay>
                    <BTable
                        :fields="formFields"
                        :items="activeWhInformation?.ordersDetails2"
                        class="table text-center text-bg-dark"
                        id="whinv-table"
                        style="border-radius: 5px">
                        <template #cell(#)="{ index }"
                            >{{ index + 1 }}
                        </template>
                        <template #cell(CodigoProducto)="{ item }">
                            {{ item.item.codename }}
                        </template>

                        <template #cell(NombreProducto)="{ item }">
                            {{ item.item.name }}
                        </template>

                        <template #cell(Precio)="{ item, index }">
                            {{ item.item.price }}

                            <div
                                align="center"
                                style="margin-top: 10px; margin-bottom: 10px"
                                class="align-content-center">
                                <b-form-input
                                    class="w-25 text-center"
                                    type="number"
                                    :v-model="item.item.price"
                                    min="0"
                                    :value="item.item.price"
                                    @input="traerDatos($event, index)"
                                    debounce="400">
                                </b-form-input>
                            </div>

                            <e-button
                                left-icon="fa-edit"
                                type="button"
                                @click.left="datos()"
                                >Editar</e-button
                            >
                        </template>
                        <template #cell(Stock)="{ item, index }">
                            {{ item.quantity }}
                            <div
                                align="center"
                                style="margin-top: 10px; margin-bottom: 10px"
                                class="align-content-center">
                                <b-form-input
                                    class="w-25 text-center"
                                    type="number"
                                    :v-model="item.quantity"
                                    min="0"
                                    :value="item.quantity"
                                    @input="getQuantity($event, index)"
                                    debounce="400">
                                </b-form-input>
                            </div>
                        </template>
                        <template #cell(Marca)="{ item }">
                            {{ item.item.brand }}
                        </template>
                        <template #cell(Modelo)="{ item }">
                            {{ item.item.model }}
                        </template>
                        <template #cell(Categoria)="{ item }">
                            {{ item.item.category.name }}
                        </template>
                        <template #cell(Estado)="{ item }">
                            {{ item.item.status.name }}
                        </template>

                        <template #cell(Acciones)="{ item }">
                            <div class="t-button-group">
                                <e-button
                                    left-icon="check"
                                    type="button"
                                    @click="SolicitudAceptada(item)"
                                    >Aceptar</e-button
                                >
                                <!---->
                                <e-button
                                    left-icon=""
                                    type="button"
                                    @click="SolicitudRechazada(item)">
                                    <span
                                        class="tw-invisible md:tw-visible tw-font-bold"
                                        >Rechazar</span
                                    ></e-button
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
