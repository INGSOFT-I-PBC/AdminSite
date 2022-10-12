<script lang="ts">
    import { defineComponent } from 'vue'
    import ItemDataService from '@/store/item'
    import type Item from '@/interfaz/items'
    import type Item3 from '@/interfaz/Items3'
</script>

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
    import { computed, reactive, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    //useAuthStore().refreshToken()
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
    //const idx = 10

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
        rows: [],
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
    interface product {
        code: number
        name: string
        marc: string
        model: string
        category: string | number
        descrip: string
        price: string | number
        stock: string | number
        state: number | string
        actions: number | string
        id: number
    }
    let items: Item[]
    const items2: product[] = []

    async function showAllProducts() {
        ItemDataService.getAll()
            .then(response => {
                items = response.data
                console.log(items)

                for (let i = 0; i < items.length; i++) {
                    items2.push({
                        code: items[i].codename_Item,
                        name: items[i].nombreItem,
                        marc: items[i].brandItem,
                        model: items[i].modelItem,
                        category: items[i].category_name_Item,
                        descrip: items[i].brandItem,
                        price: items[i].priceItem,
                        stock: items[i].quantity,
                        state: items[i].status_id_Item,
                        actions: items[i].item_id,
                        id: items[i].id,
                    })
                }

                tableSettings.rows = items2
                console.log(tableSettings.rows)
            })
            .catch((e: Error) => {
                console.log(e)
            })
    }

    function go(id: number): void {
        console.log(id)
        router.push({ path: `/inventario/editar/${String(id)}` })
    }
    function goAgregar(): void {
        router.push({ path: '/inventario/agregar' })
    }
    onMounted(() => {
        return showAllProducts()
    })
</script>

<template>
    <main>
        <ModalDialog
            id="product-modal"
            v-model:show="productModalShow"
            title="Detalle del producto">
            <h1>nombre: {{ selectedProduct?.name }}</h1>
        </ModalDialog>

        <ECard>
            <ERow>
                <h1 style="font-size: 35px; color: black">Inventario</h1>
            </ERow>
            <nav class="navbar">
                <div class="container-fluid">
                    <EButton type="secondary" @click="goAgregar"
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
                    <div v-if="colIdx == 8">
                        <div class="form-check form-switch">
                            <input
                                v-if="items2[rowIdx].state == 1"
                                class="form-check-input"
                                type="checkbox"
                                role="switch"
                                id="flexSwitchCheckDefault"
                                checked />
                            <input
                                v-else
                                class="form-check-input"
                                type="checkbox"
                                role="switch"
                                id="flexSwitchCheckDefault" />
                            <label
                                class="form-check-label"
                                for="flexSwitchCheckDefault"></label>
                        </div>
                    </div>

                    <div
                        v-else-if="colIdx > 8"
                        class="tw-grid tw-grid-flow-col tw-rounded tw-overflow-hidden">
                        <button
                            class="tw-bg-blue-600 tw-px-4 tw-py-1 tw-text-white"
                            @click="showProduct(cellData as productModel)">
                            Ver más detalles
                        </button>
                        <button
                            class="tw-bg-green-600 tw-py-1 tw-text-white"
                            @click="go(items2[rowIdx].id)">
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
