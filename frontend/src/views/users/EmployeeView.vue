<script setup lang="ts">
import ECard from '@components/custom/ECard.vue'
import ERow from '@components/custom/ERow.vue'
import EButton from '@components/custom/EButton.vue'
import ModalDialog from '@components/custom/ModalDialog.vue'
import WaitOverlay from '@components/custom/WaitOverlay.vue'
import { computed, reactive, onMounted } from 'vue'
import { useEmployeeStore } from '@store/employee'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import type { Employee } from '@store/types'
import type { TableField } from 'bootstrap-vue-3'

const router = useRouter()
/*show messages*/
const toast = useToast()

/*Name of the page*/
const pageName = 'Empleados'

/*Loading*/
const showWaitOverlay = ref<boolean>(true)

/*Modals*/
const employeeModalShow = ref(false)

/*Stores*/
const employeeRepository = useEmployeeStore()

/*Pagination*/
const employeesPerPage = ref(7)
let currentEmployeePage = ref(1)
let employeesTableTotal = ref(100)

const formFields: TableField[] = [
    { label: 'Fecha de creación', key: 'date' },
    { label: 'Hora de creación', key: 'hour' },
    { label: 'Identificación', key: 'cid' },
    { label: 'Rol', key: 'role' },
    { label: 'Nombres', key: 'name' }, ,
    { label: 'Apellidos', key: 'lastname' },
    { label: 'Estado', key: 'is_active' },
    'Acciones',
]

/*
let selectedEmployee: Optional<employeeModel> = null
function showEmployee(employee: employeeModel) {
    selectedEmployee = employee
    employeeModalShow.value = true
}
*/
const form = ref<Form>({
    employees: [],
})
type Form = {
    employees: Employee[]
}


async function showEmployees(event: any, page: number) {
    showWaitOverlay.value = true
    try {
        let dataEmployeeTable = await
            (await employeeRepository.fetchEmployees({ page: page, per_page: employeesPerPage.value }))
        form.value.employees = dataEmployeeTable.data
        employeesTableTotal.value = dataEmployeeTable.total
    } catch (error) {
        console.log(error)
    } finally {
        showWaitOverlay.value = false
    }
}

async function changeStatus(employee: Employee) {
    if (employee.is_active) {
        inactivateEmployee(employee)
    } else {
        activateEmployee(employee)
    }
}

async function activateEmployee(employee: Employee) {
    try {
        let message = await employeeRepository.fetchActivateEmployee(employee.cid)
        toast.success('Empleado activado con éxito')
        employee.is_active = true
    } catch (error) {
        console.log(error)
    }
}

async function inactivateEmployee(employee: Employee) {
    try {
        let message = await employeeRepository.fetchInactivateEmployee(employee.cid)
        toast.success('Empleado inactivado con éxito')
        employee.is_active = false
    } catch (error) {
        console.log(error)
    }
}

function goAdd(): void {
    router.push({ path: '/usuarios/empleado/agregar' })
}

function goEdit(id: number): void {
    router.push({ path: `/usuarios/empleado/editar/${String(id)}` })
}


function rol(): void {
    router.push({ path: '/admin/roles' })
}

onMounted(() => {
    return showEmployees(null, currentEmployeePage.value)
})
</script>

<template>
    <main>
        <WaitOverlay :show="showWaitOverlay">
            <!--
            <ModalDialog id="employee-modal" v-model:show="employeeModalShow" title="Detalle del empleado">
                <h1>nombre: {{ selectedEmployee?.name }}</h1>
                <span>Cantidad: ${{ selectedEmployee?.id }}</span>
            </ModalDialog>
            -->

            <ECard>
                <ERow>
                    <h1 class="tw-text-black first-line:dark:tw-text-neutral-300" style="font-size: 35px">{{ pageName }}
                    </h1>
                </ERow>
                <nav class="navbar">
                    <div class="container-fluid align">
                        <EButton type="secondary" @click="goAdd">+ Agregar empleado
                        </EButton>
                        <!--
                        <form class="d-flex" role="search">
                        <input class="form-control me-2" type="search" placeholder="Buscar empleado"
                            aria-label="Search" />
                        <button class="btn btn-outline-black" type="submit">
                            Search
                        </button>
                    </form>
                    -->

                        <EButton @click="rol">Roles</EButton>
                    </div>
                </nav>
                <BTable :fields="formFields" :items="form.employees">
                    <template #cell(date)="{ index }">{{ form.employees[index].created_at.split("T")[0] }}</template>
                    <template #cell(hour)="{ index }">{{ form.employees[index].created_at.split("T")[1].split(".")[0]
                    }}</template>
                    <template #cell(role)="{ index }">{{ form.employees[index].role?.name }}</template>
                    <template #cell(is_active)="{ index }">
                        <div class="form-check form-switch">
                            <input class="form-check-input" name="status" type="checkbox" role="switch"
                                :checked="form.employees[index].is_active"
                                @change="changeStatus(form.employees[index])" />
                        </div>
                    </template>

                    <template #cell(Acciones)="{ employee }">
                        <div class="t-button-group">
                            <e-button left-icon="fa-eye" type="secondary">Ver detalles
                            </e-button>
                            <e-button left-icon="fa-edit" type="success" @click="goEdit(employee['id'])">Editar
                            </e-button>
                        </div>
                    </template>
                </BTable>
                <b-pagination v-model="currentEmployeePage" :total-rows="employeesTableTotal"
                    :per-page="employeesPerPage" align="center" @page-click="showEmployees" :limit=5
                    hide-goto-end-buttons></b-pagination>

                <!-- </ECol>
            </ERow> -->
            </ECard>
        </WaitOverlay>
    </main>
</template>

<style lang="scss">
.align {
    padding: 0;
}

.table {
    >thead {
        @apply tw-bg-secondary tw-text-white tw-font-bold;
    }

    @media (prefers-color-scheme: dark) {
        color: white !important;
        --bs-table-striped-color: theme(colors.zinc.400);
        --bs-table-hover-color: theme('colors.primary.light');
        --bs-table-hover-bg: theme(colors.primary.light / 15%);
    }
}

.t-button-group {
    max-width: fit-content !important;
    @apply tw-rounded tw-overflow-hidden tw-flex tw-place-content-stretch tw-place-items-stretch;

    >button {
        border-radius: 0.3rem;
        margin-left: 0.5rem;
        min-width: auto;
        max-width: 100%;
    }
}
</style>
