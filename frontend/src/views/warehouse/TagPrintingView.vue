<template>
    <ModalDialog v-model:show="itemInfoShow5" size="xl">
        <template #dialog-title>
            <b class="tw-text-2xl">Validación De Ingreso</b>
        </template>
        <div class="container">
            <p>
                Los datos ingresos son incorrectos o los campos estan vacios,
                presione "Limpiar Búsqueda" y vuelva a intentar
            </p>
        </div>
    </ModalDialog>

    <ModalDialog v-model:show="itemInfoShow4" size="xl">
        <template #dialog-title>
            <b class="tw-text-2xl">Validación De Ingreso</b>
        </template>
        <div class="container">
            <p>
                Los datos ingresos son incorrectos o los campos estan vacios,
                presione "Limpiar Búsqueda" y vuelva a intentar
            </p>
        </div>
    </ModalDialog>

    <ModalDialog v-model:show="itemInfoShow" size="xl">
        <template #dialog-title>
            <b class="tw-text-2xl">Generación De Pdf</b>
        </template>
        <div class="container">
            <p>Eliga un modo por rangos o por código de etiqueta</p>

            <br />
            <div style="spacing = 100">
                <div class="container">
                    <b-row>
                        <b-col lg="1" class="my-1">
                            <b class="tw-text-1xl">De:</b>
                        </b-col>
                        <b-col lg="2" class="my-1">
                            <InputText
                                v-model="cantTickets"
                                style="width: 70px" />
                        </b-col>
                        &nbsp;
                        <b-col lg="2" class="my-1">
                            <b class="tw-text-1xl">Hasta:</b>
                        </b-col>
                        <b-col lg="1" class="my-1">
                            <InputText
                                v-model="cantTickets2"
                                style="width: 70px" />
                        </b-col>
                    </b-row>
                </div>
                <div class="container">
                    <b-row>
                        <b-col lg="3" class="my-1">
                            <b class="tw-text-1xl">Por Código De Etiqueta:</b>
                        </b-col>
                        <b-col lg="3" class="my-1">
                            <InputText
                                v-model="codeTicket"
                                style="width: 125px" />
                        </b-col>
                        &nbsp;
                        <b-col lg="3" class="my-1">
                            <b class="tw-text-1xl">Número De Veces:</b>
                        </b-col>
                        <b-col lg="1" class="my-1">
                            <InputText v-model="numTimes" style="width: 70px" />
                        </b-col>
                    </b-row>
                </div>

                &nbsp; &nbsp;
                <div class="container">
                    <BRow>
                        <BCol class="tw-flex" md="4" xl="auto">
                            <e-button
                                class="tw-flex tw-self-center"
                                left-icon=""
                                type="button"
                                @click="Tickets($event)">
                                Previsualización Rango</e-button
                            >
                            &nbsp;&nbsp;
                            <e-button
                                class="tw-flex tw-self-center"
                                left-icon=""
                                type="button"
                                @click="Tickets2($event)">
                                Previsualización Código</e-button
                            >
                            &nbsp;&nbsp;
                            <EButton
                                class="tw-flex tw-self-center"
                                @click.left="
                                    () => {
                                        cantTickets = ''
                                        cantTickets2 = ''
                                        numTimes = ''
                                        codeTicket = ''
                                    }
                                "
                                >Limpiar Buscar</EButton
                            >
                        </BCol>
                    </BRow>
                </div>
            </div>
        </div>
    </ModalDialog>

    <ModalDialog v-model:show="itemInfoShow2" size="sm">
        <template #dialog-title>
            <b class="tw-text-2xl">Códigos De Etiquetas</b>
        </template>
        <br />
        <div class="container" id="contenedor" style="justify-content: center">
            <template v-if="arr_tickets">
                <BCol
                    v-for="data in arr_tickets"
                    :key="data.id"
                    cols="3"
                    md="4"
                    lg="3"
                    xxl="3"
                    style="height: 142px">
                    <ECard
                        class="tw-h-full"
                        style="
                            margin-bottom: 10px;
                            height: 115px;
                            background-color: white;
                            border-color: black;
                            border-width: 1px;
                            width: 118px;
                            justify-content: center;
                            justify-items: center;
                        ">
                        <BarcodeImage
                            id="sdfs"
                            :code="data.upc ?? ''"
                            :width="1.1"
                            :height="35"
                            style="border-color: black; padding-top: 0.9" />

                        <Title
                            style="
                                font-size: 8.6;
                                text-align: center;
                                color: black;
                                padding-bottom: 1;
                            ">
                            <strong>
                                {{ data.variant_name }} {{ '$'
                                }}{{ data.price.slice(0, -1) }}
                            </strong></Title
                        >
                    </ECard>
                </BCol>
                &nbsp;
            </template>
        </div>
        <div class="container">
            &nbsp; &nbsp;
            <div class="container">
                <e-button left-icon="" type="button" @click="html_to_Pdf()">
                    Generar</e-button
                >
            </div>
        </div>
    </ModalDialog>

    <ModalDialog v-model:show="itemInfoShow3" size="lg">
        <template #dialog-title>
            <b class="tw-text-2xl">Códigos De Etiquetas</b>
        </template>
        <br />
        <div class="container" id="contenedorName">
            <template v-if="arr_times">
                <BCol
                    v-for="data in arr_times"
                    :key="data.id"
                    cols="3"
                    md="4"
                    lg="3"
                    xxl="3"
                    style="height: 142px">
                    <ECard
                        class="tw-h-full"
                        style="
                            margin-bottom: 10px;
                            height: 115px;
                            background-color: white;
                            border-color: black;
                            border-width: 1px;
                            width: 118px;
                            justify-content: center;
                            justify-items: center;
                        ">
                        <BarcodeImage
                            id="sdfs"
                            :code="data.upc ?? ''"
                            :width="1.1"
                            :height="35"
                            style="border-color: black; padding-top: 0.9" />

                        <Title
                            style="
                                font-size: 8.6;
                                text-align: center;
                                color: black;
                                padding-bottom: 1;
                            ">
                            <strong>
                                {{ data.variant_name }} {{ '$'
                                }}{{ data.price.slice(0, -1) }}
                            </strong></Title
                        >
                    </ECard>
                </BCol>
                &nbsp;
            </template>
        </div>
        <div class="container">
            &nbsp; &nbsp;
            <div class="container">
                <e-button left-icon="" type="button" @click="html_to_Pdf2()">
                    Generar</e-button
                >
            </div>
        </div>
    </ModalDialog>

    <ECard>
        <BRow align-v="center" align-h="around">
            <!-- Search bar section -->
            <BCol cols="12">
                <BRow>
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
                        <EButton
                            class="tw-min-w-full tw-flex tw-self-center"
                            @click.left="
                                () => {
                                    makeSearch()
                                }
                            "
                            >Consultar</EButton
                        >
                    </BCol>
                    <BCol class="tw-flex" md="6" xl="auto">
                        <EButton
                            class="tw-min-w-full tw-flex tw-self-center"
                            @click.left="
                                () => {
                                    searchForm.name = ''
                                    resetData()
                                }
                            "
                            >Limpiar Búsqueda</EButton
                        >
                    </BCol>
                    <BCol class="tw-flex" md="6" xl="auto">
                        <EButton
                            class="tw-min-w-full tw-flex tw-self-center"
                            @click="RangeSticker($event)"
                            >Generar PDF</EButton
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
                <template v-if="paginatedMainTable">
                    <BCol
                        v-for="data in paginatedMainTable"
                        :key="data.id"
                        cols="auto"
                        md="6"
                        lg="4"
                        xxl="3"
                        id="card"
                        :current-page="searchForm.page"
                        :per-page="searchForm.per_page">
                        <ECard class="tw-h-full">
                            <BarcodeImage
                                id="sdfs"
                                :code="data.upc ?? ''"
                                :width="2"
                                :height="75" />
                            <Title size="xl"
                                >#{{ data.id }} {{ data.product_name }}</Title
                            >
                            <Title size="lg"
                                >{{ data.variant_name }} {{ '$'
                                }}{{ data.price.slice(0, -1) }}</Title
                            >
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
                        :total-rows="whRows"
                        @page-click.left="onMainPageChanged"
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
    import type {
        BCProductVariant,
        BCProductVariant2,
    } from '@store/types/product'
    import { BPagination, BRow } from 'bootstrap-vue-3'
    import { jsPDF } from 'jspdf'
    import 'jspdf-autotable'

    import { onMounted } from 'vue'
    import { computed, ref, watch } from 'vue'
    import { useToast } from 'vue-toastification'

    import {
        EButton,
        ECard,
        InputText,
        ListBox,
        ModalDialog,
        Title,
        WaitOverlay,
    } from '@custom-components'

    const whRows = ref(20)
    const loadedData = ref<PaginatedResponse<BCProductVariant> | Nullish>(null)
    const loadedData2 = ref<PaginatedResponse<BCProductVariant> | Nullish>(null)
    const loadedData3 = ref<PaginatedResponse<BCProductVariant> | Nullish>(null)
    const paginatedMainTable = ref<BCProductVariant[]>([])

    const searchForm = ref({
        code: '',
        name: '',
        warehouse: null,
        page: 1,
        per_page: 20,
        showWait: false,
        paginatedItems: paginatedMainTable.value,
    })

    const searchForm2 = ref({
        code: '',
        name: '',
        warehouse: null,
        page: 1,
        per_page: 42,
        showWait: false,
    })

    const searchForm3 = ref({
        code: '',
        name: '',
        warehouse: null,
        page: 1,
        per_page: 42,
        showWait: false,
    })

    const paginationOptions = computed<PaginationOptions>(() => ({
        page: searchForm.value.page,
        per_page: searchForm.value.per_page,
    }))

    const itemStore = useProductStore()
    const itemStore2 = useProductStore()
    const itemStore3 = useProductStore()
    const toast = useToast()
    const itemInfoShow = ref(false)
    const itemInfoShow2 = ref(false)
    const itemInfoShow3 = ref(false)
    const itemInfoShow4 = ref(false)
    const itemInfoShow5 = ref(false)
    const cantTickets = ref<string>('')
    const cantTickets2 = ref<string>('')
    const codeTicket = ref<string>('')
    const numTimes = ref<string>('')
    const stopWatcher = ref(true)

    const arr_tickets: {
        product_name: string
        summary: string
        brand_name: string
        short_description: string
        id: number
        img: string | null
        upc: string | null
        ean: string | null
        variant_name: string
        sku: string
        price: string
        stock_level: number
        attributes: { name: string; value: string; type: string }[]
    }[] = []

    let arr_tickets2: {
        product_name: string
        summary: string
        brand_name: string
        short_description: string
        id: number
        img: string | null
        upc: string | null
        ean: string | null
        variant_name: string
        sku: string
        price: string
        stock_level: number
        attributes: { name: string; value: string; type: string }[]
    }[] = []

    const arr_times: {
        product_name: string
        summary: string
        brand_name: string
        short_description: string
        id: number
        img: string | null
        upc: string | null
        ean: string | null
        variant_name: string
        sku: string
        price: string
        stock_level: number
        attributes: { name: string; value: string; type: string }[]
    }[] = []

    async function makeSearch() {
        searchForm.value.showWait = true

        loadedData.value = await itemStore.searchThroughVariants(
            {
                ...searchForm.value,
                ...paginationOptions.value,
            },
            null,
            searchForm.value.name
        )

        whRows.value = loadedData.value.total

        arr_tickets2 = []
        for (let i = 0; i < searchForm.value.per_page; i++) {
            if (loadedData.value.data[i]) {
                arr_tickets2.push(loadedData.value.data[i])
            }
        }

        paginatedMainTable.value = arr_tickets2
        searchForm.value.showWait = false
        toast.success('Datos Cargados')
    }

    onMounted(async () => {
        makeSearch()
    })

    async function RangeSticker(event: any) {
        itemInfoShow.value = true
    }

    async function Tickets(event: any) {
        searchForm2.value.showWait = true
        loadedData2.value = await itemStore2.searchThroughVariants(
            searchForm2.value
        )
        arr_tickets.length = 0
        searchForm2.value.page = 1
        searchForm2.value.showWait = false
        if (
            cantTickets2.value != null &&
            cantTickets.value != null &&
            !isNaN(Number(cantTickets.value)) &&
            !isNaN(Number(cantTickets2.value)) &&
            Number(cantTickets2.value) <= loadedData2.value.total &&
            Number(cantTickets.value) > 0
        ) {
            for (let i = 0; i < Number(cantTickets2.value); i++) {
                if (
                    i >= Number(cantTickets.value) &&
                    i <= Number(cantTickets2.value)
                ) {
                    arr_tickets.push(loadedData2.value.data[i])
                }
            }
            itemInfoShow2.value = true
            itemInfoShow3.value = false
            itemInfoShow.value = false
        } else {
            itemInfoShow4.value = true
            itemInfoShow2.value = false
            itemInfoShow3.value = false
            itemInfoShow.value = true
        }

        console.log(arr_tickets)
    }

    async function Tickets2(event: any) {
        searchForm3.value.showWait = true
        loadedData3.value = await itemStore3.searchThroughVariants(
            searchForm3.value
        )
        arr_times.length = 0
        searchForm3.value.page = 1
        searchForm3.value.showWait = false

        if (
            numTimes.value != null &&
            codeTicket.value != null &&
            typeof codeTicket.value === 'string' &&
            typeof numTimes.value === 'string' &&
            codeTicket.value.length === 9
        ) {
            for (let k = 0; k < loadedData3.value.total; k++) {
                if (loadedData3.value.data[k].upc === codeTicket.value) {
                    for (let j = 0; j < Number(numTimes.value); j++) {
                        arr_times.push(loadedData3.value.data[j])
                    }
                }
            }
            itemInfoShow3.value = true
            itemInfoShow2.value = false
            itemInfoShow.value = false
        } else {
            itemInfoShow5.value = true
            itemInfoShow2.value = false
            itemInfoShow3.value = false
            itemInfoShow.value = true
        }

        console.log(arr_times)
    }

    async function html_to_Pdf() {
        const doc = new jsPDF('p', 'mm', [297, 75])
        const element = document.querySelector('#contenedor')
        const elementHTML: HTMLElement = element as HTMLElement
        const pageCount = Math.ceil(elementHTML.offsetHeight / 200)
        console.log(pageCount)

        doc.html(elementHTML, {
            callback: function (doc) {
                doc.save('etiquetas.pdf')
            },
            margin: [2, 2, 2, 2],
            autoPaging: 'text',
            x: 0,
            y: 0,
            width: 190,
            windowWidth: 675,
        })
    }

    async function html_to_Pdf2() {
        const doc2 = new jsPDF('p', 'mm', [297, 75])
        const element2 = document.querySelector('#contenedorName')
        const elementHTML2: HTMLElement = element2 as HTMLElement
        const pageCount2 = Math.ceil(elementHTML2.offsetHeight / 200)
        console.log(pageCount2)

        doc2.html(elementHTML2, {
            callback: function (doc2) {
                doc2.save('etiquetas2.pdf')
            },
            margin: [2, 2, 2, 2],
            autoPaging: 'text',
            x: 0,
            y: 0,
            width: 190,
            windowWidth: 675,
        })
    }

    function paginateMain(page_size: number, page_number: number): void {
        paginatedMainTable.value = arr_tickets2.slice(
            page_number * page_size,
            (page_number + 1) * page_size
        )
        stopWatcher.value = false
    }

    function onMainPageChanged(event: Event, page: number): void {
        paginateMain(searchForm.value.per_page, page - 1)
    }

    /*
    function filterData(): void {
        stopWatcher.value = true
        console.log(arr_tickets.length)

        if (searchForm.value.name.length > 0 || searchForm.value.code.length > 0) {
            console.log(paginatedMainTable.value)
            let arr_temp = ref<BCProductVariant[]>([])
            paginatedMainTable.value = (arr_tickets2 ?? []).filter(element => {
                    console.log(element.product_name)
                    console.log(element.upc)
                    console.log(element.product_name.includes(searchForm.value.name))
                    console.log(element.upc?.includes(searchForm.value.code))

                    if( element.product_name.includes(searchForm.value.name) ){
                            console.log('steven')
                            const indice = arr_tickets2.indexOf(element)
                            console.log(indice)
                            arr_temp.value.push(arr_tickets2[indice])
                    }
                    console.log(arr_temp.value)
                    console.log(paginatedMainTable.value)

                    return ( paginatedMainTable.value = (arr_temp.value) )
                }).slice(
                    searchForm.value.page * searchForm.value.per_page,
                    (searchForm.value.page + 1) *
                    searchForm.value.per_page
                )
            paginatedMainTable.value = arr_temp.value
            paginateMain(searchForm.value.per_page, 0)
            console.log(paginatedMainTable)
            console.log(whRows.value, paginatedMainTable.value.length)
            console.log(whRows.value, searchForm.value.per_page, paginatedMainTable.value.length / searchForm.value.per_page, Math.ceil( paginatedMainTable.value.length / searchForm.value.per_page ) )
        } else {
            stopWatcher.value = false
            paginateMain(searchForm.value.per_page, 0)
        }
    }*/

    watch(searchForm.value, prueba)

    function prueba() {
        if (!stopWatcher.value) {
            stopWatcher.value = true
            makeSearch()
        }
    }

    async function resetData() {
        makeSearch()
    }
</script>
