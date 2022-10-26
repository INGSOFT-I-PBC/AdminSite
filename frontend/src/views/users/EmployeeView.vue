<script setup lang="ts">
import ECard from '@components/custom/ECard.vue'
import ERow from '@components/custom/ERow.vue'
import EButton from '@components/custom/EButton.vue'
import ModalDialog from '@components/custom/ModalDialog.vue'
import Table from '@components/holders/Table.vue'
import WaitOverlay from '@components/custom/WaitOverlay.vue'
import { computed, reactive, onMounted } from 'vue'
import { useEmployeeStore } from '@store/employee'
import { useRoute, useRouter } from 'vue-router'
import type { Employee } from '@store-types'
const router = useRouter()

const pageName = 'Empleados'
const model = ref(null)
const employeeModalShow = ref(false)
const showWaitOverlay = ref<boolean>(true)
const employeeRepository = useEmployeeStore()

const tableSettings = reactive<TableHeaderSettings>({
    headers: [
        {
            label: 'Fecha de creación',
            attribute: 'date',
        },
        {
            label: 'Hora de creación',
            attribute: 'hour',
        },
        {
            label: 'Identificación',
            attribute: 'id',
        },
        {
            label: 'Rol',
            attribute: 'rol',
        },
        {
            label: 'Nombres y Apellidos',
            attribute: 'name',
        },
        {
            label: 'Estado',
            attribute: 'estado',
        },
        {
            label: 'Acciones',
            attribute: 'actions',
        },
    ],
    rows: [
    ],
})

interface employeeModel {
    date: string
    hour: string
    create: string
    id: string
    name: string
}
let selectedEmployee: Optional<employeeModel> = null
function showEmployee(employee: employeeModel) {
    selectedEmployee= employee
    employeeModalShow.value = true
}
function removeEmployee(index: number) {
    tableSettings.rows?.splice(index, 1)
}

interface Employee {
    code: number
    created_at: string

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
/*let items: Item[]*/
const employees: Employee[] = []

async function showAllEmployees() {
    employeeRepository.fetchEmployees().then((response) => {
        console.log(response.data)
            /*items = response.data
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

            console.log(tableSettings.rows)*/
            showWaitOverlay.value = false
        })
        .catch((e: Error) => {
            console.log(e)
        })
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
    return showAllEmployees()
})
</script>

<template>
    <main>
        <WaitOverlay :show="showWaitOverlay">
            <ModalDialog id="employee-modal" v-model:show="employeeModalShow" title="Detalle del empleado">
                <h1>nombre: {{ selectedEmployee?.name }}</h1>
                <span>Cantidad: ${{ selectedEmployee?.id }}</span>
            </ModalDialog>

            <ECard>
                <ERow>
                    <h1 class="tw-text-black first-line:dark:tw-text-neutral-300" style="font-size: 35px">{{pageName}}</h1>
                </ERow>
                <nav class="navbar">
                    <div class="container-fluid" style="padding:0">
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

                <!-- <ERow>
                <ECol cols="12"> -->

                <Table :header="tableSettings">
                    <template #body-cell="{ cellData, colIdx, rowIdx }">
                        <div v-if="colIdx == 5">
                            <div class="form-check form-switch">
                                <input v-if="employees[rowIdx].state == 1" class="form-check-input" type="checkbox"
                                    role="switch" id="flexSwitchCheckDefault" checked />
                                <input v-else class="form-check-input" type="checkbox" role="switch"
                                    id="flexSwitchCheckDefault" />
                                <label class="form-check-label" for="flexSwitchCheckDefault"></label>
                            </div>
                        </div>

                        <div v-else-if="colIdx > 5" class="tw-grid tw-grid-flow-col tw-rounded tw-overflow-hidden">
                            <button class="tw-bg-blue-600 tw-py-1 tw-text-white tw-mx-2 tw-rounded"
                                @click="showEmployee(cellData as employeeModel)">
                                Ver más detalles
                            </button>
                            <button class="tw-bg-green-600 tw-py-1 tw-text-white tw-mx-2 tw-rounded" @click="goEdit(employees[rowIdx].id)">
                                Editar
                            </button>
                            <button class="tw-bg-red-600 tw-py-1 tw-text-white tw-mx-2 tw-rounded"
                                @click="removeEmployee(rowIdx)">
                                Eliminar
                            </button>
                        </div>
                    </template>
                </Table>

                <!-- </ECol>
            </ERow> -->
            </ECard>
        </WaitOverlay>
    </main>
</template>
