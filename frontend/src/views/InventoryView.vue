<script setup lang="ts">
    import ECard from '@components/custom/ECard.vue'
    import ERow from '@components/custom/ERow.vue'
    import ECol from '@components/custom/ECol.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import EButton from '@components/custom/EButton.vue'
    import Table from '@components/holders/Table.vue'
    import { reactive } from 'vue'

    import { useRouter } from 'vue-router'
    const router = useRouter()

    const templateList = [
        { label: 'Por código', value: '1' },
        { label: 'Por nombre', value: '2' },
        {
            label: 'Por categoría',
            value: '3',
        },
        { label: 'Por cantidad', value: '4' },
    ]

    const model = ref({})
    const productModalShow = ref(false)
    // const selectedProduct = null
    const tableSettings = reactive<TableHeaderSettings>({
        headers: [
            {
                label: 'Código',
                attribute: 'code',
            },
            {
                label: 'Nombre',
                attribute: 'name',
            },
            {
                label: 'Marca ',
                attribute: 'marc',
            },
            {
                label: 'Modelo',
                attribute: 'model',
            },
            {
                label: 'Categoría',
                attribute: 'category',
            },
            {
                label: 'Descripción',
                attribute: 'descrip',
            },
            {
                label: 'Precio',
                attribute: 'price',
            },
            {
                label: 'Stock',
                attribute: 'stock',
            },
            {
                label: 'Estado',
                attribute: 'state',
            },
            {
                label: 'Acciones',
                attribute: 'actions',
            },
        ],
        rows: [
            {
                code: '250222',
                name: 'Zapatos',
                marc: 'Nike',
                model: 'Air',
                category: 'Mujer',
                descrip: 'Blanco con negro',
                price: '19.90',
                stock: '10',
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
        router.push({ path: '/inventario/agregar' })
    }
</script>

<template>
    <main>
        <ECard>
            <ERow>
                <h1 style="font-size: 35px; color: black">Inventario</h1>
            </ERow>
            <nav class="navbar">
                <div class="container-fluid">
                    <EButton type="secondary" @click="go"
                        >+ Agregar producto
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
                            placeholder="Buscar productos"
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
                        v-if="colIdx > 8"
                        class="tw-grid tw-grid-flow-col tw-rounded tw-overflow-hidden">
                        <button
                            class="tw-bg-blue-600 tw-px-4 tw-py-1 tw-text-white"
                            @click="showProduct(cellData)">
                            Ver más detalles
                        </button>
                        <button
                            class="tw-bg-green-600 tw-py-1 tw-text-white"
                            @click="removeItem(rowIdx)">
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
