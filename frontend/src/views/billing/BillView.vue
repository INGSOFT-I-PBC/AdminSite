<script setup lang="ts">
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import ECol from '@components/custom/ECol.vue'
    import ERow from '@components/custom/ERow.vue'
    import InputText from '@components/custom/InputText.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import Title from '@components/custom/Title.vue'
    import Table from '@components/holders/Table.vue'

    import { computed, reactive } from 'vue'
    import { useRouter } from 'vue-router'

    const router = useRouter()

    const templateList = [
        { label: 'Por código', value: '1' },
        { label: 'Por cliente', value: '2' },
        {
            label: 'Por fecha de emisión',
            value: '3',
        },
    ]

    const model = ref({})
    const productModalShow = ref(false)
    const tableSettings = reactive<TableHeaderSettings>({
        headers: [
            {
                label: 'Código de factura',
                attribute: 'id',
            },
            {
                label: 'Estado',
                attribute: 'state',
            },
            {
                label: 'Cajero ',
                attribute: 'employee',
            },
            {
                label: 'Cliente',
                attribute: 'client',
            },
            {
                label: 'Fecha de emisión',
                attribute: 'date',
            },
            {
                label: 'Total',
                attribute: 'total',
            },
            {
                label: 'Acciones',
                attribute: 'actions',
            },
        ],
        rows: [
            {
                id: '250222',
                state: 'Activa',
                employee: 'Alejandra Quimi',
                client: 'Carlos Arévalo',
                date: '28/09/2022',
                total: '19.99',
            },
        ],
    })

    interface productModel {
        id: string
        state: string
        employee: string
        client: string
        date: string
        total: string
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
        router.push({ path: '/facturacion/agregar' })
    }

    function go3(): void {
        router.push({ path: '/facturacion/agregar' })
    }
</script>

<template>
    <main>
        <ModalDialog
            id="client-modal"
            v-model:show="productModalShow"
            title="Detalle de la factura">
            <span>Cantidad: ${{ selectedProduct?.id }}</span>
        </ModalDialog>

        <ECard>
            <ERow>
                <h1 style="font-size: 35px; color: black">Facturas</h1>
            </ERow>
            <nav class="navbar">
                <div class="container-fluid" style="padding: 0">
                    <EButton variant="secondary" @click="go"
                        >+ Crear factura
                    </EButton>
                    <EButton variant="secondary" @click="go"
                        >Notas de crédito
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
                            placeholder="Buscar factura"
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
                    <div
                        v-if="colIdx > 5"
                        class="tw-grid tw-grid-flow-col tw-rounded tw-overflow-hidden">
                        <button
                            class="tw-bg-blue-600 tw-py-1 tw-text-white tw-mx-2 tw-rounded"
                            @click="showProduct(cellData as productModel)">
                            Ver más detalles
                        </button>
                        <button
                            class="tw-bg-green-600 tw-py-1 tw-text-white tw-mx-2 tw-rounded"
                            @click="go3">
                            Editar
                        </button>
                        <button
                            class="tw-bg-red-600 tw-py-1 tw-text-white tw-mx-2 tw-rounded"
                            @click="removeItem(rowIdx)">
                            Anular
                        </button>
                    </div>
                </template>
            </Table>

            <!-- </ECol>
            </ERow> -->
        </ECard>
    </main>
</template>
