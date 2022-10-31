<script setup lang="ts">
    import ECard from '@components/custom/ECard.vue'
    import ERow from '@components/custom/ERow.vue'
    import ECol from '@components/custom/ECol.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import EButton from '@components/custom/EButton.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import WaitOverlay from '../../components/custom/WaitOverlay.vue'
    import { onMounted } from 'vue'

    import type { Invoice } from '@store/types'
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
        'Cliente',
        'Cajero',
        { label: 'Metodo de pago', key: 'name' },
        { label: 'Total', key: 'total' },
        { label: 'Subtotal', key: 'subtotal' },
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
        itemStore.removeInvoice(id)
        removeItem(index)
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
                            <span class="col-6">{{
                                detailSelectedItem?.item?.client?.name
                            }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'payment_method'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >metodo de pago:</span
                            >
                            <span class="col-6">{{
                                detailSelectedItem?.item?.payment_method?.name
                            }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'subtotal'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >dirección:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>

                        <div class="row" v-if="k == 'total'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >email:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                        <div class="row" v-if="k == 'created_by'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >cajero:</span
                            >
                            <span class="col-6"> {{ detailSelectedItem?.item?.created_by?.name }} {{ detailSelectedItem?.item?.created_by?.lastname }}</span>
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
                    <EButton type="secondary" @click="go"
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
                        >{{ form.items[index]['client']?.name }}
                    </template>
                    <template #cell(Cajero)="{ index }"
                        >{{ form.items[index]['created_by']?.name }}
                    </template>
                    <template #cell(name)="{ index }"
                        >{{ form.items[index]['payment_method']?.name }}
                    </template>

                    <template #cell(Acciones)="{ item, index }">
                        <div class="t-button-group">
                            <e-button
                                left-icon="fa-eye"
                                type="secondary"
                                @click="showItem(item)"
                                >Ver detalles</e-button
                            >
                            <e-button
                                left-icon="fa-edit"
                                type="success"
                                @click="goEdit(item['id'])"
                                >Editar</e-button
                            >
                            <e-button
                                left-icon="fa-trash-can"
                                type="cancel"
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
