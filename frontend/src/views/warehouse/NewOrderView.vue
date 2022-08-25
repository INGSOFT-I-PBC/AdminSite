<script setup lang="ts">
    import ECard from '../../components/custom/ECard.vue'
    import ERow from '../../components/custom/ERow.vue'
    import ECol from '../../components/custom/ECol.vue'
    import ListBox from '../../components/custom/ListBox.vue'
    import InputText from '../../components/custom/InputText.vue'
    import EButton from '../../components/custom/EButton.vue'
    import ModalDialog from '../../components/custom/ModalDialog.vue'
    import Title from '../../components/custom/Title.vue'
    import Table from '../../components/holders/Table.vue'
    import { computed, reactive } from 'vue'

    const templateList = [
        { label: 'Bodega 1', value: 'Hola' },
        {
            label: 'Bodega 2',
            value: 'Test',
        },
        { label: 'Bodega 2.5', value: 'Hasa' },
        {
            label: 'Bodega 3',
            value: 'Perro',
        },
        { label: 'Bodega 4', value: 'Gato' },
    ]

    const model = ref(null)
    const productModalShow = ref(false)
    // const selectedProduct = null
    const tableSettings = reactive<TableHeaderSettings>({
        headers: [
            {
                label: 'Nombre del producto',
                attribute: 'name',
            },
            {
                label: 'Código',
                attribute: 'code',
            },
            {
                label: 'Cantidad',
                attribute: 'quantity',
            },
            {
                label: 'Detalles',
                attribute: 'detail',
            },
            {
                label: 'Opciones',
                attribute: '',
            },
        ],
        rows: [
            { name: 'Zapatos Marca X', code: '102-XFSOE', quantity: 10, detail: '' },
            {
                name: 'Camiseta deportiva',
                code: '102-XFSOE',
                quantity: 10,
                detail: '',
            },
            {
                name: 'Camiseta deportiva modelo c',
                code: '102-XFSOE',
                quantity: 10,
                detail: '',
            },
            { name: 'Zapatos Marca X', code: '102-XFSOE', quantity: 10, detail: '' },
            { name: 'Zapatos Marca X', code: '102-XFSOE', quantity: 10, detail: '' },
            { name: 'Zapatos Marca X', code: '102-XFSOE', quantity: 10, detail: '' },
            { name: 'Zapatos Marca X', code: '102-XFSOE', quantity: 10, detail: '' },
        ],
    })

    const subTotal = computed(() => 0)
    const iva = computed(() => subTotal.value * 0.12)
    interface productModel {
        name: string
        code: string
        quantity: number
        detail: string
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
</script>

<template>
    <main>
        <ModalDialog
            id="product-modal"
            v-model:show="productModalShow"
            title="Detalle del producto">
            <h1>nombre: {{ selectedProduct?.name }}</h1>
            <span>Cantidad: ${{ selectedProduct?.quantity }}</span>
        </ModalDialog>
        <ECard>
            <ERow>
                <ECol cols="12" md="6" xl="4">
                    <ListBox
                        v-model="model"
                        top-label="Enviar a"
                        :options="templateList" />
                </ECol>
                <ECol cols="12" md="5">
                    <InputText
                        label="Comentario del pedido"
                        placeholder="Razón o comentario del pedido" />
                </ECol>
            </ERow>
            <ERow>
                <ECol>
                    <EButton @click="productModalShow = true">
                        Seleccionar producto
                    </EButton>
                </ECol>
            </ERow>
            <div class="tw-flex">
                <div class="tw-w-[1.5rem]">&ZeroWidthSpace;</div>
            </div>

            <!-- <ERow>
                <ECol cols="12"> -->
            <ECard>
                <Title size="lg"> Datos del Ítem seleccionado </Title>
                <ERow>
                    <ECol>
                        <InputText label="Producto seleccionado" />
                    </ECol>
                    <ECol>
                        <InputText
                            label="Código de producto"
                            :disabled="!!selectedProduct" />
                    </ECol>
                    <ECol>
                        <EButton left-icon="plus" disabled>
                            Añadir producto
                        </EButton>
                    </ECol>
                    <!-- <ECol></ECol>
                    <ECol></ECol> -->
                </ERow>
                <!-- Item quantity fields -->
                <ERow>
                    <ECol>
                        <InputText
                            label="Detalle del producto"
                            disabled
                            placeholder="Cargue un ítem para ver su descripción" />
                    </ECol>
                    <ECol>
                        <InputText label="Cantidad del Producto" type="number" />
                    </ECol>
                </ERow>
            </ECard>
            <Table :header="tableSettings">
                <template #body-cell="{ cellData, colIdx, rowIdx }">
                    <div
                        v-if="colIdx > 3"
                        class="tw-grid tw-grid-flow-col tw-rounded tw-overflow-hidden">
                        <button
                            class="tw-bg-blue-600 tw-px-4 tw-py-1 tw-text-white"
                            @click="showProduct(cellData)">
                            Ver más detalles
                        </button>
                        <button
                            class="tw-bg-red-600 tw-py-1 tw-text-white"
                            @click="removeItem(rowIdx)">
                            Eliminar
                        </button>
                    </div>
                </template>
            </Table>
            <ERow>
                <ECol class="tw-content-end tw-justify-end">
                    <div
                        class="tw-flex tw-flex-col tw-font-bold tw-content-end tw-items-center tw-justify-between">
                        <span>Sub Total: ${{ subTotal.toFixed(3) }}</span>
                        <!-- <div> -->
                        <span>IVA 12%: ${{ iva.toFixed(3) }}</span>
                        <span>Total: ${{ (subTotal + iva).toFixed(3) }}</span>
                        <!-- </div> -->
                    </div>
                </ECol>
            </ERow>
            <!-- </ECol>
            </ERow> -->
        </ECard>
    </main>
</template>
