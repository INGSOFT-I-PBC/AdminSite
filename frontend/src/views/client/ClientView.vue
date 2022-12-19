<script setup lang="ts">
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import ECol from '@components/custom/ECol.vue'
    import ERow from '@components/custom/ERow.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import { useClientStore } from '@store/client'
    import type { Client } from '@store/types'
    //import { useToast } from 'vue-toastification'
    import type { BvEvent, TableField } from 'bootstrap-vue-3'

    import { onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { useToast } from 'vue-toastification'

    import WaitOverlay from '../../components/custom/WaitOverlay.vue'

    type SearchParam = PaginationOptions
    const router = useRouter()
    const toast = useToast()
    const showWaitOverlay = ref<boolean>(true)
    const itemLoading = ref(false)
    const itemStore = useClientStore()
    const clientModalShow = ref(false)
    let id2 = 0
    let index2 = 0
    const clientModalDelete = ref(false)
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

    const model = ref({})
    //Paginated
    const searchParam: SearchParam = {
        page: 1,

        per_page: 10,
    }

    const loadItems = async () => {
        itemLoading.value = true
        showWaitOverlay.value = true
        itemStore
            .fetchClientPaginated(searchParam)
            .then(() => {
                if (itemStore.clients?.data !== undefined) {
                    form.value.items = itemStore.clients?.data
                }
                console.log('qqqq')
                console.log(form.value.items)
            })
            .catch(() => {
                toast.error('No se pudo realizar la búsqueda ')
            })
            .finally(() => {
                showWaitOverlay.value = false
            })
        console.log(form.value.items)
        itemLoading.value = false
    }
    function onPaginationClick(event: BvEvent, page: number) {
        searchParam.page = page
        console.log(page)
        loadItems()
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
        form.value.items.splice(index, 1)
    }
    function deleteProduct(id: number, index: number): void {
        id2 = id
        index2 = index
        clientModalDelete.value = true
    }

    function acceptace(): void {
        itemStore.removeClient(id2)
        removeItem(index2)
        id2 = 0
        index2 = 0
    }

    function go(): void {
        router.push({ path: '/usuarios/cliente/agregar' })
    }
    function goEdit(id: number): void {
        router.push({ path: `/usuarios/cliente/editar/${String(id)}` })
    }
    loadItems()
</script>

<template>
    <main>
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
        <ModalDialog
            id="client-modal"
            v-model:show="clientModalDelete"
            title="Eliminar Cliente"
            ok-text="Eliminar"
            @ok="acceptace"
            button-type="ok-cancel">
            <h1 style="font-size: 15px; color: black; text-align: left">
                ¿Está seguro de eliminar al Cliente?
            </h1>
        </ModalDialog>

        <ECard>
            <ERow>
                <h1
                    class="tw-text-black first-line:dark:tw-text-neutral-300"
                    style="font-size: 35px; color: black">
                    Clientes
                </h1>
            </ERow>
            <nav class="navbar">
                <div class="container-fluid align_button">
                    <EButton variant="secondary" @click="go">
                        + Agregar cliente
                    </EButton>
                    <!--

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
                    -->
                </div>
            </nav>

            <!-- <ERow>
                <ECol cols="12"> -->
            <WaitOverlay :show="showWaitOverlay">
                <BTable :fields="formFields" :items="itemStore.clients?.data">
                    <template #cell(#)="{ index }">{{ index + 1 }} </template>
                    <template #cell(Ciudad)="{ item }"
                        >{{ item.city?.name }}
                    </template>
                    <template #cell(Acciones)="{ item, index }">
                        <div class="t-button-group">
                            <e-button
                                left-icon="fa-eye"
                                variant="secondary"
                                @click="showItem(item)"
                                >Ver detalles
                            </e-button>
                            <e-button
                                left-icon="fa-edit"
                                variant="success"
                                @click="goEdit(item['id'])"
                                >Editar
                            </e-button>
                            <e-button
                                left-icon="fa-trash-can"
                                variant="cancel"
                                @click="deleteProduct(item['id'], index)">
                                <span
                                    class="tw-invisible md:tw-visible tw-font-bold"
                                    >Eliminar</span
                                >
                            </e-button>
                        </div>
                    </template>
                </BTable>
                <div class="row">
                    <BPagination
                        align="center"
                        v-model="searchParam.page"
                        :total-rows="itemStore.clients?.total ?? 1"
                        :per-page="searchParam.per_page ?? 10"
                        next-text="Siguiente"
                        prev-text="Anterior"
                        hide-goto-end-buttons
                        class="paginator"
                        @page-click="onPaginationClick" />
                </div>
            </WaitOverlay>
        </ECard>
    </main>
</template>
<style lang="scss">
    .align_button {
        padding: 0;
    }
</style>
