<script setup lang="ts">
    import ECard from '@components/custom/ECard.vue'
    import ERow from '@components/custom/ERow.vue'
    import ECol from '@components/custom/ECol.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import EButton from '@components/custom/EButton.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import WaitOverlay from '../../components/custom/WaitOverlay.vue'
    import { onMounted } from 'vue'

    import type { IClient, Invoice, IPayment } from '@store/types'
    import { useInvoiceStore } from '@store/invoice'
    //import { useToast } from 'vue-toastification'

    import type { TableField } from 'bootstrap-vue-3'

    import { useRouter } from 'vue-router'
    const router = useRouter()
    const showWaitOverlay = ref<boolean>(true)
    const itemLoading = ref(false)
    const itemStore = useInvoiceStore()
    //const toast = useToast()
    const itemInfoShow = ref<boolean>(false)
    const invoiceModalDelete = ref(false)
    const id2 = ref(0)
    const index2 = ref(0)

    const templateList = [
        { label: 'Por fecha de creación', value: '1' },
        { label: 'Por creador', value: '2' },
        {
            label: 'Por tipo de ID',
            value: '3',
        },
        { label: 'Por Nombres y apellidos', value: '4' },
    ]
    type SelectedItem = { item: Invoice | null }
    const detailSelectedItem = ref<SelectedItem>({
        item: null,
    })

    const formFields: TableField[] = [
        '#',
        { label: 'Secuencia', key: 'code' },

        'Cliente',
        { label: 'Metodo de pago', key: 'name' },
        { label: 'Subtotal', key: 'subtotal' },
        { label: 'Total IVA', key: 'iva' },
        { label: 'Total', key: 'total' },

        'Acciones',
    ]

    const form = ref<Form>({
        items: [],
    })
    type Form = {
        items: Invoice[]
    }
    /*type ItemForm = {
        item: Client | null
    }

    const itemForm = ref<ItemForm>({
        item: null,
    })*/
    const model = ref({})

    const loadItems = async () => {
        itemLoading.value = true
        form.value.items = await itemStore.fetchAllInvoice()
        console.log(form.value.items)
        itemLoading.value = false
        showWaitOverlay.value = false
    }
    function onShowModalClick() {
        loadItems()
    }
    async function showItem(item: Invoice) {
        detailSelectedItem.value.item = item
        itemInfoShow.value = true
    }
    function removeItem(index: number) {
        console.log(index)
        form.value.items.splice(index, 1)
    }
    function deleteProduct(id: number, index: number): void {
        id2.value = id
        index2.value = index
        invoiceModalDelete.value = true
    }
    function acceptace(): void {
        itemStore.removeInvoice(id2)
        removeItem(index2)
        id2.value = 0
        index2.value = 0
    }

    function go(): void {
        router.push({ path: '/facturacion/agregar' })
    }
    function goEdit(id: number): void {
        console.log(id)
        router.push({ path: `/facturacion/editar/${String(id)}` })
    }

    onMounted(() => {
        return onShowModalClick()
    })
</script>

<template>
    <main>
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

        <ModalDialog
            id="invoice-modal"
            v-model:show="invoiceModalDelete"
            title="Anular Factura"
            ok-text="Anular"
            @ok="acceptace"
            button-type="ok-cancel">
            <h1 style="font-size: 15px; color: black; text-align: left">
                ¿Está seguro de anular la Factura ?
            </h1>
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
                            v-model="model"
                            top-label="Seleccione un filtro"
                            :options="templateList" />
                    </ECol>
                    <form class="d-flex" role="search">
                        <input
                            class="form-control me-2"
                            type="search"
                            placeholder="Buscar cliente"
                            aria-label="Search" />
                        <button class="btn btn-outline-black" type="submit">
                            Search
                        </button>
                    </form>
                </div>
            </nav>

            <!-- <ERow>
                <ECol cols="12"> -->
            <WaitOverlay :show="showWaitOverlay">
                <BTable :fields="formFields" :items="form.items">
                    <template #cell(#)="{ index }">{{ index + 1 }} </template>
                    <template #cell(Cliente)="{ index }"
                        >{{ (form.items[index]['client'] as IClient).name }}
                    </template>
                    <template #cell(name)="{ index }"
                        >{{
                            (form.items[index]['payment_method'] as IPayment)
                                .name
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
                                left-icon="fa-trash-can"
                                variant="cancel"
                                @click="deleteProduct(item['id'], index)">
                                <span
                                    class="tw-invisible md:tw-visible tw-font-bold"
                                    >Eliminar</span
                                ></e-button
                            >
                        </div>
                    </template>
                </BTable>
            </WaitOverlay>
        </ECard>
    </main>
</template>
