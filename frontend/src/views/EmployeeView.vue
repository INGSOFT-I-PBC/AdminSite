<script setup lang="ts">
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import ERow from '@components/custom/ERow.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import Table from '@components/holders/Table.vue'

    import { reactive } from 'vue'
    import { useRouter } from 'vue-router'

    const router = useRouter()

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
                id: '09467493043',
                name: 'Dennisse Aguirre',
            },
        ],
    })

    interface productModel {
        date: string
        hour: string
        create: string
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
        router.push({ path: '/usuarios/empleado/agregar' })
    }

    function go3(): void {
        router.push({ path: '/usuarios/empleado/agregar' })
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
            title="Detalle del empleado">
            <h1>nombre: {{ selectedProduct?.name }}</h1>
            <span>Cantidad: ${{ selectedProduct?.id }}</span>
        </ModalDialog>

        <ECard>
            <ERow>
                <h1 style="font-size: 35px; color: black">Empleados</h1>
            </ERow>
            <nav class="navbar">
                <div class="container-fluid">
                    <EButton variant="secondary" @click="go"
                        >+ Agregar empleado
                    </EButton>

                    <form class="d-flex" role="search">
                        <input
                            class="form-control me-2"
                            type="search"
                            placeholder="Buscar empleado"
                            aria-label="Search" />
                        <button class="btn btn-outline-black" type="submit">
                            Search
                        </button>
                    </form>

                    <EButton @click="rol">Roles</EButton>
                </div>
            </nav>

            <!-- <ERow>
                <ECol cols="12"> -->

            <Table :header="tableSettings">
                <template #body-cell="{ cellData, colIdx, rowIdx }">
                    <div v-if="colIdx == 5">
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
                        v-else-if="colIdx > 5"
                        class="tw-grid tw-grid-flow-col tw-rounded tw-overflow-hidden">
                        <button
                            class="tw-bg-blue-600 tw-px-4 tw-py-1 tw-text-white"
                            @click="showProduct(cellData as productModel)">
                            Ver más detalles
                        </button>
                        <button
                            class="tw-bg-green-600 tw-py-1 tw-text-white"
                            @click="go3">
                            Editar
                        </button>
                        <button
                            class="tw-bg-red-600 tw-py-1 tw-text-white"
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
