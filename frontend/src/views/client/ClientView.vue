<script setup lang="ts">
    import ECard from '@components/custom/ECard.vue'
    import ERow from '@components/custom/ERow.vue'
    import ECol from '@components/custom/ECol.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import EButton from '@components/custom/EButton.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'

    import { onMounted } from 'vue'

    import type { Client } from '@store/types'
    import { useClientStore } from '@store/client'
    //import { useToast } from 'vue-toastification'

    import type { TableField } from 'bootstrap-vue-3'

    import { useRouter } from 'vue-router'
    const router = useRouter()
    const itemLoading = ref(false)
    const itemStore = useClientStore()
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
    type SelectedItem = { item: Client | null }
    const detailSelectedItem = ref<SelectedItem>({
        item: null,
    })

    const formFields: TableField[] = [
        '#',
        { label: 'Identificacion', key: 'number_id' },
        { label: 'Nombres y Apellidos', key: 'name' },
        { label: 'Dirección', key: 'address' },
        { label: 'Email', key: 'email' },
        'Ciudad',
        'Acciones',
    ]

    const form = ref<Form>({
        items: [],
    })
    type Form = {
        items: Client[]
    }
    /*type ItemForm = {
        item: Client | null
    }

    const itemForm = ref<ItemForm>({
        item: null,
    })*/
    const model = ref({})
    //const productModalShow = ref(false)

    /*interface productModel {
        date: string
        hour: string
        create: string
        type_id: string
        id: string
        name: string
    }
    let selectedProduct: Optional<productModel> = null
    function showProduct(product: productModel) {
        selectedProduct = product
        console.log(selectedProduct)
        productModalShow.value = true
    }*/
    const loadItems = async () => {
        itemLoading.value = true
        form.value.items = await itemStore.fetchAllClient()
        console.log(form.value.items)
        itemLoading.value = false
    }
    function onShowModalClick() {
        loadItems()
    }
    async function showItem(item: Client) {
        detailSelectedItem.value.item = item
        itemInfoShow.value = true
    }
    function removeItem(index: number) {
        console.log(index)
        //tableSettings.rows?.splice(index, 1)
    }

    function go(): void {
        router.push({ path: '/usuarios/cliente/agregar' })
    }

    onMounted(() => {
        return onShowModalClick()
    })
</script>

<template>
    <main>
        <!--<ModalDialog
            id="client-modal"
            v-model:show="productModalShow"
            title="Detalle del cliente">
            <h1>nombre: {{ selectedProduct?.name }}</h1>
            <span>Cantidad: ${{ selectedProduct?.id }}</span>
        </ModalDialog>-->

        <ModalDialog v-model:show="itemInfoShow" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl"
                    >Detalle del Cliente {{ detailSelectedItem.item?.name }}</b
                >
            </template>
            <div class="container">
                <div
                    class="row tw-pb-3 align-content-center justify-content-center gy-2">
                    <template
                        v-for="(d, k) in detailSelectedItem.item"
                        :key="k">
                        <div class="row" v-if="k == 'number_id'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >cédula:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'name'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >nombre:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'address'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >dirección:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>

                        <div class="row" v-if="k == 'email'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >email:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                        <div class="row" v-if="k == 'phone_number'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >teléfono:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'city'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >ciudad:</span
                            >
                            <span class="col-6">{{
                                detailSelectedItem?.item?.city?.name
                            }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'province'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >provincia:</span
                            >
                            <span class="col-6">{{
                                detailSelectedItem?.item?.province?.name
                            }}</span>
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
                <h1 style="font-size: 35px; color: black">Clientes</h1>
            </ERow>
            <nav class="navbar">
                <div class="container-fluid">
                    <EButton type="secondary" @click="go"
                        >+ Agregar cliente
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
            <BTable :fields="formFields" :items="form.items">
                <template #cell(#)="{ index }">{{ index + 1 }} </template>
                <template #cell(Ciudad)="{ index }"
                    >{{ form.items[index]['city']?.name }}
                </template>
                <template #cell(Acciones)="{ item, index }">
                    <div class="t-button-group">
                        <e-button
                            left-icon="fa-eye"
                            type="secondary"
                            @click="showItem(item)"
                            >Ver detalles</e-button
                        >
                        <e-button left-icon="fa-edit" type="success"
                            >Editar</e-button
                        >
                        <e-button
                            left-icon="fa-trash-can"
                            type="cancel"
                            @click="removeItem(index)">
                            <span
                                class="tw-invisible md:tw-visible tw-font-bold"
                                >Eliminar</span
                            ></e-button
                        >
                    </div>
                </template>
            </BTable>
        </ECard>
    </main>
</template>
