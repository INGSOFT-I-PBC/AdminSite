<script setup lang="ts">
    import { useItemStore } from '@/store'
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import type { WarehouseQuery } from '@store/models/warehouseModels'
    import {
        type Item,
        type Movement,
        type Purchase,
        type TomaFisica,
        type Warehouse,
        type WhWithTomaFisica,
    } from '@store/types'
    import type { ItemProps } from '@store/types/items.model'
    import { useWarehouseStore } from '@store/warehouse'
    import {
        BForm,
        BFormCheckbox,
        BFormInput,
        BListGroup,
        BListGroupItem,
        BPagination,
        BTab,
        BTable,
        BTabs,
        type TableField,
    } from 'bootstrap-vue-3'

    import ModalDialog from '../../components/custom/ModalDialog.vue'
    import WaitOverlay from '../../components/custom/WaitOverlay.vue'

    type SelectedItem = { item: Item | null; props: ItemProps[] }
    type QuantifiedItem = Item & { quantity: number }

    type whCardController = {
        currentPage: number
        totalRows: number
        searchInput: string
    }

    type warehouseInformation = {
        bodega: Warehouse
        inventory: QuantifiedItem[]
        purchases: Purchase[]
        tomasFisicas: TomaFisica[]
        movements: Movement[]
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
        'FechaTomaFisica',
        'RealizadaPor',
        'Novedad',
        'Detalles',
    ]

    const inventoryFields: TableField[] = [
        '#',
        { label: 'Codigo Producto', key: 'codename' },
        { label: 'Nombre Producto', key: 'name' },
        { label: 'Stock', key: 'quantity' },
        { label: 'Precio', key: 'price' },
        'PVenta',
        'Acciones',
    ]

    const purchasesFields: TableField[] = [
        '#',
        'FechaCreación',
        { label: 'Codigo Orden', key: 'reference' },
        'Proveedor',
        'Entregado',
        'Pago',
        'FechaPago',
        'Acciones',
    ]

    const tomasFisFields: TableField[] = [
        '#',
        'FechaRealizacion',
        'RealizadaPor',
        { label: 'Novedad', key: 'novedad' },
        'Acciones',
    ]

    const movementsFields: TableField[] = [
        '#',
        'Creada',
        'RealizadaPor',
        'BodegaRelacionada',
        'TipoDeMovimiento',
        { label: 'Estado', key: 'status' },
        'Notas',
    ]

    let allWarehousesTableInformation: WhWithTomaFisica[] = []

    const currentAsidePage = ref(1)
    const whRows = ref(0)
    const paginatedWarehouse = ref()
    const activeWharehouseButton = ref(-1)

    const paginatedMainTable = ref()

    const mainPageController = ref<whCardController>({
        currentPage: 1,
        totalRows: whRows.value,
        searchInput: ' ',
    })

    const activeWhInformation = ref<warehouseInformation>({})

    const invTabController = ref<whCardController>({
        currentPage: 1,
        totalRows: 15,
        searchInput: ' ',
    })

    const tomasFisicasTabController = ref<whCardController>({
        currentPage: 1,
        totalRows: 15,
        searchInput: ' ',
    })

    const purchaseTabController = ref<whCardController>({
        currentPage: 1,
        totalRows: 15,
        searchInput: ' ',
    })

    const movementTabController = ref<whCardController>({
        currentPage: 1,
        totalRows: 15,
        searchInput: ' ',
    })

    const arrayControllers = [
        invTabController.value,
        tomasFisicasTabController.value,
        purchaseTabController.value,
        movementTabController.value,
    ]

    const itemInfoShow = ref(false)

    function paginateAside(page_size: number, page_number: number) {
        paginatedWarehouse.value = (warehouse.getWarehouseList ?? []).slice(
            page_number * page_size,
            (page_number + 1) * page_size
        )
    }

    function onAsidePageChanged(event: Event, page: number) {
        paginateAside(whPageCount.value, page - 1)
    }

    function paginateMain(page_size: number, page_number: number) {
        paginatedMainTable.value = allWarehousesTableInformation.slice(
            page_number * page_size,
            (page_number + 1) * page_size
        )
    }

    function onMainPageChanged(event: Event, page: number): void {
        paginateMain(whPageCount.value, page - 1)
    }

    function resetInvData(): void {
        for (const controller of arrayControllers) {
            ;(controller.currentPage = 1),
                (controller.totalRows = 1),
                (controller.searchInput = ' ')
        }
    }

    async function fetchManager(
        tabOption: string,
        query: WarehouseQuery,
        paginated_opt: PaginationOptions
    ): Promise<void> {
        switch (tabOption) {
            case 'inventory': {
                const res = await warehouse.fetchPaginatedWarehouseInventory(
                    query,
                    paginated_opt
                )
                activeWhInformation.value.inventory = res.data.data
                invTabController.value.totalRows = res.data.total
                break
            }
            case 'purchases': {
                const res = await warehouse.fetchPaginatedWarehousePurchase(
                    query,
                    paginated_opt
                )
                activeWhInformation.value.purchases = res.data.data
                purchaseTabController.value.totalRows = res.data.total
                break
            }
            case 'tomas-fisicas': {
                const res = await warehouse.fetchPaginatedWarehouseTomasFisicas(
                    query,
                    paginated_opt
                )
                activeWhInformation.value.tomasFisicas = res.data.data
                tomasFisicasTabController.value.totalRows = res.data.total
                break
            }
            case 'movements': {
                const res = await warehouse.fetchPaginatedWarehouseMovements(
                    query,
                    paginated_opt
                )
                activeWhInformation.value.movements = res.data.data
                movementTabController.value.totalRows = res.data.total
                break
            }
        }
    }

    async function onReset(
        controller: whCardController,
        tabOption: string
    ): Promise<void> {
        showWaitOverlay.value = true

        await fetchManager(
            tabOption,
            { id: activeWhInformation.value.bodega.id },
            { page: 1, per_page: whInformationPerPage.value }
        )

        controller.searchInput = ' '
        controller.currentPage = 1

        showWaitOverlay.value = false
    }

    async function onPageChanged(
        tabOption: string,
        controller: whCardController
    ) {
        showWaitOverlay.value = true

        const pageOpt = {
            page: controller.currentPage,
            per_page: whInformationPerPage.value,
        }

        await fetchManager(
            tabOption,
            { id: activeWhInformation.value.bodega.id },
            pageOpt
        )

        showWaitOverlay.value = false
    }

    function wharehouseButtonPressed(
        event: Event,
        whId: number,
        index: number
    ) {
        showAllWarehouses.value = true

        activeWharehouseButton.value = whId

        activeWhInformation.value.bodega = (warehouse.getWarehouseList ?? [])[
            index
        ]

        showWaitOverlay.value = true

        resetInvData()

        onPageChanged('inventory', invTabController.value).then(() => {
            showWaitOverlay.value = false
        })
        onPageChanged('tomas-fisicas', tomasFisicasTabController.value)
        onPageChanged('purchases', purchaseTabController.value)
        onPageChanged('movements', movementTabController.value)

        showAllWarehouses.value = false
    }

    async function showItem(item: Item): Promise<void> {
        detailSelectedItem.value.item = item
        itemInfoShow.value = true
        detailSelectedItem.value.props = []
        detailSelectedItem.value.props = await itemStore.fetchItemProperties(
            item.id
        )
    }

    const truncate = (text: string, length: number, suffix: string): string => {
        if (typeof text == undefined || text == null) {
            return '---'
        }
        if (text.length > length) {
            return text.substring(0, length) + suffix
        } else {
            return text
        }
    }

    warehouse.fetchWarehouses().then(() => {
        whRows.value = (warehouse.getWarehouseList ?? []).length
        paginateAside(whPageCount.value, 0)
    })

    warehouse.fetchWarehousesLatestTomasFisicas().then(it => {
        allWarehousesTableInformation = it.data as WhWithTomaFisica[]
        paginateMain(whPageCount.value, 0)
        showWaitOverlay.value = false
    })
</script>

<template>
    <WaitOverlay :show="showWaitOverlay">
        <ECard>
            <div
                class="row d-inline-flex allign-content-center tw-bg-slate-50 dark:tw-bg-slate-600">
                <div
                    class="col-2 mx-1 tw-flex-col tw-rounded-lg tw-bg-white dark:tw-bg-slate-800">
                    <h1 class="title mt-2">Bodegas Disponibles</h1>

                    <b-form class="mt-2 t-form" role="search">
                        <b-form-input
                            class="mt-2"
                            type="search"
                            placeholder="Buscar"
                            aria-label="Search"
                            @change.prevent="">
                        </b-form-input>
                    </b-form>

                    <b-pagination
                        v-model="currentAsidePage"
                        :total-rows="whRows"
                        :per-page="whPageCount"
                        aria-controls="b-list-warehouses"
                        align="center"
                        @page-click.prevent="onAsidePageChanged"
                        :limit="3"
                        hide-goto-end-buttons
                        class="paginator"></b-pagination>

                    <b-list-group
                        :per-page="whPageCount"
                        :current-page="currentAsidePage"
                        class="button-group smaller-btn-group">
                        <b-list-group-item
                            :class="{ active: activeWharehouseButton === -1 }"
                            button
                            @click.prevent="
                                () => {
                                    showAllWarehouses = true
                                    activeWharehouseButton = -1
                                }
                            ">
                            Todas las bodegas
                        </b-list-group-item>
                        <b-list-group-item
                            v-for="(wh, index) in paginatedWarehouse"
                            button
                            :class="{
                                active: wh.id === activeWharehouseButton,
                            }"
                            :key="wh.id"
                            :id="'whbtn-' + wh.id"
                            @click.prevent="
                                wharehouseButtonPressed($event, wh.id, index)
                            ">
                            {{ wh.name }}
                        </b-list-group-item>
                    </b-list-group>
                </div>

                <div
                    v-if="showAllWarehouses"
                    class="col-xl tw-bg-slate-50 dark:tw-bg-slate-700">
                    <h1 class="title tw-text-3xl tw-mt-2 mb-2">
                        Bodegas y Últimas Tomas Físicas
                    </h1>

                    <div class="row display-inline-flex">
                        <b-form inline class="col-3">
                            <b-form-input
                                id="wh-search"
                                placeholder="Busqueda de Bodega">
                            </b-form-input>
                        </b-form>
                        <e-button
                            @click.prevent=""
                            type="button"
                            variant="primary"
                            class="col-1"
                            >Buscar
                        </e-button>

                        <b-pagination
                            v-model="mainPageController.currentPage"
                            :total-rows="whRows"
                            :per-page="whPageCount"
                            aria-controls="b-list-warehouses"
                            align="center"
                            @page-click.prevent="onMainPageChanged"
                            :limit="10"
                            class="paginator col-5 tw-inline-flex"></b-pagination>

                        <e-button
                            @click.prevent=""
                            type="button"
                            variant="secondary"
                            class="col-2 mx-1">
                            Limpiar filtros
                        </e-button>
                    </div>

                    <BTable
                        :fields="allWarehousesFields"
                        :items="paginatedMainTable"
                        class="text-center">
                        <template #cell(#)="{ index }">
                            {{ index + 1 }}
                        </template>
                        <template #cell(RealizadaPor)="{ item }">
                            {{
                                (item.whtf_done_by_name ?? '--') +
                                ' ' +
                                (item.whtf_done_by_lastname ?? '--')
                            }}
                        </template>
                        <template #cell(FechaTomaFisica)="{ item }">
                            {{ item.whtf_created_at }}
                        </template>
                        <template #cell(Novedad)="{ item }">
                            {{ truncate(item.whtf_novedad, 15, '...') }}
                        </template>
                        <template #cell(Detalles)="{}">
                            <e-button
                                left-icon="fa-eye"
                                @click.prevent=""
                                type="button"
                                variant="secondary"
                                >Ver detalles
                            </e-button>
                        </template>
                    </BTable>
                </div>

                <!-- Specific warehouse card  -->

                <div v-else class="col-xl">
                    <div
                        class="row tw-bg-slate-50 dark:tw-bg-slate-600 mt-2 mb-2">
                        <h1 class="tw-text-3xl tw-font-bold">
                            {{ activeWhInformation.bodega?.name }}
                        </h1>
                    </div>

                    <b-tabs active-tab-class="" content-class="mt-3 " pills>
                        <!--


                            INVENTARIO TAB


                        -->

                        <b-tab title="Inventario" active>
                            <div class="row display-inline-flex mb-1">
                                <b-form inline class="col-3">
                                    <b-form-input
                                        @submit.prevent
                                        id="wh-inv-search"
                                        placeholder="Busqueda de Inventario"
                                        v-model="invTabController.searchInput">
                                    </b-form-input>
                                </b-form>
                                <e-button
                                    @click.prevent=""
                                    type="button"
                                    variant="primary"
                                    class="col-2 mx-1"
                                    >Buscar
                                </e-button>

                                <e-button
                                    @click.prevent="
                                        onReset(invTabController, 'inventory')
                                    "
                                    type="button"
                                    variant="secondary"
                                    class="col-2 mx-1">
                                    Limpiar Busqueda
                                </e-button>
                            </div>

                            <ModalDialog v-model:show="itemInfoShow" size="3xl">
                                <template #dialog-title>
                                    <b class="tw-text-2xl"
                                        >Detalle del Ítem
                                        {{ detailSelectedItem.item?.name }}</b
                                    >
                                </template>
                                <div class="container">
                                    <h3 class="tw-text-xl tw-font-bold">
                                        Detalle
                                    </h3>
                                    <div
                                        class="row tw-pb-3 align-content-center justify-content-center gy-2">
                                        <template
                                            v-for="(
                                                d, k
                                            ) in detailSelectedItem.item"
                                            :key="k">
                                            <div
                                                class="tw-rounded tw-ring-1 tw-ring-slate-500 tw-py-1 col-12 col-md-5 tw-mx-2"
                                                v-if="
                                                    ![
                                                        'category',
                                                        'img',
                                                        'quantity',
                                                    ].includes(k)
                                                ">
                                                <div class="row">
                                                    <span
                                                        class="tw-w-1/2 tw-font-bold col-6"
                                                        >{{ k }}:</span
                                                    >
                                                    <span class="col-6">{{
                                                        d
                                                    }}</span>
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
                                            v-for="(
                                                param, idx
                                            ) in detailSelectedItem.props"
                                            :key="idx">
                                            <div
                                                class="col-6 col-md-3 col-xl-2 tw-text-md">
                                                <b>{{ param.name }}:</b>
                                            </div>
                                            <div
                                                class="col-6 col-md-3 col-xl-2">
                                                {{ param.value }}
                                            </div>
                                        </template>
                                    </div>
                                </div>
                            </ModalDialog>

                            <BTable
                                id="whinv-table"
                                :fields="inventoryFields"
                                :items="activeWhInformation.inventory"
                                class="table">
                                <template #cell(#)="{ index }">
                                    {{ index + 1 }}
                                </template>
                                <template #cell(PVenta)="{ item }">
                                    {{ item.price * item.quantity }}
                                </template>
                                <template #cell(Acciones)="{ item }">
                                    <e-button
                                        left-icon="fa-eye"
                                        @click.prevent="showItem(item)"
                                        type="button"
                                        variant="secondary"
                                        >Ver detalles
                                    </e-button>
                                </template>
                            </BTable>

                            <b-pagination
                                v-model="invTabController.currentPage"
                                :total-rows="invTabController.totalRows"
                                :per-page="whInformationPerPage"
                                aria-controls="whinv-table"
                                align="center"
                                @page-click.prevent="
                                    onPageChanged('inventory', invTabController)
                                "
                                :limit="10"
                                hide-goto-end-buttons
                                class="paginator"></b-pagination>
                        </b-tab>

                        <!--


                            HISTORIAL DE COMPRAS TAB


                        -->

                        <b-tab title="Historial de Compras">
                            <div class="row display-inline-flex mb-1">
                                <b-form inline class="col-3">
                                    <b-form-input
                                        @submit.prevent
                                        id="wh-purchase-search"
                                        placeholder="Busqueda de Compra">
                                    </b-form-input>
                                    <input type="date" />
                                </b-form>

                                <e-button
                                    @click.prevent=""
                                    type="button"
                                    variant="primary"
                                    class="col-2 mx-1"
                                    >Buscar
                                </e-button>

                                <e-button
                                    type="button"
                                    variant="secondary"
                                    class="col-2 mx-1"
                                    @click.prevent="
                                        onReset(
                                            purchaseTabController,
                                            'purchases'
                                        )
                                    "
                                    >Limpiar Busqueda
                                </e-button>
                            </div>

                            <BTable
                                :fields="purchasesFields"
                                :items="activeWhInformation.purchases">
                                <template #cell(#)="{ index }">
                                    {{ index + 1 }}
                                </template>
                                <template #cell(FechaCreación)="{ item }">
                                    {{ truncate(item.aproved_at, 10, '') }}
                                </template>
                                <template #cell(Entregado)="{}">
                                    <b-form-checkbox
                                        id="checkbox-1"
                                        name="checkbox-1"
                                        value="accepted">
                                    </b-form-checkbox>
                                </template>
                                <template #cell(Proveedor)="{ item }">
                                    {{ item.provider.name }}
                                </template>
                                <template #cell(Pago)="{ item }">
                                    {{ item.invoice.code ?? '--' }}
                                </template>
                                <template #cell(FechaPago)="{ item }">
                                    {{
                                        truncate(
                                            item.invoice.created_at,
                                            10,
                                            ''
                                        )
                                    }}
                                </template>
                                <template #cell(Acciones)="{}">
                                    <e-button
                                        left-icon="fa-eye"
                                        @click.prevent=""
                                        type="button"
                                        variant="secondary"
                                        >Ver detalles
                                    </e-button>
                                </template>
                            </BTable>

                            <b-pagination
                                v-model="purchaseTabController.currentPage"
                                :total-rows="purchaseTabController.totalRows"
                                :per-page="whInformationPerPage"
                                aria-controls="whpurchase-table"
                                align="center"
                                @page-click.prevent="
                                    onPageChanged(
                                        'purchases',
                                        purchaseTabController
                                    )
                                "
                                :limit="10"
                                hide-goto-end-buttons
                                class="paginator"></b-pagination>
                        </b-tab>

                        <!--


                            TOMAS FISICAS TAB


                        -->

                        <b-tab title="Toma Física">
                            <div class="row display-inline-flex mb-1">
                                <b-form inline class="col-3">
                                    <b-form-input
                                        id="wh-tf-search"
                                        placeholder="Busqueda de Toma Física"
                                        v-model="
                                            tomasFisicasTabController.searchInput
                                        ">
                                    </b-form-input>
                                </b-form>
                                <e-button
                                    @click.prevent=""
                                    type="button"
                                    variant="primary"
                                    class="col-2 mx-1"
                                    >Buscar
                                </e-button>

                                <e-button
                                    type="button"
                                    variant="secondary"
                                    class="col-2 mx-1"
                                    @click.prevent="
                                        onReset(
                                            tomasFisicasTabController,
                                            'tomas-fisicas'
                                        )
                                    "
                                    >Limpiar Busqueda
                                </e-button>
                            </div>

                            <BTable
                                :fields="tomasFisFields"
                                :items="activeWhInformation.tomasFisicas">
                                <template #cell(#)="{ index }">
                                    {{ index + 1 }}
                                </template>
                                <template #cell(FechaRealizacion)="{ item }">
                                    {{ truncate(item.created_at, 10, '') }}
                                </template>
                                <template #cell(RealizadaPor)="{ item }">
                                    {{
                                        item.done_by.name +
                                        ' ' +
                                        item.done_by.lastname
                                    }}
                                </template>
                                <template #cell(Acciones)="{}">
                                    <e-button
                                        left-icon="fa-eye"
                                        @click.prevent=""
                                        type="button"
                                        variant="secondary"
                                        >Ver detalles
                                    </e-button>
                                </template>
                            </BTable>

                            <b-pagination
                                v-model="tomasFisicasTabController.currentPage"
                                :total-rows="
                                    tomasFisicasTabController.totalRows
                                "
                                :per-page="whInformationPerPage"
                                aria-controls="whpurchase-table"
                                align="center"
                                @page-click.prevent="
                                    onPageChanged(
                                        'tomas-fisicas',
                                        tomasFisicasTabController
                                    )
                                "
                                :limit="10"
                                hide-goto-end-buttons
                                class="paginator"></b-pagination>
                        </b-tab>

                        <b-tab title="Movimientos">
                            <!--


                            MOVIMIENTOS DE BODEGA TAB


                        -->
                            <div class="row display-inline-flex mb-1">
                                <b-form inline class="col-3">
                                    <b-form-input
                                        id="wh-mov-search"
                                        placeholder="Busqueda de Movimiento"
                                        @submit.prevent>
                                    </b-form-input>
                                </b-form>
                                <e-button
                                    @click.prevent=""
                                    type="button"
                                    variant="primary"
                                    class="col-2 mx-1"
                                    >Buscar
                                </e-button>

                                <e-button
                                    type="button"
                                    variant="secondary"
                                    class="col-2 mx-1"
                                    @click.prevent="
                                        onReset(
                                            movementTabController,
                                            'movements'
                                        )
                                    "
                                    >Limpiar Busqueda
                                </e-button>
                            </div>

                            <BTable
                                :fields="movementsFields"
                                :items="activeWhInformation.movements">
                                <template #cell(#)="{ index }">
                                    {{ index + 1 }}
                                </template>

                                <template #cell(Creada)="{ item }">
                                    {{ truncate(item.created_at, 10, '') }}
                                </template>
                                <template #cell(RealizadaPor)="{ item }">
                                    {{
                                        item.created_by.name +
                                        ' ' +
                                        item.created_by.lastname
                                    }}
                                </template>
                                <template #cell(BodegaRelacionada)="{ item }">
                                    {{
                                        item.warehouse_destiny.id ==
                                        activeWhInformation.bodega.id
                                            ? item.warehouse_destiny.name
                                            : item.warehouse_origin.name
                                    }}
                                </template>
                                <template #cell(TipoDeMovimiento)="{ item }">
                                    {{
                                        item.warehouse_destiny.id ==
                                        activeWhInformation.bodega.id
                                            ? 'Salida'
                                            : 'Entrada'
                                    }}
                                </template>
                                <template #cell(Notas)="{ item }">
                                    {{ truncate(item.notes, 10, '...') }}
                                </template>
                                <template #cell(Acciones)="{}">
                                    <e-button
                                        left-icon="fa-eye"
                                        @click.prevent=""
                                        type="button"
                                        variant="primary"
                                        >Ver detalles
                                    </e-button>
                                </template>
                            </BTable>

                            <b-pagination
                                v-model="movementTabController.currentPage"
                                :total-rows="movementTabController.totalRows"
                                :per-page="whInformationPerPage"
                                aria-controls="whpurchase-table"
                                align="center"
                                @page-click.prevent="
                                    onPageChanged(
                                        'movements',
                                        movementTabController
                                    )
                                "
                                :limit="10"
                                hide-goto-end-buttons
                                class="paginator"></b-pagination>
                        </b-tab>
                    </b-tabs>
                </div>
            </div>
        </ECard>
    </WaitOverlay>
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
            @apply tw-text-sm;
        }

        @media (prefers-color-scheme: dark) {
            color: white !important;
            --bs-table-striped-color: theme(colors.zinc.400);
            --bs-table-hover-color: theme('colors.primary.light');
            --bs-table-hover-bg: theme(colors.primary.light / 15%);
        }
    }
</style>
