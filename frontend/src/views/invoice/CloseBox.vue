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

    //import EmployeeSearch from '@components/EmployeeSearch.vue'

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

    const userForm = ref({
        username: useField(
            'username',
            yup.string().required('El campo es requerido')
        ),
        email: useField('email', yup.string().email().required()),
        group: useField('group', yup.object().required()),
        password: useField('password', yup.string().min(8).max(50).required()),
        passwordConfirm: useField(
            'password_confirm',
            yup.string().min(8).max(50).required()
        ),
        employee: useField('employee', yup.object().required()),
    })

    const historyForm = ref({
        username: useField(
            'username',
            yup.string().required('El campo es requerido')
        ),
        email: useField('email', yup.string().email().required()),
        group: useField('group', yup.object().required()),
        password: useField('password', yup.string().min(8).max(50).required()),
        passwordConfirm: useField(
            'password_confirm',
            yup.string().min(8).max(50).required()
        ),
        employee: useField('employee', yup.object().required()),
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
    }
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
                        userForm.employee.value = employee
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
                            :info-label="userForm.employee.errorMessage" />
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
                                    info-status="danger" />
                            </template>
                        </Datepicker>
                    </div>
                    <div class="col-lg-6 col-xl-3 col-sm-12 mt-auto">
                        <InputText label="Saldo Inicial" info-status="danger" />
                    </div>

                    <div class="row" align-v="start">
                        <label>Detalle de monedas </label>
                    </div>

                    <div class="row" align-v="start">
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText label="1 centavo" info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="5 centavos"
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="25 centavos"
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="50 centavos"
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText label="1 dolar" info-status="danger" />
                        </div>
                    </div>

                    <div class="row" align-v="start">
                        <label>Detalle de billetes </label>
                    </div>

                    <div class="row" align-v="start">
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText label="1 dolar" info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText label="5 dólares" info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="10 dólares"
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="20 dólares"
                                info-status="danger" />
                        </div>
                        <div class="col-sm-3 col-lg-4 col-xl-2">
                            <InputText
                                label="50 dólares"
                                info-status="danger" />
                        </div>
                    </div>

                    <div class="row" align-v="start">
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

        <div v-if="showReportTable">
            <BTable
                id="whinv-table"
                :fields="historyFields"
                :items="tableData"
                class="table">
            </BTable>
        </div>

        <div class="row" align-v="start">
            <EButton> Generar PDF </EButton>
        </div>
    </WaitOverlay>
</template>
