<script setup lang="ts">
    import EButton from '@components/custom/EButton.vue'
    import {
        ECard,
        ECol,
        ERow,
        InputText,
        ListBox,
        ModalDialog,
        TextArea,
        WaitOverlay,
    } from '@custom-components'
    import { onMounted } from 'vue'
    import Title from '@components/custom/Title.vue'
    import Table from '@components/holders/Table.vue'
    import { computed, watch } from 'vue'
    import * as VeeValidate from 'vee-validate'
    import { Field, ErrorMessage } from 'vee-validate'
    import type { TableField } from 'bootstrap-vue-3'
    import { Form as EForm } from 'vee-validate'
    import { useRoute, useRouter } from 'vue-router'
    import { useInvoiceStore } from '@store/invoice'
    import { usePaymentStore } from '@store/payment'
    import SequenceDataService from '@/store/sequence'
    import { useAuthStore } from '@store'

    import type {
        IClient,
        IItem,
        Invoice,
        IInvoiceDetails,
        IPayment,
        MessageResponse,
    } from '@store/types'
    import { isMessage, type Sequence } from '@store/types'
    import type { ServerOptions } from 'vue3-easy-data-table'
    import { useToast } from 'vue-toastification'
    import { string } from 'yup'
    const authStore = useAuthStore()
    const nameEmployee = authStore.userData?.name
    const itemStore = useInvoiceStore()
    const paymentStore = usePaymentStore()
    const productModalShow = ref<boolean>(false)
    const showWaitOverlay = ref<boolean>(true)
    const serverOpts = ref<ServerOptions>({
        page: 1,
        rowsPerPage: 5,
    })
    type SelectedItem = { item: IItem | null }
    const detailSelectedItem = ref<SelectedItem>({
        item: null,
    })
    const toast = useToast()
    const itemLoading = ref(false)
    const router = useRouter()
    const emission = new Date().toISOString().slice(0, 10)
    const return_deadline = new Date().toISOString().slice(0, 10)
    const tipopago = ref(true)
    const itemInfoShow = ref<boolean>(false)
    const formClient = ref<IClient>({
        id: 0,
        business_name: '',
        email: '',
        number_id: '',
        name: '',
    })
    const items = computed((): IItem[] => {
        if (isMessage(itemStore.paginatedItems)) return []
        console.log('hola')
        console.log(itemStore.paginatedItems?.data)
        return itemStore.paginatedItems?.data || []
    })
    const itemPageLength = computed(() => {
        const items = itemStore.paginatedItems
        if (items == null || isMessage(items)) return 0
        return items.total
    })
    const itemPaginationOptions = computed<PaginationOptions>(() => ({
        page: serverOpts.value.page,
        per_page: serverOpts.value.rowsPerPage,
    }))
    const iformShow = computed(() => ({
        codigo: itemForm.value.item?.codename?.toString(),
        nombre: itemForm.value.item?.name ?? '',
    }))
    const loadClient = async () => {
        if (formClient.value.number_id != '') {
            formClient.value = await itemStore.fetchClientNumber(
                formClient.value.number_id
            )
            console.log(formClient.value)
        } else {
            console.log('esta vacio')
            console.log(formClient.value)
            formClient.value.id = 0
            formClient.value.name = ''
        }
    }
    const loadItems = async () => {
        itemLoading.value = true
        await itemStore.fetchIItemsPaginated(itemPaginationOptions.value)
        itemLoading.value = false
    }
    const loadPayment = async () => {
        itemLoading.value = true
        itemLoading.value = false
    }
    paymentStore.fetchPayment().then(() => {
        showWaitOverlay.value = false
    })
    type QuantifiedItem = IItem & { quantity: number; total: number }
    type Form = {
        payment_method?: IPayment
        items: QuantifiedItem[]
    }
    const form = ref<Form>({
        payment_method: undefined,
        items: [],
    })

    type ItemForm = {
        item: IItem | null
        quantity: string
        total: string
        subtotal: string
        totalIVA: string
        totalInvoice: string
    }
    const itemForm = ref<ItemForm>({
        item: null,
        quantity: '0',
        total: '0',
        subtotal: '0',
        totalIVA: '0',
        totalInvoice: '0',
    })
    const itemHeader = [
        { text: 'Código', value: 'codename' },
        { text: 'Nombre de producto', value: 'name' },
        { text: 'Marca', value: 'brand' },
        { text: 'Modelo', value: 'model' },
        { text: 'Categoría', value: 'category.name' },
    ]
    const formFields: TableField[] = [
        '#',
        { label: 'Código', key: 'codename' },
        'Descripción',
        'Medida',
        { label: 'Cantidad', key: 'quantity' },
        { label: 'Precio IVA', key: 'price' },
        { label: 'IVA', key: 'iva' },
        { label: 'Total', key: 'total' },
        'Acciones',
    ]
    const formSequence = ref<Sequence>({
        id: 0,
        name: '',
        number: 0,
    })
    const formSequenceEditado = ref<Sequence>({
        id: 0,
        name: '',
        number: 0,
    })
    const codeInvoice = ref('')
    async function loadSequence(name: string) {
        formSequence.value = await SequenceDataService.fetchSequence(name)
        // formSequence.value.number += 1
        console.log(formSequence.value)
        codeInvoice.value = (
            '000000000' + String(formSequence.value.number + 1)
        ).substr(-9)
    }
    async function editSequence(name: string, formSequence: Sequence) {
        formSequenceEditado.value = await SequenceDataService.editSequence(
            name,
            formSequence
        )
        console.log(formSequenceEditado)
    }
    function saveInvoice() {
        const { value: data } = form
        if (
            formClient.value.id == 0 ||
            data.payment_method == null ||
            data.items.length == 0
        ) {
            toast.error(
                data.items.length == 0
                    ? 'No hay ítems en la tabla para guardar'
                    : 'Llene los campos para continuar'
            )
            return
        }
        const saveData: Invoice = {
            code: codeInvoice.value,
            client: formClient.value.id,
            iva: Number(itemForm.value.totalIVA),
            payment_method: data.payment_method?.id,
            return_deadline: return_deadline,
            emission: emission,
            status: 2,
            subtotal: Number(itemForm.value.subtotal),
            total: Number(itemForm.value.totalInvoice),
            anulated: false,
            invoice_details: data.items.map(it => ({
                price: Number(it.price),
                quantity: it.quantity,
                item: it.id,
            })),
        }
        showWaitOverlay.value = true
        loadSequence('INVOICE')
        console.log(saveData.code)
        itemStore
            .saveInvoice(saveData)
            .then(() => {
                toast.success('Factura registrada correctamente')
                data.items.splice(0, data.items.length)
                formSequence.value.number += 1
                editSequence('INVOICE', formSequence.value)
                console.log('hola')
                console.log(formSequence.value.number)
                router.push({ path: '/facturacion' })
            })
            .catch((it: MessageResponse) => {
                toast.error(`No se pudo guardar la factura [${it.code}]`)
            })
            .finally(() => {
                showWaitOverlay.value = false
            })
    }
    function onShowModalClick() {
        loadItems()
        console.log('valo')
        console.log(form.value.payment_method)
        productModalShow.value = true
    }
    function onRowClick(selectedItem: IItem) {
        console.log('Data: ', selectedItem)
        itemForm.value.item = selectedItem
        productModalShow.value = false
    }
    function addToTable() {
        const targetItem = itemForm.value.item
        if (!targetItem) {
            toast.error('Seleccione un producto para añadirlo a la tabla')
            return
        }
        if (form.value.items.findIndex(it => targetItem.id == it.id) >= 0) {
            toast.warning('El producto ya está añadido')
            return
        }
        const suma =
            Number(itemForm.value.quantity) *
            (Number(itemForm.value.item?.price) +
                Number(itemForm.value.item?.price) *
                    Number(itemForm.value.item?.iva))
        form.value.items.push({
            ...itemForm.value.item,
            quantity: Number(itemForm.value.quantity),
            total: Number(suma.toFixed(2)),
        } as QuantifiedItem)
        itemForm.value.subtotal = String(
            (
                Number(itemForm.value.subtotal) +
                Number(itemForm.value.quantity) *
                    Number(itemForm.value.item?.price)
            ).toFixed(2)
        )

        itemForm.value.totalIVA = String(
            (
                Number(itemForm.value.totalIVA) +
                Number(itemForm.value.quantity) *
                    Number(itemForm.value.item?.price) *
                    Number(itemForm.value.item?.iva)
            ).toFixed(2)
        )
        const subtotal =
            Number(itemForm.value.quantity) * Number(itemForm.value.item?.price)
        const totalIva =
            Number(itemForm.value.quantity) *
            (Number(itemForm.value.item?.price) *
                Number(itemForm.value.item?.iva))
        itemForm.value.totalInvoice = String(
            (
                Number(itemForm.value.totalInvoice) +
                Number(subtotal) +
                Number(totalIva)
            ).toFixed(2)
        )

        itemForm.value.item = null
        itemForm.value.quantity = '0'
        itemForm.value.total = '0'
        /*  itemForm.value.subtotal += itemForm.value.subtotal
        itemForm.value.totalIVA += itemForm.value.totalIVA
        itemForm.value.totalInvoice += itemForm.value.totalInvoice*/
        toast.success('Producto añadido a la tabla')
    }
    async function showItem(item: IItem) {
        detailSelectedItem.value.item = item
        /*detailSelectedItem.value.props = await itemStore.fetchItemProperties(
                item.id
            )*/
        itemInfoShow.value = true
    }
    function removeItem(index: number) {
        const varsubtotal =
            Number(form.value.items[index].quantity) *
            Number(form.value.items[index].price)

        itemForm.value.subtotal = String(
            (Number(itemForm.value.subtotal) - Number(varsubtotal)).toFixed(2)
        )
        const varTotalIva =
            Number(form.value.items[index].quantity) *
            (Number(form.value.items[index].price) *
                Number(form.value.items[index].iva))
        itemForm.value.totalIVA = String(
            (Number(itemForm.value.totalIVA) - Number(varTotalIva)).toFixed(2)
        )
        const subtotal =
            Number(form.value.items[index].quantity) *
            Number(form.value.items[index].price)
        const totalIva =
            Number(form.value.items[index].quantity) *
            (Number(form.value.items[index].price) *
                Number(form.value.items[index].iva))
        itemForm.value.totalInvoice = String(
            (
                Number(itemForm.value.totalInvoice) -
                Number(subtotal) -
                Number(totalIva)
            ).toFixed(2)
        )
        form.value.items.splice(index, 1)
    }
    function changeCountry(event: any) {
        if (
            event.target.options[event.target.options.selectedIndex].text ==
            'En efectivo'
        ) {
            tipopago.value = true
        } else {
            tipopago.value = false
        }
    }

    function onSubmit(value: any) {
        console.log(value)
    }

    function validateID(value: any) {
        // if the field is empty
        if (!value) {
            return 'Este campo es requerido'
        }
        if (isNaN(value)) {
            return 'Inválido'
        }

        return true
    }

    function validateCell(value: any) {
        // if the field is empty
        if (!value) {
            return 'Este campo es requerido'
        }
        if (value.length != 10 || isNaN(value)) {
            return 'Inválido'
        }

        return true
    }

    function validateId(value: any) {
        // if the field is empty
        if (!value) {
            return 'Este campo es requerido'
        }
        if (value.length != 10 || isNaN(value)) {
            return 'Inválido'
        }

        return true
    }

    function validateName(value: any) {
        // if the field is empty
        if (!value) {
            return 'Este campo es requerido'
        }
        if (!isNaN(value)) {
            return 'Inválido'
        }
        const regex = /^[a-zA-ZÀ-ÿ ]+$/

        if (!regex.test(value)) {
            return 'Inválido'
        }

        return true
    }
    function validateDate(value: any) {
        // if the field is empty
        if (!value) {
            return 'Este campo es requerido'
        }

        return true
    }

    function validateDate2(value: any) {
        // if the field is empty
        if (!value) {
            return 'Este campo es requerido'
        }

        return true
    }

    function validateEmail(value: any) {
        if (!value) {
            return 'Este campo es requerido'
        }

        const correo = /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/
        if (!correo.test(value)) {
            return 'Inválido'
        }

        return true
    }

    function validateProvincia(value: any) {
        // if the field is empty
        if (!value) {
            return 'Este campo es requerido'
        }
        if (!isNaN(value)) {
            return 'Inválido'
        }
        const regex = /^[a-zA-ZÀ-ÿ ]+$/

        if (!regex.test(value)) {
            return 'Inválido'
        }

        return true
    }

    function validateSucursal(value: any) {
        // if the field is empty
        if (!value) {
            return 'Este campo es requerido'
        }
        if (!isNaN(value)) {
            return 'Inválido'
        }
        const regex = /^[a-zA-ZÀ-ÿ ]+$/

        if (!regex.test(value)) {
            return 'Inválido'
        }

        return true
    }
    function validateDireccion(value: any) {
        // if the field is empty
        if (!value) {
            return 'Este campo es requerido'
        }

        return true
    }

    function validatePago(value: any) {
        const regex = /^[a-zA-ZÀ-ÿ ]+$/
        if (tipopago.value == false && !value) {
            return 'Este campo es necesario '
        }

        if (tipopago.value == false && isNaN(value)) {
            return 'Inválido'
        }
        if (tipopago.value == false && regex.test(value)) {
            return 'Inválido'
        }

        if (tipopago.value == true) {
            return true
        }
        return true
    }
    onMounted(() => {
        return loadSequence('INVOICE')
    })
    watch(serverOpts, loadItems)
</script>

<template>
    <main>
        <ModalDialog
            id="product-modal"
            v-model:show="productModalShow"
            size="3xl"
            title="Lista de productos">
            <!-- <div
                    class="tw-overflow-y-auto tw-max-h-72 tw-text-black dark:tw-text-white"> -->
            <EasyDataTable
                :headers="itemHeader"
                :items="items"
                buttons-pagination
                :rows-items="[5, 10, 15, 20]"
                v-model:server-options="serverOpts"
                :server-items-length="itemPageLength"
                table-class-name="custom-data-table"
                :loading="itemLoading"
                @click-row="onRowClick" />
        </ModalDialog>
        <div class="container" style="border-radius: 5px">
            <EForm @submit="onSubmit">
                <!--      <div class="row g-3">
                    <div class="col">
                        <h6
                            style="
                                font-size: 15px;
                                color: black;
                                text-align: left;
                            ">
                            Fecha de emisión *
                        </h6>
                        <Field
                            name="fecha"
                            placeholder="dd/mm/yyyy"
                            class="form-control"
                            type="Date"
                            :rules="validateDate" />
                        <div class="col">
                            <ErrorMessage
                                name="fecha"
                                style="
                                    font-size: 10px;
                                    color: red;
                                    text-align: left;
                                " />
                        </div>
                    </div>
                    <div class="col">
                        <h6
                            style="
                                font-size: 15px;
                                color: black;
                                text-align: left;
                            ">
                            Fecha de devolución*
                        </h6>
                        <Field
                            name="date"
                            placeholder="dd/mm/yyyy"
                            class="form-control"
                            type="Date"
                            :rules="validateDate2" />
                        <div class="col">
                            <ErrorMessage
                                name="date"
                                style="
                                    font-size: 10px;
                                    color: red;
                                    text-align: left;
                                " />
                        </div>
                    </div>
                    <div class="col">
                        <h6
                            style="
                                font-size: 15px;
                                color: black;
                                text-align: left;
                            ">
                            Cajero *
                        </h6>
                        <Field
                            name="provincia"
                            class="form-control"
                            type="email"
                            :rules="validateProvincia" />
                        <div class="col">
                            <ErrorMessage
                                name="provincia"
                                style="
                                    font-size: 10px;
                                    color: red;
                                    text-align: left;
                                " />
                        </div>
                    </div>-->
                <ERow align-v="start">
                    <ECol cols="12" lg="6" xl="2">
                        <InputText
                            label="Secuencia"
                            placeholder=""
                            :model-value="codeInvoice"
                            readonly />
                    </ECol>
                    <ECol cols="12" lg="6" xl="2">
                        <InputText
                            label="Emisión *"
                            :model-value="emission"
                            type="date"
                            readonly />
                    </ECol>
                    <ECol cols="12" lg="6" xl="2">
                        <InputText
                            label="Devolución *"
                            :model-value="return_deadline"
                            type="date" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="2"> </ECol>

                    <ECol cols="6" lg="6" xl="3">
                        <InputText
                            label="Facturador"
                            placeholder=""
                            v-model="nameEmployee"
                            readonly />
                    </ECol>
                </ERow>

                <ERow style="align-items: center">
                    <ECol cols="6" lg="6" xl="2">
                        <InputText
                            label="C.I/RUC"
                            placeholder="Cliente"
                            v-model.string="formClient.number_id"
                            :rules="validateID" />
                        <div class="col">
                            <ErrorMessage
                                name="email"
                                style="
                                    font-size: 10px;
                                    color: red;
                                    text-align: left;
                                " />
                        </div>
                    </ECol>
                    <ECol cols="6" lg="6" xl="1">
                        <EButton
                            variant="secondary"
                            class="tw-w-full lg:tw-w-auto"
                            @click="loadClient">
                            Buscar
                        </EButton>
                    </ECol>

                    <ECol cols="12" lg="6" xl="2">
                        <br />

                        <InputText
                            placeholder=""
                            :model-value="formClient.name"
                            readonly />
                    </ECol>
                    <ECol cols="12" lg="6" xl="1"> </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <ListBox
                            top-label="Seleccione metodo de pago"
                            v-model="form.payment_method"
                            placeholder="No ha seleccionado metodo de pago"
                            :options="paymentStore.allPayment ?? []"
                            label="name" />
                    </ECol>
                </ERow>
                <ERow style="margin-bottom: 10px">
                    <ECol cols="6" lg="auto">
                        <EButton
                            class="tw-w-full lg:tw-w-auto"
                            @click="onShowModalClick">
                            Seleccionar producto
                        </EButton>
                    </ECol>
                </ERow>
                <div class="tw">
                    <div class="tw"></div>
                </div>
                <ECard class="col-md-8" style="padding: 10px">
                    <Title size="xl"> Producto seleccionado </Title>
                    <ERow align-v="start">
                        <ECol cols="2" lg="3">
                            <InputText
                                label="Código de producto"
                                placeholder="Código del producto"
                                :model-value="iformShow.codigo"
                                readonly />
                        </ECol>
                        <ECol cols="2" lg="3">
                            <InputText
                                label="Producto seleccionado"
                                placeholder="Seleccione un producto"
                                :model-value="iformShow.nombre"
                                readonly />
                        </ECol>
                        <ECol cols="2" lg="3">
                            <InputText
                                label="Cantidad del Producto"
                                v-model.number="itemForm.quantity"
                                :formatter="(it: string) => it.replace(/\D/g, '')" />
                        </ECol>
                        <ECol cols="2" lg="3" style="padding-top: 33px">
                            <EButton
                                class="tw-w-full lg:tw-w-auto"
                                left-icon="plus"
                                :disabled="
                                    itemForm.item == null ||
                                    Number(itemForm.quantity) <= 0
                                "
                                @click="addToTable">
                                Añadir producto
                            </EButton>
                        </ECol>
                        <!-- <ECol></ECol>
                    <ECol></ECol> -->
                    </ERow>
                    <!-- Item quantity fields -->
                </ECard>
                <div class="tw-overflow-x-auto">
                    <BTable :fields="formFields" :items="form.items">
                        <template #cell(#)="{ index }">
                            {{ index + 1 }}
                        </template>
                        <template #cell(Descripción)="{ index }"
                            >{{ form.items[index]?.name }}-
                            {{ form.items[index]?.model }}-
                            {{ form.items[index]?.brand }}
                        </template>
                        <template #cell(Medida)="{}">Unidad </template>

                        <template #cell(Acciones)="{ index }">
                            <div class="t-button-group">
                                <EButton
                                    left-icon="fa-trash-can"
                                    variant="cancel"
                                    @click="removeItem(index)">
                                    <span
                                        class="tw-invisible md:tw-visible tw-font-bold">
                                        Eliminar
                                    </span>
                                </EButton>
                            </div>
                        </template>
                    </BTable>
                </div>
                <ERow>
                    <ECol
                        class="col-md-3 col-md-offset-3"
                        style="position: absolute; top: 0px; right: 10px">
                        <InputText
                            label="Subtotal:"
                            v-model.number="itemForm.subtotal"
                    /></ECol>
                    <ECol
                        class="col-md-3 col-md-offset-3"
                        style="position: absolute; top: 70px; right: 10px">
                        <InputText
                            label="Total IVA:"
                            v-model.number="itemForm.totalIVA" />
                    </ECol>
                    <ECol
                        class="col-md-3 col-md-offset-3"
                        style="position: absolute; top: 140px; right: 10px">
                        <InputText
                            label="Total:"
                            v-model.number="itemForm.totalInvoice" />
                    </ECol>

                    <ECol
                        class="tw-content-end tw-justify-end"
                        style="position: absolute; top: 220px; right: 10px">
                        <EButton
                            left-icon="fa-floppy-disk"
                            icon-provider="awesome"
                            @click="saveInvoice">
                            Facturar
                        </EButton>
                    </ECol>
                    <ECol
                        class="tw-content-end tw-justify-end"
                        style="position: absolute; top: 260px; right: 10px">
                        <br />
                    </ECol>
                </ERow>
            </EForm>
        </div>
    </main>
</template>
<style lang="scss">
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
    .custom-data-table {
        --easy-table-header-background-color: theme(colors.secondary.DEFAULT);
        --easy-table-header-font-color: theme(colors.white);
        --easy-table-border: transparentize();
        --easy-table-footer-background-color: theme(colors.secondary.DEFAULT);
        --easy-table-footer-font-color: white;

        @media (prefers-color-scheme: dark) {
            --easy-table-body-row-background-color: theme(
                colors.secondary.light
            );
            --easy-table-body-row-font-color: white;
            --easy-table-row-border: theme(colors.secondary.DEFAULT);
        }
    }
    .t-button-group {
        max-width: fit-content !important;
        @apply tw-rounded tw-overflow-hidden tw-flex tw-place-content-stretch tw-place-items-stretch;
        > t-button,
        > button {
            border-radius: 0;
            margin: 0;
            min-width: auto;
            max-width: 100%;
        }
    }
</style>
