<template>
    <ModalDialog v-model:show="itemInfoShow" size="xl">
        <template #dialog-title>
            <b class="tw-text-2xl">Generación De Pdf</b>
        </template>
        <div class="container">
            <p>Coloque la cantidad de etiquetas</p>

            <br />
            <div style="spacing = 100">
                <div class="container">
                    <p>De</p>
                    <InputText v-model="cantTickets" ref="cant1" />
                    <p>hasta</p>
                    <InputText v-model="cantTickets2" ref="cant2" />
                </div>

                &nbsp; &nbsp;
                <div class="container">
                    <e-button
                        left-icon=""
                        type="button"
                        @click="Tickets($event)">
                        Previsualización</e-button
                    >
                </div>
            </div>
        </div>
    </ModalDialog>

    <ModalDialog v-model:show="itemInfoShow2" size="4xl">
        <template #dialog-title>
            <b class="tw-text-2xl">Codigos De Etiquetas</b>
        </template>
        <br />
        <div class="container" id="contenedor">
            <BRow
                align-v="fill"
                align-h="around"
                align-content="around"
                gutter-x="3"
                gutter-y="4">
                <template v-if="arr_tickets">
                    <BCol
                        v-for="data in arr_tickets"
                        :key="data.id"
                        cols="3"
                        md="4"
                        lg="3"
                        xxl="3">
                        <ECard class="tw-h-full" style="margin-bottom: 10px">
                            <BarcodeImage
                                id="sdfs"
                                :code="data.upc ?? ''"
                                :width="2"
                                :height="40" />
                            <Title style="font-size: 11; text-align: center"
                                >{{ data.product_name }}
                                {{ data.variant_name }}</Title
                            >
                            <!--
                                <Title style="font-size:12; text-align:center">{{ data.variant_name }}</Title>-->
                        </ECard>
                    </BCol>
                </template>
            </BRow>
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
                        <EButton
                            class="tw-min-w-full tw-flex tw-self-center"
                            @click.left="makeSearch"
                            >Buscar</EButton
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
    //import {html2pdf} from "html2pdf.js"
    import BarcodeImage from '@components/holders/BarcodeImage.vue'
    import { useProductStore } from '@store/product'
    import type { PaginatedResponse } from '@store/types'
    import type { BCProductVariant } from '@store/types/product'
    import { BRow } from 'bootstrap-vue-3'
    import { jsPDF } from 'jspdf'

    import { onMounted } from 'vue'
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

    const searchForm = ref({
        code: '',
        name: '',
        warehouse: null,
        page: 1,
        per_page: 20,
        showWait: false,
    })

    const paginationOptions = computed<PaginationOptions>(() => ({
        page: searchForm.value.page,
        per_page: searchForm.value.per_page,
    }))

    const itemStore = useProductStore()
    const toast = useToast()
    const itemInfoShow = ref(false)
    const itemInfoShow2 = ref(false)
    const cantTickets = ref<string>('')
    const cantTickets2 = ref<string>('')

    const loadedData = ref<PaginatedResponse<BCProductVariant> | Nullish>(null)

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

    async function makeSearch() {
        searchForm.value.showWait = true
        loadedData.value = await itemStore.searchThroughVariants({
            ...searchForm.value,
            ...paginationOptions.value,
        })

        console.log(loadedData.value)
        console.log(searchForm.value.code)
        console.log(searchForm.value.name)
        searchForm.value.page = 1
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
        searchForm.value.showWait = true
        console.log(cantTickets.value)
        loadedData.value = await itemStore.searchThroughVariants(
            searchForm.value
        )
        searchForm.value.page = 1
        searchForm.value.showWait = false
        //let arr_tickets = []
        for (let i = 0; i < Number(cantTickets2.value); i++) {
            if (
                i >= Number(cantTickets.value) &&
                i <= Number(cantTickets2.value)
            ) {
                arr_tickets.push(loadedData.value.data[i])
            }
        }
        console.log(arr_tickets)
        itemInfoShow2.value = true
        itemInfoShow.value = false
    }
    interface Pdf {
        titulo?: string
        etiqueta?: string
        salary?: number
    }

    const pdf: Pdf = {
        titulo: '',
        etiqueta: '',
        salary: 0,
    }

    async function imprimirPdf(event: any) {
        pdf.titulo = document.getElementById('tituloname')?.innerText
        const contenedor = document.getElementById('hola')?.innerText
        pdf.etiqueta = document.getElementById('card')?.innerText
        //var card = document.getElementById('card')?.innerText
        //const titulo= emp.titulo
        const titulo: string = pdf.titulo || ''
        const etiqueta: string = pdf.etiqueta || ''
        console.log(titulo)
        const doc = new jsPDF('l', 'mm', [297, 210])
        doc.setFontSize(22)
        doc.text('hola', 20, 10)
        doc.text('steven', 10, 20)
        doc.text(titulo, 20, 30)
        doc.text(etiqueta, 30, 30)
        doc.save('a4.pdf')
    }

    /*
    async function printPdf(event: any){
        html2pdf(document.getElementById("etiquetas"), {
				margin: 1,
  			filename: "etiquetas.pdf",
			})
    }
    */

    async function html_to_Pdf() {
        const doc = new jsPDF('p', 'mm', [297, 210])
        const element = document.querySelector('#contenedor')
        const elementHTML: HTMLElement = element as HTMLElement
        //var elementHTML = document.querySelector('#etiquetas')
        doc.html(elementHTML, {
            callback: function (doc) {
                doc.save('etiquetas.pdf')
            },
            margin: [10, 10, 10, 10],
            autoPaging: 'text',
            x: 0,
            y: 0,
            width: 190,
            windowWidth: 675,
        })
    }
</script>
