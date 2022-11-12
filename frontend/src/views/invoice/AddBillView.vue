<script setup lang="ts">
    import SequenceDataService from '@/store/sequence'
    import EButton from '@components/custom/EButton.vue'
    import Title from '@components/custom/Title.vue'
    import Table from '@components/holders/Table.vue'
    import { useAuthStore } from '@store'
    import { useInvoiceStore } from '@store/invoice'
    import { usePaymentStore } from '@store/payment'
    import type {
        IClient,
        IInvoiceDetails,
        IItem,
        IPayment,
        IServerOptions,
        Invoice,
        MessageResponse,
    } from '@store/types'
    import { type Sequence, isMessage } from '@store/types'
    import type { TableField } from 'bootstrap-vue-3'
    import { Console } from 'console'
    import * as VeeValidate from 'vee-validate'
    import { ErrorMessage, Field } from 'vee-validate'
    import { Form as EForm } from 'vee-validate'
    import { string } from 'yup'

    import { onMounted } from 'vue'
    import { computed, watch } from 'vue'
    import type { ServerOptions } from 'vue3-easy-data-table'
    import { useRoute, useRouter } from 'vue-router'
    import { useToast } from 'vue-toastification'

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

    const authStore = useAuthStore()
    const nameEmployee = authStore.userData?.name
    const itemStore = useInvoiceStore()
    const paymentStore = usePaymentStore()
    const productModalShow = ref<boolean>(false)
    const showWaitOverlay = ref<boolean>(true)
    const serverOpts = ref<IServerOptions>({
        page: 1,
        rowsPerPage: 5,
        buscar: '',
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
    const numero = ref(0)
    const items = computed((): IItem[] => {
        if (isMessage(itemStore.paginatedItems)) return []
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
        buscar: serverOpts.value.buscar,
    }))
    const iformShow = computed(() => ({
        codigo: itemForm.value.item?.codename?.toString(),
        nombre: itemForm.value.item?.name ?? '',
        quantity: itemForm.value.quantity ?? 1,
        priceIVA:
            Number(itemForm.value.item?.price) *
            Number(itemForm.value.item?.iva),
        iva: itemForm.value.item?.iva,
        total:
            Number(itemForm.value.item?.price) *
            Number(itemForm.value.item?.iva) *
            Number(itemForm.value.quantity),
    }))
    const loadClient = async () => {
        if (formClient.value.number_id != '') {
            formClient.value = await itemStore.fetchClientNumber(
                formClient.value.number_id
            )
        } else {
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
    type QuantifiedItem = IItem & {
        quantity: number
        subtotal: number
        totalIVA: number
        total: number
    }
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
        quantity: '1',
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
        codeInvoice.value = (
            '000000000' + String(formSequence.value.number + 1)
        ).substr(-9)
    }
    async function editSequence(name: string, formSequence: Sequence) {
        formSequenceEditado.value = await SequenceDataService.editSequence(
            name,
            formSequence
        )
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
            payment_method: data.payment_method.id,
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
        itemStore
            .saveInvoice(saveData)
            .then(() => {
                toast.success('Factura registrada correctamente')
                data.items.splice(0, data.items.length)
                formSequence.value.number += 1
                editSequence('INVOICE', formSequence.value)
                router.push({ path: '/facturacion' })
            })
            .catch((it: MessageResponse) => {
                toast.error(`No se pudo guardar la factura [${it.code}]`)
            })
            .finally(() => {
                showWaitOverlay.value = false
            })
    }

    async function onShowModalClick() {
        serverOpts.value.buscar = ''
        loadItems()
        productModalShow.value = true
    }
    function onRowClick(selectedItem: IItem) {
        itemForm.value.item = selectedItem

        productModalShow.value = false
        addToTable()
    }

    function itemcantidad(index: number) {
        /*const numInputs = document.getElementById(
            'cantidad'
        ) as HTMLInputElement*/
        const numInputs = document.querySelectorAll('input[id=cantidad]')

        numInputs.forEach(function (input) {
            input.addEventListener('change', function (e) {
                if (
                    String(form.value.items[index].quantity) == '' ||
                    form.value.items[index].quantity < 0
                ) {
                    form.value.items[index].quantity = 1
                    console.log(index)
                    //(e.target as HTMLInputElement).value = 1
                }
                itemForm.value.subtotal = '0'
                itemForm.value.totalIVA = '0'
                itemForm.value.totalInvoice = '0'
                for (const i of form.value.items) {
                    const suma =
                        Number(i.quantity) *
                        (Number(i.price) + Number(i.price) * Number(i.iva))
                    i.total = Number(suma.toFixed(2))
                    i.subtotal = Number(i.quantity) * Number(i.price)
                    i.totalIVA =
                        Number(i.quantity) * Number(i.price) * Number(i.iva)
                    itemForm.value.subtotal = (
                        Number(itemForm.value.subtotal) +
                        Number(i.subtotal.toFixed(2))
                    ).toFixed(2)

                    itemForm.value.totalIVA = (
                        Number(itemForm.value.totalIVA) +
                        Number(i.totalIVA.toFixed(2))
                    ).toFixed(2)
                }
                itemForm.value.totalInvoice = (
                    Number(itemForm.value.totalInvoice) +
                    Number(itemForm.value.subtotal) +
                    Number(itemForm.value.totalIVA)
                ).toFixed(2)
            })
        })
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
        itemForm.value.subtotal = (
            Number(itemForm.value.subtotal) +
            Number(itemForm.value.quantity) * Number(itemForm.value.item?.price)
        ).toFixed(2)

        itemForm.value.totalIVA = (
            Number(itemForm.value.totalIVA) +
            Number(itemForm.value.quantity) *
                Number(itemForm.value.item?.price) *
                Number(itemForm.value.item?.iva)
        ).toFixed(2)

        const subtotal =
            Number(itemForm.value.quantity) * Number(itemForm.value.item?.price)
        const totalIva =
            Number(itemForm.value.quantity) *
            (Number(itemForm.value.item?.price) *
                Number(itemForm.value.item?.iva))
        itemForm.value.totalInvoice = (
            Number(itemForm.value.totalInvoice) +
            Number(subtotal) +
            Number(totalIva)
        ).toFixed(2)

        itemForm.value.item = null
        //itemForm.value.quantity = '1'
        itemForm.value.total = '0'
        toast.success('Producto añadido a la tabla')
    }
    async function showItem(item: IItem) {
        detailSelectedItem.value.item = item
        itemInfoShow.value = true
    }

    function removeItem(index: number) {
        form.value.items.splice(index, 1)
        itemForm.value.subtotal = '0'
        itemForm.value.totalIVA = '0'
        itemForm.value.totalInvoice = '0'
        for (const i of form.value.items) {
            const suma =
                Number(i.quantity) *
                (Number(i.price) + Number(i.price) * Number(i.iva))
            i.total = Number(suma.toFixed(2))
            i.subtotal = Number(i.quantity) * Number(i.price)
            i.totalIVA = Number(i.quantity) * Number(i.price) * Number(i.iva)
            itemForm.value.subtotal = (
                Number(itemForm.value.subtotal) + Number(i.subtotal.toFixed(2))
            ).toFixed(2)

            itemForm.value.totalIVA = (
                Number(itemForm.value.totalIVA) + Number(i.totalIVA.toFixed(2))
            ).toFixed(2)
        }
        itemForm.value.totalInvoice = (
            Number(itemForm.value.totalInvoice) +
            Number(itemForm.value.subtotal) +
            Number(itemForm.value.totalIVA)
        ).toFixed(2)
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
        return loadSequence('INVOICE'), (serverOpts.value.buscar = '')
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
            <ERow>
                <ECol cols="12" lg="6" xl="12">
                    <InputText
                        type="text"
                        placeholder="Ingrese código o nombre del producto"
                        v-model.string="serverOpts.buscar"
                        @input="loadItems" />
                </ECol>
            </ERow>

            <EasyDataTable
                :headers="itemHeader"
                :items="items"
                buttons-pagination
                :rows-items="[5, 10, 15, 20]"
                v-model:server-options="serverOpts"
                :server-items-length="itemPageLength"
                :loading="itemLoading"
                table-class-name="custom-data-table"
                @click-row="onRowClick" />
        </ModalDialog>
        <div class="container" style="border-radius: 5px">
            <EForm>
                <ERow align-v="start">
                    <ECol cols="12" lg="6" xl="2">
                        <InputText
                            label="Código"
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
            </EForm>
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
                    <template #cell(quantity)="{ index }">
                        <ECol cols="2" lg="3">
                            <input
                                :required="true"
                                min="1"
                                pattern="^[0-9]+"
                                style="text-align: center"
                                type="number"
                                id="cantidad"
                                v-model="form.items[index].quantity"
                                @input="itemcantidad(index)" />
                        </ECol>
                    </template>
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
