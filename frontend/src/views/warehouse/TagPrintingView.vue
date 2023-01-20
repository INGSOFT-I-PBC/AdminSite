<template>
    <ECard>
        <BRow align-v="center" align-h="around">
            <!-- Search bar section -->
            <BCol cols="12">
                <BRow>
                    <BCol lg="3">
                        <InputText
                            label="Búsqueda por Código"
                            v-model="searchForm.code" />
                    </BCol>
                    <BCol lg="3">
                        <InputText
                            label="Búsqueda por Nombre"
                            v-model="searchForm.name" />
                    </BCol>
                    <BCol lg="3" v-show="false">
                        <ListBox
                            top-label="Filtro por bodega"
                            v-model="searchForm.warehouse" />
                    </BCol>
                    <BCol class="tw-flex" md="6" xl="auto">
                        <EButton class="tw-min-w-full tw-flex tw-self-center"
                            >Buscar</EButton
                        >
                    </BCol>
                </BRow>
            </BCol>
        </BRow>

        <!-- Showing section  -->
        <WaitOverlay :show="searchForm.showWait">
            <BRow
                align-v="fill"
                align-h="around"
                align-content="around"
                gutter-x="3"
                gutter-y="4">
                <template v-if="loadedData">
                    <BCol
                        v-for="data in loadedData.data"
                        :key="data.id"
                        cols="auto"
                        md="6"
                        lg="4"
                        xxl="3">
                        <ECard class="tw-h-full">
                            <BarcodeImage
                                id="sdfs"
                                :code="data.upc ?? ''"
                                :width="2"
                                :height="75" />
                            <Title size="xl"
                                >#{{ data.id }} {{ data.product_name }}</Title
                            >
                            <Title size="lg">{{ data.variant_name }}</Title>
                        </ECard>
                    </BCol>
                </template>
                <BCol v-else cols="12">
                    <Title class="tw-w-full tw-text-center tw-p-5"
                        >No hay datos para mostrar</Title
                    >
                </BCol>
                <BCol cols="12">
                    <BPagination
                        v-model="searchForm.page"
                        :per-page="searchForm.per_page"
                        :total-rows="loadedData?.total ?? 1"
                        align="center" />
                </BCol>
            </BRow>
        </WaitOverlay>
    </ECard>
</template>

<script lang="ts" setup>
    import BarcodeImage from '@components/holders/BarcodeImage.vue'
    import { useProductStore } from '@store/product'
    import type { PaginatedResponse } from '@store/types'
    import type { BCProductVariant } from '@store/types/product'
    import { BRow } from 'bootstrap-vue-3'

    import { onMounted } from 'vue'
    import { useToast } from 'vue-toastification'

    import {
        EButton,
        ECard,
        InputText,
        ListBox,
        Title,
        WaitOverlay,
    } from '@custom-components'

    const searchForm = ref({
        code: '',
        name: '',
        warehouse: null,
        page: 1,
        per_page: 12,
        showWait: false,
    })

    const itemStore = useProductStore()
    const toast = useToast()

    const loadedData = ref<PaginatedResponse<BCProductVariant> | Nullish>(null)

    async function makeSearch() {
        searchForm.value.showWait = true
        loadedData.value = await itemStore.searchThroughVariants(
            searchForm.value
        )
        searchForm.value.page = 1
        searchForm.value.showWait = false
        toast.success('Datos Cargados')
    }
    onMounted(async () => {
        makeSearch()
    })
</script>
