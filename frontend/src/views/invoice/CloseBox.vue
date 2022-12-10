<script setup lang="ts">
    import { useItemStore } from '@/store'
    import {
        type Item,
        type MessageResponse,
        type Movement,
        type PaginatedAPIResponse,
        type PaginatedResponse,
        type Purchase,
        type TomaFisica,
        type Warehouse,
        type WhWithTomaFisica,
        isMessage,
    } from '@store/types'
    import type { Employee } from '@store/types'
    import type { ItemProps } from '@store/types/items.model'
    import { useWarehouseStore } from '@store/warehouse'
    import Datepicker from '@vuepic/vue-datepicker'
    import {
        BForm,
        BFormCheckbox,
        BFormInput,
        BListGroup,
        BListGroupItem,
        BPagination,
        BTab,
        BTable,
        BTabs,
        type TableField,
    } from 'bootstrap-vue-3'
    import { Form as ValidationForm, useField } from 'vee-validate'
    import * as yup from 'yup'

    import { computed, onMounted, ref } from 'vue'
    import { useToast } from 'vue-toastification'

    import {
        EButton,
        ECard,
        InputText,
        ModalDialog,
        WaitOverlay,
    } from '@custom-components'

    import EmployeeSearch from '../admin/utils/EmployeeSearch.vue'

    const showWaitOverlay = ref(false)
    const targetEmployee = ref<Employee>()
    const showEmployeeDialog = ref(false)
    const showReportTable = ref(false)

    const historyFields: TableField[] = [
        { label: 'Forma de pago', key: 'pago' },
        { label: 'Cantidad de facturas', key: 'invoicesCant' },
        { label: 'Sistema', key: 'total' },
        { label: 'Fisico', key: 'fisico' },
        { label: 'Faltante', key: 'faltante' },
    ]

    type TableDataForm = {
        pago: string
        invoicesCant: number | string | null
        total: number | string | null
        fisico: number | string | null
        faltante: number | string | null
    }

    const tableData: TableDataForm[] = [
        {
            pago: 'Efectivo',
            invoicesCant: 0,
            total: 0,
            fisico: 0,
            faltante: 0,
        },
        {
            pago: 'Tarjeta de Crédito',
            invoicesCant: 0,
            total: 0,
            fisico: 0,
            faltante: 0,
        },
        {
            pago: 'Total',
            invoicesCant: 0,
            total: 0,
            fisico: 0,
            faltante: 0,
        },
    ]

    const message = ref('El campo es requerido')

    const historyForm = ref({
        employee: useField('employee', yup.object().required(message.value)),
        date: useField('date', yup.date().required(message.value)),
        num_caja: useField('num_caja', yup.number().required(message.value)),
        valor_apertura: useField(
            'valor_apertura',
            yup.number().required(message.value)
        ),
        un_cent: useField('un_cent', yup.number().required(message.value)),
        cinco_cent: useField(
            'cinco_cent',
            yup.number().required(message.value)
        ),
        diez_cent: useField('diez_cent', yup.number().required(message.value)),
        veinticinco_cent: useField(
            'veinte_cent',
            yup.number().required(message.value)
        ),
        cincuenta_cent: useField(
            'cincuenta_cent',
            yup.number().required(message.value)
        ),
        un_dolar_moneda: useField(
            'un_dolar_moneda',
            yup.number().required(message.value)
        ),
        un_dolar_billete: useField(
            'un_dolar_billete',
            yup.number().required(message.value)
        ),
        cinco_billete: useField(
            'cinco_dolares',
            yup.number().required(message.value)
        ),
        diez_billete: useField(
            'diez_dolares',
            yup.number().required(message.value)
        ),
        veinte_billete: useField(
            'veinte_dolares',
            yup.number().required(message.value)
        ),
        cincuenta_billete: useField(
            'cincuenta_dolares',
            yup.number().required(message.value)
        ),
    })

    const generateReport = () => {
        /*const f = employeeFormValidation.value
        if (
            f.role.errorMessage ||
            f.cid.errorMessage ||
            f.name.errorMessage ||
            f.lastName.errorMessage ||
            f.phone_number.errorMessage ||
            f.gender.errorMessage ||
            f.address.errorMessage
        ) {
            toast.error('Verifique los datos antes de registrar al empleado')
            return
        }

        isUploadingEmployee.value = true
        const employeeRepository = useEmployeeStore()

        employeeRepository
            .saveEmployee({
                name: f.name.value,
                lastname: f.lastName.value,
                cid: f.cid.value,
                is_active: form.value.is_active,
                role: f.role.value.id as number,
                phone_number: f.phone_number.value,
                created_by: authStore.userData?.employee,
                gender: f.gender.value.id as number,
                address: f.address.value,
            })
            .then(() => {
                toast.success('Usuario registrado correctamente')
                router.push('/usuarios/empleados')
            })
            .catch(err => {
                if (isMessage(err)) {
                    toast.error(err.message)
                } else {
                    toast.error('Error al registrar al empleado')
                    console.error(err)
                }
            })
            .finally(() => {
                isUploadingEmployee.value = false
            })*/
    }

    function showTable() {
        showReportTable.value = true
        console.log()
    }
    /*
    function onMounted() {

    }*/
</script>

<template>
    <WaitOverlay :show="showWaitOverlay">
        <ModalDialog
            :show="showEmployeeDialog"
            title="Búsqueda por empleado"
            size="3xl">
            <EmployeeSearch
                @item-select="
                    employee => {
                        targetEmployee = employee
                        historyForm.employee.value = employee
                        showEmployeeDialog = false
                    }
                " />
        </ModalDialog>
        <ECard>
            <ValidationForm
                @submit="generateReport"
                :validation-schema="historyForm">
                <div class="row" align-v="start">
                    <div class="col-lg-4 col-xl-3 col-sm-6 mt-auto">
                        <InputText
                            label="Empleado"
                            right-icon="search"
                            :model-value="
                                targetEmployee
                                    ? targetEmployee?.name +
                                      ' ' +
                                      targetEmployee?.lastname
                                    : 'No hay empleado seleccionado'
                            "
                            readonly
                            @right-icon-click="showEmployeeDialog = true"
                            info-status="danger"
                            :info-label="historyForm.employee.errorMessage" />
                    </div>
                    <div class="col-lg-4 col-xl-3 col-sm-6">
                        <Datepicker
                            show-now-button
                            now-button-label="Ahora"
                            auto-apply
                            close-on-scroll
                            textinput
                            dark
                            teleport-center>
                            <template #dp-input="{ value }">
                                <InputText
                                    label="Fecha"
                                    :model-value="value"
                                    :info-label="historyForm.date.errorMessage"
                                    :status="
                                        Boolean(historyForm.date.errorMessage)
                                    "
                                    info-status="danger" />
                            </template>
                        </Datepicker>
                    </div>
                    <div class="col-lg-6 col-xl-3 col-sm-12 mt-auto">
                        <InputText
                            label="Saldo Inicial"
                            v-model="historyForm.valor_apertura.value"
                            :info-label="
                                historyForm.valor_apertura.errorMessage
                            "
                            :status="
                                Boolean(historyForm.valor_apertura.errorMessage)
                            "
                            info-status="danger" />
                    </div>
                    <div class="col-lg-6 col-xl-3 col-sm-12 mt-auto">
                        <InputText
                            label="N° Caja"
                            v-model="historyForm.num_caja.value"
                            :info-label="historyForm.num_caja.errorMessage"
                            :status="Boolean(historyForm.num_caja.errorMessage)"
                            info-status="danger" />
                    </div>

                    <div class="row" align-v="start">
                        <b class="tw-text-2xl my-3">Detalle de monedas</b>
                    </div>

                    <div class="row" align-v="start">
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="1 centavo"
                                v-model="historyForm.un_cent.value"
                                :info-label="historyForm.un_cent.errorMessage"
                                :status="
                                    Boolean(historyForm.un_cent.errorMessage)
                                "
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="5 centavos"
                                v-model="historyForm.cinco_cent.value"
                                :info-label="
                                    historyForm.cinco_cent.errorMessage
                                "
                                :status="
                                    Boolean(historyForm.cinco_cent.errorMessage)
                                "
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="25 centavos"
                                v-model="historyForm.veinticinco_cent.value"
                                :info-label="
                                    historyForm.veinticinco_cent.errorMessage
                                "
                                :status="
                                    Boolean(
                                        historyForm.veinticinco_cent
                                            .errorMessage
                                    )
                                "
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="50 centavos"
                                v-model="historyForm.cincuenta_cent.value"
                                :info-label="
                                    historyForm.cincuenta_cent.errorMessage
                                "
                                :status="
                                    Boolean(
                                        historyForm.cincuenta_cent.errorMessage
                                    )
                                "
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="1 dólar"
                                v-model="historyForm.un_dolar_moneda.value"
                                :info-label="
                                    historyForm.un_dolar_moneda.errorMessage
                                "
                                :status="
                                    Boolean(
                                        historyForm.un_dolar_moneda.errorMessage
                                    )
                                "
                                info-status="danger" />
                        </div>
                    </div>

                    <div class="row" align-v="start">
                        <b class="tw-text-2xl my-3">Detalle de billetes</b>
                    </div>

                    <div class="row" align-v="start">
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="1 dólar"
                                v-model="historyForm.un_dolar_billete.value"
                                :info-label="
                                    historyForm.un_dolar_billete.errorMessage
                                "
                                :status="
                                    Boolean(
                                        historyForm.un_dolar_billete
                                            .errorMessage
                                    )
                                "
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="5 dólares"
                                v-model="historyForm.cinco_billete.value"
                                :info-label="
                                    historyForm.cinco_billete.errorMessage
                                "
                                :status="
                                    Boolean(
                                        historyForm.cinco_billete.errorMessage
                                    )
                                "
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="10 dólares"
                                v-model="historyForm.diez_billete.value"
                                :info-label="
                                    historyForm.diez_billete.errorMessage
                                "
                                :status="
                                    Boolean(
                                        historyForm.diez_billete.errorMessage
                                    )
                                "
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="20 dólares"
                                v-model="historyForm.veinte_billete.value"
                                :info-label="
                                    historyForm.veinte_billete.errorMessage
                                "
                                :status="
                                    Boolean(
                                        historyForm.veinte_billete.errorMessage
                                    )
                                "
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="50 dólares"
                                v-model="historyForm.cincuenta_billete.value"
                                :info-label="
                                    historyForm.cincuenta_billete.errorMessage
                                "
                                :status="
                                    Boolean(
                                        historyForm.cincuenta_billete
                                            .errorMessage
                                    )
                                "
                                info-status="danger" />
                        </div>
                    </div>
                </div>
                <div class="row" align-v="start">
                    <div class="col-sm-3 col-lg-4 col-xl-2 my-3">
                        <EButton
                            type="button"
                            variant="primary"
                            @click="showTable">
                            Generar Tabla
                        </EButton>
                    </div>
                </div>
            </ValidationForm>
        </ECard>

        <div v-if="showReportTable" class="my-4">
            <ECard>
                <BTable
                    id="whinv-table"
                    :fields="historyFields"
                    :items="tableData"
                    class="table">
                </BTable>

                <div class="row" align-v="start">
                    <div class="col-sm-3 col-lg-4 col-xl-2 my-3">
                        <EButton type="button" variant="primary">
                            Generar PDF
                        </EButton>
                    </div>
                </div>
            </ECard>
        </div>
    </WaitOverlay>
</template>
