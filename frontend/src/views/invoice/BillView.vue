<script setup lang="ts">
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import ECol from '@components/custom/ECol.vue'
    import ERow from '@components/custom/ERow.vue'
    import InputText from '@components/custom/InputText.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import type { PaginatedAPIResponse, PaginatedResponse } from '@store-types'
    import { useInvoiceStore } from '@store/invoice'
    import type {
        IClient,
        IPayment,
        IServerOptions,
        Invoice,
    } from '@store/types'
    import { isMessage } from '@store/types'
    import { BIconFileEarmarkSlidesFill } from 'bootstrap-icons-vue'
    //import { useToast } from 'vue-toastification'
    import type { BvEvent, TableField } from 'bootstrap-vue-3'

    import { onMounted } from 'vue'
    import type { Ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { useToast } from 'vue-toastification'

    import WaitOverlay from '../../components/custom/WaitOverlay.vue'

    type SearchParam = PaginationOptions

    const router = useRouter()
    const productModalShow = ref(false)
    const showWaitOverlay = ref<boolean>(true)
    const itemLoading = ref(false)
    const itemStore = useInvoiceStore()
    const emission: Ref<string> = ref(new Date().toUTCString().slice(0, 10))
    const endDate: Ref<string> = ref(new Date().toUTCString().slice(0, 10))
    //const toast = useToast()
    const filterText = ref<string>('')
    const itemInfoShow = ref<boolean>(false)
    const toast = useToast()

    const templateList = ref<
        {
            label: string
            value: 'emission' | 'created' | 'cid' | 'name'
        }[]
    >([
        //{ label: 'Por creador', value: 'created' },
        { label: 'Por tipo de ID', value: 'cid' },
        { label: 'Por Nombres y apellidos', value: 'name' },
        { label: 'Por fecha de creación', value: 'emission' },
    ])
    const filterName = ref(templateList.value[0])
    type SelectedItem = { item: Invoice | null }
    const detailSelectedItem = ref<SelectedItem>({
        item: null,
    })

    const formFields: TableField[] = [
        '#',
        { label: 'Secuencia', key: 'code' },
        { label: 'Emisión', key: 'emission' },
        'Cliente',
        { label: 'Cedúla Cliente', key: 'cid' },
        { label: 'Metodo de pago', key: 'name' },
        { label: 'Subtotal', key: 'subtotal' },
        { label: 'Total IVA', key: 'iva' },
        { label: 'Total', key: 'total' },

        'Acciones',
    ]

    const form = ref<Form>({
        items: [],
    })
    const formFiltres = ref<Form>({
        items: [],
    })
    type Form = {
        items: Invoice[]
    }
    type DeleteInvoice = {
        id: number
        index: number
    }

    const itemForm = ref<DeleteInvoice>({
        id: 0,
        index: 0,
    })
    const model = ref({})
    /*Pagination*/
    const perPage = ref(10)

    const searchParam: SearchParam = {
        page: 1,

        per_page: 10,
    }
    function cleanFilters() {
        filterText.value = ''
        formFiltres.value.items.splice(0, formFiltres.value.items.length)
        showInvoices()
    }
    function makeSearch(valor: any) {
        itemStore.providers?.data.splice(0, itemStore.providers?.data.length)
        if (filterText.value != '') {
            showWaitOverlay.value = true
            itemStore
                .getAllInvoice()
                .then(response => {
                    formFiltres.value.items = []
                    formFiltres.value.items = response.data
                    itemStore.providers?.data.splice(
                        0,
                        itemStore.providers?.data.length
                    )
                    for (let i = 0; i < formFiltres.value.items.length; i++) {
                        if (
                            (filterText.value ==
                                (formFiltres.value.items[i].client as IClient)
                                    .name &&
                                valor == 'name') ||
                            (filterText.value ==
                                (formFiltres.value.items[i].client as IClient)
                                    .number_id &&
                                valor == 'cid')
                        ) {
                            console.log('entre')
                            itemStore.providers?.data.push(
                                formFiltres.value.items[i]
                            )
                        }
                    }

                    showWaitOverlay.value = false
                })
                .catch((e: Error) => {
                    console.log(e)
                })
        }
        if (filterText.value == '' && valor == 'emission') {
            showWaitOverlay.value = true

            itemStore
                .getAllInvoice()
                .then(response => {
                    formFiltres.value.items = []
                    formFiltres.value.items = response.data
                    itemStore.providers?.data.splice(
                        0,
                        itemStore.providers?.data.length
                    )
                    for (let i = 0; i < formFiltres.value.items.length; i++) {
                        if (
                            new Date(formFiltres.value.items[i].emission) >=
                                new Date(emission.value) &&
                            new Date(formFiltres.value.items[i].emission) <=
                                new Date(endDate.value)
                        ) {
                            itemStore.providers?.data.push(
                                formFiltres.value.items[i]
                            )
                        }
                    }

                    showWaitOverlay.value = false
                })
                .catch((e: Error) => {
                    console.log(e)
                })
        }
    }
    function showInvoices() {
        showWaitOverlay.value = true

        itemStore
            .fetchProviders(searchParam)
            .catch(() => {
                toast.error('No se pudo realizar la búsqueda ')
            })
            .finally(() => {
                if (itemStore.providers?.data !== undefined) {
                    form.value.items = itemStore.providers?.data
                }
                //(
                //as PaginatedResponse<Invoice>
                //).data
                console.log(form.value.items)
                showWaitOverlay.value = false
            })
    }
    function onPaginationClick(event: BvEvent, page: number) {
        searchParam.page = page
        console.log(page)
        showInvoices()
    }

    function onShowModalClick() {
        showInvoices()
    }
    async function showItem(item: Invoice) {
        detailSelectedItem.value.item = item
        itemInfoShow.value = true
    }
    function removeItem(index: number) {
        console.log(index)
        form.value.items.splice(index, 1)
    }
    function deleteProduct(): void {
        itemStore.removeInvoice(itemForm.value.id)
        removeItem(itemForm.value.index)
    }

    function go(): void {
        router.push({ path: '/facturacion/agregar' })
    }
    function goEdit(id: number): void {
        console.log(id)
        router.push({ path: `/facturacion/editar/${String(id)}` })
    }
    function onSubmit(id: number, index: number) {
        itemForm.value.id = id
        itemForm.value.index = index
        productModalShow.value = true
    }

    showInvoices()
</script>

<template>
    <main>
        <ModalDialog
            id="product-modal"
            v-model:show="productModalShow"
            title="Anular Facturar"
            ok-text="Aceptar"
            @ok="deleteProduct()"
            button-type="ok-cancel">
            <h1 style="font-size: 15px; color: black; text-align: left">
                ¿Está seguro de anular la factura?
            </h1>
        </ModalDialog>
        <ModalDialog v-model:show="itemInfoShow" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl">Detalle de la factura </b>
            </template>
            <div class="container">
                <div
                    class="row tw-pb-3 align-content-center justify-content-center gy-2">
                    <template
                        v-for="(d, k) in detailSelectedItem.item"
                        :key="k">
                        <div class="row" v-if="k == 'client'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >cliente:</span
                            >
                            <span class="col-6">{{ (d as IClient).name }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'payment_method'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >metodo de pago:</span
                            >
                            <span class="col-6">{{
                                (d as IPayment).name
                            }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'subtotal'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >subtotal:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'iva'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >total IVA:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>

                        <div class="row" v-if="k == 'total'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >total:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>

                        <div class="row" v-if="k == 'created_at'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >fecha de creación:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                    </template>
                </div>
            </div>
        </ModalDialog>

        <ECard>
            <ERow>
                <h1 style="font-size: 35px; color: black">Facturas</h1>
            </ERow>
            <nav class="navbar">
                <div class="container-fluid">
                    <EButton variant="secondary" @click="go"
                        >+ Agregar factura
                    </EButton>
                    <ECol cols="9" md="6" xl="4">
                        <ListBox
                            v-model="filterName"
                            :clearable="true"
                            top-label="Seleccione un filtro"
                            :options="templateList" />
                    </ECol>
                    <ECol cols="9" md="6" xl="2" class="mt-3">
                        <InputText
                            label="Fecha Min"
                            type="date"
                            v-model="emission"
                            :readonly="filterName.value != 'emission'" />
                    </ECol>
                    <ECol cols="9" md="6" xl="2" class="mt-3">
                        <InputText
                            label="Fecha Max"
                            type="date"
                            v-model="endDate"
                            :readonly="filterName.value != 'emission'" />
                    </ECol>
                </div>
                <div
                    class="container-fluid"
                    style="justify-content: flex-end; align-items: stretch">
                    <ECol cols="9" md="6" xl="3" class="mt-3">
                        <InputText
                            v-model="filterText"
                            label="Cuadro de búsqueda"
                            :placeholder="`Búsqueda por ${filterName.label}`"
                            :readonly="filterName.value == 'emission'" />
                    </ECol>
                    <ECol cols="9" md="6" xl="1" class="mt-4">
                        <EButton
                            class="mt-4 tw-ml-4"
                            @click="makeSearch(`${filterName.value}`)"
                            >Buscar</EButton
                        >
                    </ECol>
                    <ECol cols="9" md="6" xl="1" class="mt-4">
                        <EButton class="mt-4" @click="cleanFilters"
                            >Limpiar</EButton
                        >
                    </ECol>
                </div>
            </nav>

            <!-- <ERow>
                <ECol cols="12"> -->
            <WaitOverlay :show="showWaitOverlay">
                <BTable :fields="formFields" :items="itemStore.providers?.data">
                    <template #cell(#)="{ index }">{{ index + 1 }} </template>
                    <template #cell(Cliente)="{ index }"
                        >{{
                            (
                                itemStore.providers?.data[index][
                                    'client'
                                ] as IClient
                            ).name
                        }}
                    </template>
                    <template #cell(cid)="{ index }"
                        >{{
                            (
                                itemStore.providers?.data[index][
                                    'client'
                                ] as IClient
                            ).number_id
                        }}
                    </template>
                    <template #cell(name)="{ index }"
                        >{{
                            (
                                itemStore.providers?.data[index][
                                    'payment_method'
                                ] as IPayment
                            ).name
                        }}
                    </template>

                    <template #cell(Acciones)="{ item, index }">
                        <div class="t-button-group">
                            <e-button
                                left-icon="fa-eye"
                                variant="secondary"
                                @click="showItem(item)"
                                >Ver detalles</e-button
                            >
                            <e-button
                                left-icon="fa-edit"
                                variant="success"
                                @click="goEdit(item['id'])"
                                >Editar</e-button
                            >
                            <e-button
                                left-icon="fa-cancel"
                                variant="cancel"
                                @click="onSubmit(item['id'], index)">
                                <span
                                    class="tw-invisible md:tw-visible tw-font-bold"
                                    >Anular</span
                                ></e-button
                            >
                        </div>
                    </template>
                </BTable>
                <div class="row">
                    <BPagination
                        align="center"
                        v-model="searchParam.page"
                        :total-rows="itemStore.providers?.total ?? 1"
                        :per-page="searchParam.per_page ?? 10"
                        next-text="Siguiente"
                        prev-text="Anterior"
                        class="paginator"
                        hide-goto-end-buttons
                        @page-click="onPaginationClick" />
                </div>
            </WaitOverlay>
        </ECard>
    </main>
</template>
