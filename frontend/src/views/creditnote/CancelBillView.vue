<script setup lang="ts">
    import SequenceDataService from '@/store/sequence'
    import EButton from '@components/custom/EButton.vue'
    import Title from '@components/custom/Title.vue'
    import Table from '@components/holders/Table.vue'
    import { useAuthStore } from '@store'
    import { useCreditNoteStore } from '@store/creditnote'
    import { useInvoiceStore } from '@store/invoice'
    import { usePaymentStore } from '@store/payment'
    import type {
        Client,
        CreditNote,
        EditCreditNoteInvoice,
        IClient,
        IEditInventory,
        IInventory,
        IInvoiceDetails,
        IItem,
        IPayment,
        IServerOptions,
        Invoice,
        MessageResponse,
    } from '@store/types'
    import { type Sequence, isMessage } from '@store/types'
    import type { IVariant } from '@store/types/invoice.model'
    import type { TableField } from 'bootstrap-vue-3'
    import { Console } from 'console'
    import { all } from 'ol/loadingstrategy'
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
    const nameNoteCredit = ref('Nota de Crédito')
    const itemStore = useInvoiceStore()
    const creditnoteStore = useCreditNoteStore()

    const paymentStore = usePaymentStore()
    const productModalShow = ref<boolean>(false)
    const saveModalShow = ref<boolean>(false)
    const showWaitOverlay = ref<boolean>(true)
    const route = useRoute()

    const serverOpts = ref<IServerOptions>({
        page: 1,
        rowsPerPage: 5,
        buscar: '',
    })

    type SelectedItem = { item: IInventory | null }
    const detailSelectedItem = ref<SelectedItem>({
        item: null,
    })
    const toast = useToast()
    const itemLoading = ref(false)
    const router = useRouter()
    const emission = ref('')
    const return_deadline = ref('')
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
    let iinvoice: Optional<Invoice> = null
    const items = computed((): IInventory[] => {
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
        codigo: itemForm.value.item?.variant?.sku?.toString(),
        nombre: itemForm.value.item?.variant?.variant_name ?? '',
        iquantity: itemForm.value.iquantity ?? 1,
        priceIVA: Number(itemForm.value.item?.variant?.price) * 0.12,
        // Number(itemForm.value.item?.item?.iva),
        iva: 0.12, //itemForm.value.item?.item?.iva,
        total:
            Number(itemForm.value.item?.variant?.price) *
            0.12 *
            //Number(itemForm.value.item?.item?.iva) *
            Number(itemForm.value.iquantity),
    }))

    const loadClient = async (number_id: string) => {
        if (formClient.value.number_id != '') {
            formClient.value = await itemStore.fetchClientNumber(number_id)
            console.log('hola' + number_id)
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
    type QuantifiedItem = IInventory & {
        iquantity: number
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
        item: IInventory | null
        iquantity: string
        total: string
        subtotal: string
        totalIVA: string
        totalInvoice: string
    }
    type IFormEdit = {
        invoices: Invoice[]
    }
    const formEdit = ref<Optional<IFormEdit>>({
        invoices: [],
    })

    const itemForm = ref<ItemForm>({
        item: null,
        iquantity: '1',
        total: '0',
        subtotal: '0',
        totalIVA: '0',
        totalInvoice: '0',
    })
    const itemHeader = [
        { text: 'Código', value: 'variant.sku' },
        { text: 'Nombre de producto', value: 'product.product_name' },
        { text: 'Variante', value: 'variant.variant_name' },
        { text: 'Marca', value: 'product.brand_name' },
        { text: 'Stock', value: 'stock_level' },
    ]
    const formFields: TableField[] = [
        '#',
        'Código',
        'Descripción',
        'Medida',
        { label: 'Cantidad', key: 'iquantity' },
        { label: 'Precio', key: 'price' },
        { label: 'IVA 12%', key: 'iva' },
        { label: 'Total', key: 'total' },
        //  'Acciones',
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
    /*Disabled*/

    const divEditar = ref(false)
    const divCancelar = ref(false)
    const divButtons = ref(true)

    /*Readonlys*/
    const readonlyNumberId = ref(true)
    const readonlyPayMethod = ref(true)
    const readonlyDateReturn = ref(true)
    const readonlyquantity = ref(true)

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
        const saveData: CreditNote = {
            code: codeInvoice.value,
            client: formClient.value.id,
            iva: Number(itemForm.value.totalIVA),
            payment_method: data.payment_method.id,
            return_deadline: return_deadline.value,
            active: true,
            subtotal: Number(itemForm.value.subtotal),
            total: Number(itemForm.value.totalInvoice),
        }
        showWaitOverlay.value = true
        //Number(route.params.id)
        creditnoteStore
            .saveCreditNote(saveData)
            .then(response => {
                console.log('fffff')
                console.log(response)
                console.log(response.id)
                for (const i of form.value.items) {
                    const editquantity: IEditInventory = {
                        stock_level: i.stock_level + i.iquantity,
                    }
                    //console.log(i.item?.id)
                    //console.log(editquantity.quantity)
                    itemStore.editquantityInventory(
                        Number(i.variant?.id),
                        editquantity
                    )
                }
                const editcreditinvoice: EditCreditNoteInvoice = {
                    credit_note: response.id,
                    //01856-80e5b0739a-7b0db
                }
                creditnoteStore.editCreditNoteInvoice(
                    Number(route.params.id),
                    editcreditinvoice
                )
                toast.success('La Factura ha sido registrada correctamenta')
                data.items.splice(0, data.items.length)
                formSequence.value.number += 1

                router.push({ path: '/facturacion' })
            })
            .catch((it: MessageResponse) => {
                toast.error(`No se pudo anular la factura [${it.code}]`)
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
    function onRowClick(selectedItem: IInventory) {
        itemForm.value.item = selectedItem

        productModalShow.value = false
        addToTable()
    }

    function itemcantidad(index: number) {
        const numInputs = document.querySelectorAll('input[id=cantidad]')

        numInputs.forEach(function (input) {
            input.addEventListener('change', function (e) {
                if (String(form.value.items[index].iquantity) == '') {
                    form.value.items[index].iquantity = 1
                    console.log(index)
                } else if (
                    form.value.items[index].iquantity >
                    form.value.items[index].stock_level
                ) {
                    toast.error(
                        `El stock del producto ${form.value.items[index].variant?.sku} es de ${form.value.items[index].stock_level}`
                    )
                    form.value.items[index].iquantity =
                        form.value.items[index].stock_level
                }
                itemForm.value.subtotal = '0'
                itemForm.value.totalIVA = '0'
                itemForm.value.totalInvoice = '0'
                for (const i of form.value.items) {
                    const suma =
                        Number(i.iquantity) *
                        (Number(i.variant?.price) +
                            Number(i.variant?.price) * 0.12) // Number(i.item?.iva))
                    i.total = Number(suma.toFixed(2))
                    i.subtotal = Number(i.iquantity) * Number(i.variant?.price)
                    i.totalIVA =
                        Number(i.iquantity) * Number(i.variant?.price) * 0.12
                    //Number(i.item?.iva)
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
        console.log(targetItem)
        if (!targetItem) {
            toast.error('Seleccione un producto para añadirlo a la tabla')
            return
        }
        if (form.value.items.findIndex(it => targetItem.id == it.id) >= 0) {
            toast.warning('El producto ya está añadido')
            return
        }
        const suma =
            Number(itemForm.value.iquantity) *
            (Number(itemForm.value.item?.variant?.price) +
                Number(itemForm.value.item?.variant?.price) * 0.12)
        //  Number(itemForm.value.item?.item?.iva))
        form.value.items.push({
            ...itemForm.value.item,
            iquantity: Number(itemForm.value.iquantity),
            total: Number(suma.toFixed(2)),
        } as QuantifiedItem)
        itemForm.value.subtotal = (
            Number(itemForm.value.subtotal) +
            Number(itemForm.value.iquantity) *
                Number(itemForm.value.item?.variant?.price)
        ).toFixed(2)

        itemForm.value.totalIVA = (
            Number(itemForm.value.totalIVA) +
            Number(itemForm.value.iquantity) *
                Number(itemForm.value.item?.variant?.price) *
                0.12
        )
            //Number(itemForm.value.item?.item?.iva)
            .toFixed(2)

        const subtotal =
            Number(itemForm.value.iquantity) *
            Number(itemForm.value.item?.variant?.price)
        const totalIva =
            Number(itemForm.value.iquantity) *
            (Number(itemForm.value.item?.variant?.price) * 0.12)
        // Number(itemForm.value.item?.item?.iva))
        itemForm.value.totalInvoice = (
            Number(itemForm.value.totalInvoice) +
            Number(subtotal) +
            Number(totalIva)
        ).toFixed(2)

        itemForm.value.item = null
        //itemForm.value.iquantity = '1'
        itemForm.value.total = '0'
        toast.success('Producto añadido a la tabla')
    }
    async function showItem(item: IInventory) {
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
                Number(i.iquantity) *
                (Number(i.variant?.price) + Number(i.variant?.price) * 0.12) // Number(i.item?.iva))
            i.total = Number(suma.toFixed(2))
            i.subtotal = Number(i.iquantity) * Number(i.variant?.price)
            i.totalIVA = Number(i.iquantity) * Number(i.variant?.price) * 0.12
            //Number(i.item?.iva)
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
        saveModalShow.value = true
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
    function enableFields() {
        /*Ocultar y mostrar divs*/
        divEditar.value = false
        divCancelar.value = true
        divButtons.value = false
        enableInputs()
    }
    function enableInputs() {
        readonlyNumberId.value = false
        readonlyPayMethod.value = false
        readonlyquantity.value = false
    }
    function disabledInputs() {
        readonlyNumberId.value = true
        readonlyPayMethod.value = true
        readonlyquantity.value = true
        divButtons.value = true
    }

    async function loadInvoice() {
        iinvoice = null
        form.value.items = []
        itemForm.value.item = null
        itemForm.value.iquantity = '1'
        itemForm.value.total = '0'
        itemForm.value.subtotal = '0'
        itemForm.value.totalIVA = '0'
        itemForm.value.totalInvoice = '0'

        iinvoice = await itemStore.fetchInvoiceById(Number(route.params.id))

        console.log(Number(route.params.id))
        console.log('iinvoice')
        console.log(iinvoice)
        console.log(iinvoice.invoice_details)
        formClient.value = await itemStore.fetchClientNumber(
            (iinvoice.client as IClient)?.number_id
        )
        codeInvoice.value = String(iinvoice.code)
        emission.value = iinvoice.emission
        return_deadline.value = iinvoice.return_deadline
        form.value.payment_method = iinvoice.payment_method as IPayment
        //console.log(iinvoice.invoice_details)
        iinvoice.invoice_details?.forEach(async function (value) {
            console.log('hola')
            console.log(value)

            itemForm.value.item = await itemStore.fetchIInventoryById(
                (value.variant as IVariant)?.id
            )

            itemForm.value.iquantity = String(value.quantity)
            const suma =
                Number(itemForm.value.iquantity) *
                (Number(itemForm.value.item?.variant?.price) +
                    Number(itemForm.value.item?.variant?.price) * 0.12)
            // Number(itemForm.value.item?.item?.iva))
            form.value.items.push({
                ...itemForm.value.item,
                iquantity: Number(itemForm.value.iquantity),
                total: Number(suma.toFixed(2)),
            } as QuantifiedItem)
            itemForm.value.subtotal = (
                Number(itemForm.value.subtotal) +
                Number(itemForm.value.iquantity) *
                    Number(itemForm.value.item?.variant?.price)
            ).toFixed(2)

            itemForm.value.totalIVA = (
                Number(itemForm.value.totalIVA) +
                Number(itemForm.value.iquantity) *
                    Number(itemForm.value.item?.variant?.price) *
                    0.12
            )
                // Number(itemForm.value.item?.item?.iva)
                .toFixed(2)

            const subtotal =
                Number(itemForm.value.iquantity) *
                Number(itemForm.value.item?.variant?.price)
            const totalIva =
                Number(itemForm.value.iquantity) *
                (Number(itemForm.value.item?.variant?.price) * 0.12)
            // Number(itemForm.value.item?.item?.iva))
            itemForm.value.totalInvoice = (
                Number(itemForm.value.totalInvoice) +
                Number(subtotal) +
                Number(totalIva)
            ).toFixed(2)

            itemForm.value.item = null
            itemForm.value.iquantity = '1'
            itemForm.value.total = '0'
        })
        divEditar.value = true
        divCancelar.value = false
        disabledInputs()

        /*itemForm.value.item = (iinvoice?.invoice_details[1] as IInvoiceDetails)
            .item as IItem*/

        //console.log(itemForm.value.item)
    }
    function cancel() {
        /*Ocultar y mostrar divs*/
        loadInvoice()
    }

    loadInvoice()
    onMounted(() => {
        return (serverOpts.value.buscar = '')
    })

    watch(serverOpts, loadItems)
</script>

<template>
    <main>
        <ModalDialog
            id="product-modal"
            v-model:show="saveModalShow"
            title="Editar Factura"
            ok-text="Facturar"
            @ok="saveInvoice"
            button-type="ok-cancel">
            <h1 style="font-size: 15px; color: black; text-align: left">
                ¿Está seguro de anular la factura?
            </h1>
        </ModalDialog>
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
                <!-- <ERow v-if="divEditar">
                    <ECol cols="6" lg="6" xl="2">
                        <EButton
                            left-icon="fa-edit"
                            variant="success"
                            @click="enableFields()">
                            Editar
                        </EButton>
                    </ECol>
                </ERow>
                <ERow v-if="divCancelar">
                    <ECol>
                        <EButton
                            left-icon="fa-cancel"
                            variant="cancel"
                            @click="cancel">
                            Cancelar
                        </EButton>
                    </ECol>
                </ERow>-->
                <ERow align-v="start" class="tw-items-center">
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
                            v-model="emission"
                            type="date"
                            readonly />
                    </ECol>
                    <ECol cols="12" lg="6" xl="2">
                        <InputText
                            label="Devolución *"
                            v-model="return_deadline"
                            type="date"
                            :readonly="readonlyDateReturn" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="1"> </ECol>

                    <ECol cols="6" lg="6" xl="2">
                        <InputText
                            label="Facturador"
                            placeholder=""
                            v-model="nameEmployee"
                            readonly />
                    </ECol>

                    <ECol cols="6" lg="6" xl="2">
                        <InputText
                            label="Tipo de Documento"
                            placeholder=""
                            v-model="nameNoteCredit"
                            readonly />
                    </ECol>
                </ERow>

                <ERow style="align-items: center">
                    <ECol cols="6" lg="6" xl="2">
                        <InputText
                            label="C.I/RUC"
                            placeholder="Cliente"
                            v-model.string="formClient.number_id"
                            :rules="validateID"
                            :readonly="readonlyNumberId" />
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
                    <!-- <ECol cols="6" lg="6" xl="1">
                        <EButton
                            variant="secondary"
                            class="tw-w-full lg:tw-w-auto"
                            :disabled="divButtons"
                            @click="loadClient(formClient.number_id)">
                            Buscar
                        </EButton>
                    </ECol>-->

                    <ECol cols="12" lg="6" xl="2">
                        <!-- <br />-->

                        <InputText
                            label="Nombre del Cliente"
                            placeholder=""
                            :model-value="formClient.name"
                            readonly />
                    </ECol>
                    <ECol cols="12" lg="6" xl="1"> </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <InputText
                            label="Método de pago"
                            :model-value="form.payment_method?.name"
                            readonly />
                    </ECol>
                </ERow>
                <!--<ERow style="margin-bottom: 10px">
                    <ECol cols="6" lg="auto">
                        <EButton
                            class="tw-w-full lg:tw-w-auto"
                            :disabled="divButtons"
                            @click="onShowModalClick">
                            Seleccionar producto
                        </EButton>
                    </ECol>
                </ERow>-->
                <div class="tw">
                    <div class="tw"></div>
                </div>
            </EForm>
            <div class="tw-overflow-x-auto">
                <BTable :fields="formFields" :items="form.items">
                    <template #cell(#)="{ index }">
                        {{ index + 1 }}
                    </template>
                    <template #cell(Código)="{ index }">
                        {{ form.items[index]?.variant?.sku }}
                    </template>
                    <template #cell(Descripción)="{ index }"
                        >{{ form.items[index]?.variant?.variant_name }}-
                        {{ form.items[index]?.product?.brand_name }}
                    </template>
                    <template #cell(Medida)="{}">Unidad </template>
                    <template #cell(iquantity)="{ index }">
                        <ECol cols="2" lg="3">
                            <input
                                :required="true"
                                min="1"
                                pattern="^[0-9]+"
                                style="text-align: center"
                                type="number"
                                id="cantidad"
                                :readonly="readonlyquantity"
                                v-model="form.items[index].iquantity"
                                onkeypress="return (  event.charCode <32 &&  event.charCode !=127)"
                                @input="itemcantidad(index)" />
                        </ECol>
                    </template>
                    <template #cell(price)="{ index }"
                        >{{ form.items[index]?.variant?.price }}
                    </template>
                    <template #cell(iva)>
                        0.12<!-- {{ form.items[index]?.item?.iva }}-->
                    </template>
                    <!--<template #cell(Acciones)="{ index }">
                        <div class="t-button-group">
                            <EButton
                                left-icon="fa-trash-can"
                                variant="cancel"
                                :disabled="divButtons"
                                @click="removeItem(index)">
                                <span
                                    class="tw-invisible md:tw-visible tw-font-bold">
                                    Eliminar
                                </span>
                            </EButton>
                        </div>
                    </template>-->
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
                        variant="cancel"
                        icon-provider="awesome"
                        @click="onSubmit">
                        Anular
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
