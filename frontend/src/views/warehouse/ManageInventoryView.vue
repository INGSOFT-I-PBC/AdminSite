<script setup lang="ts">
    import { useWarehouseStore } from '@store'
    import type { Warehouse } from '@store/types'
    import { BPagination } from 'bootstrap-vue-3'

    import { ref, watch } from 'vue'

    import { ECard, WaitOverlay } from '@custom-components'

    const warehouseStore = useWarehouseStore()

    const loadingState = ref({
        waitWarehouse: false,
        waitData: false,
    })

    const toggle = ref<boolean>(true)

    const currentAsidePage = ref<number>(1)
    const whRows = ref<number>(0)
    const paginatedWarehouse = ref<Warehouse[]>()
    const whPageCount = ref<number>(15)
    const activeWharehouseButton = ref<number>(-1)
    const selectedWarehouse = ref<Warehouse>()

    function paginateAside() {
        paginatedWarehouse.value = (
            warehouseStore.getWarehouseList ?? []
        ).slice(
            (currentAsidePage.value - 1) * whPageCount.value,
            currentAsidePage.value * whPageCount.value
        )
    }

    function wharehouseButtonPressed(wh: Warehouse, index: number) {
        selectedWarehouse.value = wh
    }

    warehouseStore.fetchWarehouses()

    watch(currentAsidePage, paginateAside)
</script>

<template>
    <WaitOverlay :show="loadingState.waitWarehouse">
        <ECard>
            <div
                class="row d-inline-flex allign-content-center tw-bg-slate-50 dark:tw-bg-slate-600">
                <div
                    v-if="toggle"
                    class="col-sm-12 col-md-12 col-xl-2 mx-1 tw-flex-col tw-rounded-lg tw-bg-white dark:tw-bg-slate-800 justify-center">
                    <h1 class="title my-2">Bodegas Disponibles</h1>

                    <e-button
                        @click.left="
                            () => {
                                toggle = false
                            }
                        "
                        class="tw-text-slate-800 col-lg-3 col-md-3 col-sm-6 col-xl-6 mx-3 mb-3"
                        left-icon="chevrons-left"
                        icon-provider="feather">
                    </e-button>

                    <b-pagination
                        v-model="currentAsidePage"
                        :total-rows="whRows"
                        :per-page="whPageCount"
                        aria-controls="b-list-warehouses"
                        :limit="3"
                        hide-goto-end-buttons
                        class="paginator mb-2"></b-pagination>

                    <b-list-group
                        :per-page="whPageCount"
                        :current-page="currentAsidePage"
                        class="button-group smaller-btn-group col-lg-12 col-md-6 col-sm-6">
                        <b-list-group-item
                            :class="{ active: activeWharehouseButton === -1 }"
                            button
                            @click.left="
                                () => {
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
                            @click.left="wharehouseButtonPressed(wh, index)">
                            {{ wh.name }}
                        </b-list-group-item>
                    </b-list-group>
                </div>
                <div class="col-xl tw-bg-slate-50 dark:tw-bg-slate-700"></div>
            </div>
        </ECard>
    </WaitOverlay>
</template>
