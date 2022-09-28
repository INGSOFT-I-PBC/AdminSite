<script setup lang="ts">
   import ECard from '@components/custom/ECard.vue'
    import ERow from '@components/custom/ERow.vue'
    import ECol from '@components/custom/ECol.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import InputText from '@components/custom/InputText.vue'
    import EButton from '@components/custom/EButton.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import Title from '@components/custom/Title.vue'
    import Table from '@components/holders/Table.vue'
    import { computed, reactive } from 'vue'

    import { useRouter } from 'vue-router'
    const router = useRouter()

    const templateList = [
        { label: 'Por fecha de creación', value: '1' },
        { label: 'Por tipo de identificación', value: '2' },
        { label: 'Por Nombres y Apellidos', value: '3' },
        { label: 'Por creador', value: '4' },
    ]


    const model = ref(null)
    const productModalShow = ref(false)
    // const selectedProduct = null
    const tableSettings = reactive<TableHeaderSettings>({
        headers: [
            {
                label: 'Fecha de creación',
                attribute: 'date',
            },
            {
                label: 'Hora de creación',
                attribute: 'hour',
            },
            {
                label: 'Creado por ',
                attribute: 'create',
            },
            {
                label: 'Tipo de identificación',
                attribute: 'type_id',
            },
            {
                label: 'Identificación',
                attribute: 'id',
            },
            {
                label: 'Nombres y Apellidos',
                attribute: 'name',
            },
            {
                label: 'Estado',
                attribute: 'estado',
            },
            {
                label: 'Acciones',
                attribute: 'actions',
            },
        ],
        rows: [
            {
                date: '12/03/2022',
                hour: '15:00',
                create: 'Admin',
                type_id:'cédula',
                id: '09467493043',
                name: 'Pamela Rugel',
            },
        ],
    })

    interface productModel {
        date: string
        hour: string
        create: string
        type_id:string
        id: string
        name: string
    }
    let selectedProduct: Optional<productModel> = null
    function showProduct(product: productModel) {
        selectedProduct = product
        console.log(selectedProduct)
        productModalShow.value = true
    }
    function removeItem(index: number) {
        tableSettings.rows?.splice(index, 1)
    }

    function go(): void {
        router.push({ path: '/usuarios/cliente/agregar' })
    }

    function go3(): void {
        router.push({ path: '/usuarios/cliente/agregar' })
    }

    function rol(): void {
        router.push({ path: '/admin/roles' })
    }
</script>

<template>
    <main>
        <ModalDialog
            id="employee-modal"
            v-model:show="productModalShow"
            title="Detalle del cliente">
            <h1>nombre: {{ selectedProduct?.name }}</h1>
            <span>Cantidad: ${{ selectedProduct?.id }}</span>
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

            <Table :header="tableSettings">
                <template #body-cell="{ cellData, colIdx, rowIdx }">
                    <div v-if="colIdx == 6">
                        <div class="form-check form-switch">
                            <input
                                class="form-check-input"
                                type="checkbox"
                                role="switch"
                                id="flexSwitchCheckDefault"
                                checked />
                            <label
                                class="form-check-label"
                                for="flexSwitchCheckDefault"></label>
                        </div>
                    </div>

                    <div
                        v-else-if="colIdx > 6"
                        class="tw-grid tw-grid-flow-col tw-rounded tw-overflow-hidden">
                        <button
                            class="tw-bg-blue-500 tw-px-4 tw-py-1 tw-text-white"
                            @click="showProduct(cellData as productModel)">
                            Ver más detalles
                        </button>
                        <button
                            class="tw-bg-green-500 tw-py-1 tw-text-white"
                            @click="go3">
                            Editar
                        </button>
                        <button
                            class="tw-bg-red-500 tw-py-1 tw-text-white"
                            @click="removeItem(rowIdx)">
                            Eliminar
                        </button>
                    </div>
                </template>
            </Table>

            <!-- </ECol>
            </ERow> -->
        </ECard>
    </main>
</template>
