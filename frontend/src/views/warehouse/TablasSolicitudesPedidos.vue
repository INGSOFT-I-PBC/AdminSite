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
    import type {
        Item2,
        ItemProps,
        ProviderProductDetails,
    } from '@store/types/items.model'
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
    const itemInfoShow3 = ref(false)
    const itemInfoShow4 = ref(false)
    const itemInfoShow5 = ref(false)
    const itemInfoShow6 = ref(false)
    const itemInfoShow7 = ref(false)

    type SelectedItem = { item: OrderDetails2 | null }
    const detailSelectedItem = ref<SelectedItem>({
        item: null,
    })
    const itemId = ref<string>('')
    const price = ref<string>('')
    const quantity = ref<string>('')
    const varnt = ref<string>('')

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
        //ordersDetails2: { item: Item; quantity: number }[]
        //ordersDetails2: { item: Item2; quantity: number }[]
        ordersDetails2?: Item2[]
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
        'Acciones',
    ]

    const formProvider: TableField[] = [
        '#',
        'Producto',
        'NombreProveedor',
        'Direccion',
        'Email',
        'Precio',
        'Acciones',
    ]

    type providerDetails = {
        productProviderDetails: ProviderProductDetails[]
    }

    const activeProductProviderInformations = ref<providerDetails>({
        productProviderDetails: [],
    })

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
        ordersDetails2: [],
    })

    type FilterOption = {
        label: string
        value: 'producto' | 'marca'
    }
    const filterOption = ref<FilterOption[]>([
        { label: 'Producto', value: 'producto' },
        { label: 'Marca', value: 'marca' },
    ])

    const filterName = ref(filterOption.value[0])
    const filterText = ref<string>('')
    const cantStock = ref<string>('')

    const numeroruta = route.params.id

    async function ProviderProductTable() {
        const response = await warehouse.fetchProviderProduct()
        console.log(response)

        activeProductProviderInformations.value.productProviderDetails =
            response.data
        console.log(
            activeProductProviderInformations.value.productProviderDetails
        )
    }

    ProviderProductTable()

    //let ordenes = ref(<arr_ordens>{})

    async function OrderDetailsTable() {
        showWaitOverlay.value = true
        const busqueda = filterText.value != '' ? filterText.value : ''
        const filtro = filterName.value.value

        const response = await warehouse.fetchOrdersDetails(
            Number(route.params.id),
            null,
            busqueda,
            filtro
        )
        console.log(response)

        activeWhInformation.value.ordersDetails2 = response.data
        //console.log( 'data',activeWhInformation.value.ordersDetails2.data[0].item)

        console.log(activeWhInformation.value.ordersDetails2 == undefined)

        /*
        if (activeWhInformation.value == undefined) return
        activeWhInformation.value.ordersDetails2 = response.data
        console.log(response.data)
        console.log(activeWhInformation.value.ordersDetails2)
        */
        showWaitOverlay.value = false
    }

    OrderDetailsTable()

    function goEdit(id: number): void {
        console.log(id)
        router.push({ path: `/usuarios/cliente/editar/${String(id)}` })
    }

    async function SolicitudAceptada(items: OrderDetails2, id: any) {
        detailSelectedItem.value.item = items
        itemId.value = id
        itemInfoShow.value = true
    }

    async function AceptarRechazar(item: OrderDetails2) {
        detailSelectedItem.value.item = item
        itemInfoShow.value = true
    }

    async function ActualizarStock(item: any) {
        const stockProduct = item.quantity
        console.log(stockProduct)

        if (stockProduct != null) {
            itemId.value = item['item'].id
            cantStock.value = stockProduct
            itemInfoShow5.value = true
        }
    }

    async function StockWindow() {
        itemInfoShow4.value = true
    }

    async function datos() {
        console.log(activeWhInformation.value?.ordersDetails2)
        console.log()
    }

    async function traerDatos(event: any, index: number) {
        console.log(event)
        if (activeWhInformation.value == undefined) return
        //activeWhInformation.value.ordersDetails2[index].item.price = event
        console.log(activeWhInformation.value.ordersDetails2)
    }

    async function getQuantity(event: any) {
        //console.log(event)
        quantity.value = event
        //console.log(event)
        if (quantity.value != null) {
            //itemInfoShow4.value = true
        }
        console.log(itemId.value)
        console.log(quantity.value)
    }

    async function getPrice(event: any) {
        price.value = event.price
        if (price.value != null) {
            itemInfoShow3.value = true
        }
        console.log(itemId.value)
        console.log(price.value)
    }

    async function guardarprecioitem(event: any) {
        const response = await warehouse.savePriceToItem(
            null,
            itemId.value,
            price.value
        )
        console.log(response)
        itemInfoShow3.value = false
        itemInfoShow.value = false
        OrderDetailsTable()
        //location.reload()
    }

    /**/
    async function guardarcantidaditem(event: any) {
        const response = await warehouse.saveQuantityToItem(
            null,
            itemId.value,
            cantStock.value
        )
        console.log(response)
        //itemInfoShow4.value = false
        itemInfoShow4.value = false
        itemInfoShow5.value = false
        OrderDetailsTable()
        //location.reload()
    }

    async function aprobarCompra(event: any, type: any, id = 0) {
        if (type == 1) {
            itemInfoShow7.value = true
        }
        if (type == 3) {
            itemInfoShow7.value = false
        }
        if (type == 2) {
            console.log(id)
            const response = await warehouse.approvePurchase(null, id)
        }
    }

    async function GenerarInforme(event: any) {
        itemInfoShow6.value = true
    }
</script>

<template>
    <main>
        <!---->
        <ModalDialog v-model:show="itemInfoShow" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl">
                    <!--
                    <InputText v-model="filterText" label="Codigo Producto" readonly="true" />-->
                    Lista de proveedores
                    {{ detailSelectedItem.item?.warehouse }}
                </b>
            </template>
            <div class="container">
                <p>
                    Seleccione el proveedor con el cual quiere realizar la
                    compra del item
                </p>
                <br />

                <BTable
                    :fields="formProvider"
                    :items="
                        activeProductProviderInformations?.productProviderDetails
                    "
                    class="table text-center text-bg-dark"
                    id="whinv-table"
                    style="border-radius: 5px">
                    <template #cell(#)="{ index }">{{ index + 1 }} </template>

                    <template #cell(Producto)="{ item }">
                        {{ item['product'].short_description }}
                    </template>

                    <template #cell(NombreProveedor)="{ item }">
                        {{ item['provider'].name }}
                    </template>

                    <template #cell(Direccion)="{ item }">
                        {{ item['provider'].address }}
                    </template>

                    <template #cell(Email)="{ item }">
                        {{ item.provider.email }}
                    </template>

                    <template #cell(Precio)="{ item }">
                        {{ item.price }}
                    </template>

                    <template #cell(Acciones)="{ item }">
                        <div class="t-button-group">
                            <e-button
                                left-icon="check"
                                type="button"
                                @click="getPrice(item)"
                                >Seleccionar</e-button
                            >
                        </div>
                    </template>
                </BTable>

                <!--
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
                -->
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

        <ModalDialog v-model:show="itemInfoShow3" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl">Ventana de confirmacion </b>
            </template>
            <div class="container">
                <p>Estas seguro de realizar los cambios?</p>

                <br />
                <div style="spacing = 100">
                    <e-button
                        left-icon="check"
                        type="button"
                        @click="guardarprecioitem($event)"
                        >Aceptar</e-button
                    >
                    &nbsp;
                    <e-button left-icon="" type="button">Rechazar</e-button>
                </div>
            </div>
        </ModalDialog>

        <ModalDialog v-model:show="itemInfoShow4" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl">Ventana de confirmación </b>
            </template>
            <div class="container">
                <p>Estas seguro de realizar los cambios?</p>

                <br />
                <div style="spacing = 100">
                    <e-button
                        left-icon="check"
                        type="button"
                        @click="guardarcantidaditem($event)"
                        >Aceptar</e-button
                    >
                    &nbsp;
                    <e-button left-icon="" type="button">Rechazar</e-button>
                </div>
            </div>
        </ModalDialog>

        <ModalDialog v-model:show="itemInfoShow5" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl">Cambio del numero de stock </b>
            </template>
            <div class="container">
                <p>Coloque la cantidad que desea solicitar</p>

                <br />
                <div style="spacing = 100">
                    <div class="container">
                        <InputText v-model="cantStock" />
                        <!--<b-form-input
                                    class="w-25 text-center"
                                    type="number"
                                    min="0"
                                    @input="getQuantity($event)"
                                    debounce="400">
                                </b-form-input>-->
                    </div>

                    &nbsp; &nbsp;
                    <div class="container">
                        <e-button
                            left-icon=""
                            type="button"
                            @click="StockWindow()">
                            Guardar</e-button
                        >
                    </div>
                </div>
            </div>
        </ModalDialog>

        <ModalDialog v-model:show="itemInfoShow6" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl">Informe Orden Compra </b>
            </template>
            <div class="container">
                <p>Detalles de la orden de compra</p>

                <br />

                <ul>
                    <li>Aprovado en:</li>
                    <li>Numero de compra:</li>
                    <li>Numero de orden:</li>
                    <li>Nombre de proveedor:</li>
                    <li>Nombre de bodega:</li>
                </ul>
            </div>
        </ModalDialog>

        <ModalDialog v-model:show="itemInfoShow7" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl">Ventana de confirmacion </b>
            </template>
            <div class="container">
                <p>
                    Estas seguro de aprobar la compra, la misma no se podra
                    actualizar luego de la transaccion?
                </p>

                <br />
                <div style="spacing = 100">
                    <e-button
                        left-icon="check"
                        type="button"
                        @click="aprobarCompra($event, 2, Number(numeroruta))"
                        >Aceptar</e-button
                    >
                    &nbsp;
                    <e-button
                        @click="aprobarCompra($event, 3)"
                        left-icon=""
                        type="button"
                        >Rechazar</e-button
                    >
                </div>
            </div>
        </ModalDialog>

        <div
            class="container"
            style="background-color: rgb(60, 60, 60); border-radius: 10px">
            <div>
                <b-container fluid>
                    <div
                        class="container"
                        style="
                            background-color: rgb(60, 60, 60);
                            border-radius: 5px;
                        ">
                        <b-row>
                            <b-col lg="4" class="my-1">
                                <ListBox
                                    :clearable="true"
                                    v-model="filterName"
                                    top-label="Filtrar por:"
                                    :options="filterOption" />
                            </b-col>
                            <b-col lg="4" class="my-1">
                                <InputText
                                    v-model="filterText"
                                    label="Cuadro de búsqueda"
                                    :placeholder="`Búsqueda por ${filterName.label}`" />
                            </b-col>

                            <b-col lg="4" class="my-1">
                                <EButton
                                    style="
                                        margin-top: 34px;
                                        margin-bottom: 10px;
                                    "
                                    class="tw-min-w-full"
                                    @click="OrderDetailsTable"
                                    >Buscar</EButton
                                >
                            </b-col>
                        </b-row>
                    </div>

                    <!---->
                    <WaitOverlay :show="showWaitOverlay"></WaitOverlay>
                    <BTable
                        :fields="formFields"
                        :items="activeWhInformation?.ordersDetails2"
                        class="table text-center text-bg-dark"
                        id="whinv-table"
                        style="border-radius: 10px">
                        <template #cell(#)="{ index }"
                            >{{ index + 1 }}
                        </template>

                        <!---->
                        <template #cell(CodigoProducto)="{ item }">
                            {{ item['item'].id }}
                        </template>

                        <template #cell(NombreProducto)="{ item }">
                            {{ item['item'].product_name }}
                        </template>

                        <template #cell(Precio)="{ item }">
                            {{ item.item.price }}
                        </template>

                        <!---->
                        <template #cell(Stock)="{ item }">
                            {{ item.quantity }}
                        </template>

                        <template #cell(Marca)="{ item }">
                            {{ item.item.brand_name }}
                        </template>

                        <template #cell(Modelo)="{ item }">
                            {{ item.item.variant_name }}
                        </template>

                        <template #cell(Acciones)="{ item }">
                            <div class="t-button-group">
                                <e-button
                                    left-icon="check"
                                    type="button"
                                    @click="
                                        SolicitudAceptada(item, item.item.id)
                                    "
                                    >Actualizar Precio</e-button
                                >
                                &nbsp;
                                <!---->
                                <e-button
                                    left-icon=""
                                    type="button"
                                    @click="ActualizarStock(item)">
                                    <span
                                        class="tw-invisible md:tw-visible tw-font-bold"
                                        >Actualizar Stock</span
                                    ></e-button
                                >
                                &nbsp;
                                <e-button
                                    left-icon=""
                                    type="button"
                                    @click="GenerarInforme($event)">
                                    <span
                                        class="tw-invisible md:tw-visible tw-font-bold"
                                        >Informe</span
                                    ></e-button
                                >
                            </div>
                        </template>
                    </BTable>

                    <e-button
                        style="margin-bottom: 20px"
                        left-icon=""
                        type="button"
                        @click="aprobarCompra($event, 1)">
                        <span class="tw-invisible md:tw-visible tw-font-bold"
                            >Aprobar Compra</span
                        ></e-button
                    >
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
