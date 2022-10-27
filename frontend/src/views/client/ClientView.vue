<script setup lang="ts">
    import ECard from '@components/custom/ECard.vue'
    import ERow from '@components/custom/ERow.vue'
    import ECol from '@components/custom/ECol.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import EButton from '@components/custom/EButton.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import WaitOverlay from '../../components/custom/WaitOverlay.vue'
    import { onMounted } from 'vue'

    import type { Client } from '@store/types'
    import { useClientStore } from '@store/client'
    //import { useToast } from 'vue-toastification'

    import type { TableField } from 'bootstrap-vue-3'

    import { useRouter } from 'vue-router'
    const router = useRouter()
    const showWaitOverlay = ref<boolean>(true)
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

    const model = ref({})

    const loadItems = async () => {
        itemLoading.value = true
        form.value.items = await itemStore.fetchAllClient()
        itemLoading.value = false
        showWaitOverlay.value = false
    }
    function onShowModalClick() {
        loadItems()
    }
    async function showItem(item: Client) {
        detailSelectedItem.value.item = item
        itemInfoShow.value = true
    }
    function removeItem(index: number) {
        form.value.items.splice(index, 1)
    }
    function deleteProduct(id: number, index: number): void {
        itemStore.removeClient(id)
        removeItem(index)
    }

    function go(): void {
        router.push({ path: '/usuarios/cliente/agregar' })
    }
    function goEdit(id: number): void {
        router.push({ path: `/usuarios/cliente/editar/${String(id)}` })
    }

    onMounted(() => {
        return onShowModalClick()
    })
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


        <ECard>

            <ERow>
                <h1 class="tw-text-black first-line:dark:tw-text-neutral-300" style="font-size: 35px; color: black">Clientes</h1>
            </ERow>
            <nav class="navbar">
                <div class="container-fluid align">
                    <EButton type="secondary" @click="go"
                        >+ Agregar cliente
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
<style lang="scss">
    .align {
        padding: 0;
    }
    .table {
            > thead {
                @apply tw-bg-secondary tw-text-white tw-font-bold;
            }
            @media (prefers-color-scheme: dark) {
                color: white !important;
                --bs-table-striped-color: theme(colors.zinc.400);
                --bs-table-hover-color: theme('colors.primary.light');
                --bs-table-hover-bg: theme(colors.primary.light / 15%);
            }
        }
    .t-button-group {
        max-width: fit-content !important;
        @apply tw-rounded tw-overflow-hidden tw-flex tw-place-content-stretch tw-place-items-stretch;
        > button {
            padding: 0;
            border-radius: 0.3rem;
            margin-left: 0.5rem;
            min-width: auto;
            max-width: 100%;
        }
    }
</style>
