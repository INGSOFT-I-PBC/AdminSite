<script setup lang="ts">
import type Item from '@/interfaz/items'
import ItemDataService from '@/store/item'
import EButton from '@components/custom/EButton.vue'
import ECard from '@components/custom/ECard.vue'
import ECol from '@components/custom/ECol.vue'
import ERow from '@components/custom/ERow.vue'
import ListBox from '@components/custom/ListBox.vue'
import ModalDialog from '@components/custom/ModalDialog.vue'
import Table from '@components/holders/Table.vue'
import { onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import WaitOverlay from '../../components/custom/WaitOverlay.vue'
const router = useRouter()
const showWaitOverlay = ref<boolean>(true)
//
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
const productModalDelete = ref(false)
let num = 0

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

const selectedProduct: Optional<any> = ref(null)
function showProduct(product: product) {
    selectedProduct.value = product
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
    id_item: number
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
                    id_item: items[i].item_id,
                    id: items[i].id,
                })
            }

            tableSettings.rows = items2
            showWaitOverlay.value = false

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

function acceptace(): void {
    ItemDataService.deleteInventory(items2[num].id)
        .then(response => {
            console.log(response.data)
            ItemDataService.deleteItem(items2[num].id_item).then(
                response => {
                    console.log(response.data)
                    removeItem(num)
                }
            )
        })
        .catch((e: Error) => {
            console.log(e)
        })
}

function deleteProduct(index: number): void {
    num = index
    productModalDelete.value = true
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
        <ModalDialog v-model:show="productModalShow" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl">Detalle del Producto {{ selectedProduct?.name }}</b>
            </template>
            <div class="container">
                <div class="row tw-pb-3 align-content-center justify-content-center gy-2">
                    <template v-for="(k, d) in selectedProduct" :key="k">
                        <div class="row" v-if="d.toString() == 'code'">
                            <span class="tw-w-1/2 tw-font-bold col-6">Codigo:</span>
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div class="row" v-if="d.toString() == 'name'">
                            <span class="tw-w-1/2 tw-font-bold col-6">Nombre:</span>
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div class="row" v-if="d.toString() == 'marc'">
                            <span class="tw-w-1/2 tw-font-bold col-6">Marca:</span>
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div class="row" v-if="d.toString() == 'model'">
                            <span class="tw-w-1/2 tw-font-bold col-6">Modelo:</span>
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div class="row" v-if="d.toString() == 'category'">
                            <span class="tw-w-1/2 tw-font-bold col-6">Categoria:</span>
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div class="row" v-if="d.toString() == 'price'">
                            <span class="tw-w-1/2 tw-font-bold col-6">Precio:</span>
                            <span class="col-6">{{ k }}</span>
                        </div>
                        <div class="row" v-if="d.toString() == 'stock'">
                            <span class="tw-w-1/2 tw-font-bold col-6">Stock:</span>
                            <span class="col-6">{{ k }}</span>
                        </div>
                    </template>
                </div>
            </div>
        </ModalDialog>
        <ModalDialog id="product-modal" v-model:show="productModalDelete" title="Eliminar Producto" ok-text="Eliminar"
            @ok="acceptace" button-type="ok-cancel">
            <h1 style="font-size: 15px; color: black; text-align: left">
                ¿Está seguro de eliminar el Producto?
            </h1>
        </ModalDialog>

        <ECard>
            <ERow>
                <h1 style="font-size: 35px; color: black">Inventario</h1>
            </ERow>
            <nav class="navbar">
                <div class="container-fluid">
                    <EButton variant="secondary" @click="goAgregar">+ Agregar producto
                    </EButton>

                    <ECol cols="9" md="6" xl="4">
                        <ListBox v-model="model" top-label="Seleccione un filtro" :options="templateList" />
                    </ECol>

                    <form class="d-flex" role="search">
                        <input class="form-control me-2" type="search" placeholder="Buscar productos"
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
                <Table :header="tableSettings">
                    <template #body-cell="{ colIdx, rowIdx }">
                        <div v-if="colIdx == 8">
                            <div class="form-check form-switch">
                                <input v-if="items2[rowIdx].state == 1" class="form-check-input" type="checkbox"
                                    role="switch" id="flexSwitchCheckDefault" checked />
                                <input v-else class="form-check-input" type="checkbox" role="switch"
                                    id="flexSwitchCheckDefault" checked />
                                <label class="form-check-label" for="flexSwitchCheckDefault"></label>
                            </div>
                        </div>

                        <div v-else-if="colIdx > 8" class="tw-grid tw-grid-flow-col tw-rounded tw-overflow-hidden">
                            <button class="tw-bg-blue-600 tw-px-4 tw-py-1 tw-text-white"
                                @click="showProduct(items2[rowIdx])">
                                Ver más detalles
                            </button>
                            <button class="tw-bg-green-600 tw-py-1 tw-text-white tw-mx-2 tw-rounded"
                                @click="go(items2[rowIdx].id)">
                                Editar
                            </button>
                            <button class="tw-bg-red-600 tw-py-1 tw-text-white tw-mx-2 tw-rounded"
                                @click="deleteProduct(rowIdx)">
                                Eliminar
                            </button>
                        </div>
                    </template>
                </Table>
            </WaitOverlay>

            <!-- </ECol>h
            </ERow> -->
        </ECard>
    </main>
</template>
