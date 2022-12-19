<script setup lang="ts">
    import { isMessage } from '@/store/types/typesafe'
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import ERow from '@components/custom/ERow.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import WaitOverlay from '@components/custom/WaitOverlay.vue'
    import { useEmployeeStore } from '@store/employee'
    import type { Employee } from '@store/types'
    import type { TableField } from 'bootstrap-vue-3'
    import moment from 'moment'

    import { onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { useToast } from 'vue-toastification'

    const router = useRouter()
    /*show messages*/
    const toast = useToast()

    /*Name of the page*/
    const pageName = 'Empleados'

    /*Loading*/
    const showWaitOverlay = ref<boolean>(true)

    /*Stores*/
    const employeeRepository = useEmployeeStore()

    /*Pagination*/
    const perPage = ref(6)
    const currentPage = ref(1)
    const totalRows = ref(100)

    /*Modal*/
    const itemInfoShow = ref<boolean>(false)
    const empModalDelete = ref(false)

    const formFields: TableField[] = [
        { label: 'Fecha de creación', key: 'date' },
        { label: 'Hora de creación', key: 'hour' },
        { label: 'Identificación', key: 'cid' },
        { label: 'Rol', key: 'role' },
        { label: 'Nombres', key: 'name' },
        { label: 'Apellidos', key: 'lastname' },
        { label: 'Estado', key: 'is_active' },
        'Acciones',
    ]

    type SelectedItem = { item: Employee | null }
    const detailSelectedItem = ref<SelectedItem>({
        item: null,
    })

    const form = ref<Form>({
        employees: [],
    })
    type Form = {
        employees: Employee[]
    }

    async function showEmployees(e: Event | null, page: number) {
        console.log(e)
        showWaitOverlay.value = true
        try {
            const dataEmployeeTable =
                await await employeeRepository.fetchEmployees({
                    page: page,
                    per_page: perPage.value,
                })
            form.value.employees = dataEmployeeTable.data
            totalRows.value = dataEmployeeTable.total
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
            await employeeRepository.fetchActivateEmployee(employee.cid)
            toast.success('Empleado activado con éxito')
            employee.is_active = true
        } catch (error) {
            console.log(error)
        }
    }

    async function inactivateEmployee(employee: Employee) {
        try {
            await employeeRepository.fetchInactivateEmployee(employee.cid)
            toast.success('Empleado inactivado con éxito')
            employee.is_active = false
        } catch (error) {
            console.log(error)
        }
    }
    async function showItem(item: Employee) {
        detailSelectedItem.value.item = item
        itemInfoShow.value = true
    }

    function goAdd(): void {
        router.push({ path: '/usuarios/empleado/agregar' })
    }

    function goEdit(id: number): void {
        router.push({ path: `/usuarios/empleado/editar/${String(id)}` })
    }

    let id2 = 0
    let index2 = 0
    function deleteProduct(id: number, index: number): void {
        id2 = id
        index2 = index
        empModalDelete.value = true
    }

    function acceptace(): void {
        employeeRepository
            .removeEmployee(id2)
            .then(() => {
                form.value.employees.splice(index2, 1)
                toast.success('Empleado eliminado con éxito')
            })
            .catch(err => {
                if (isMessage(err)) {
                    toast.error(err.message)
                } else {
                    toast.error('Error al eliminar el empleado')
                    console.error(err)
                }
            })
            .finally(() => {
                id2 = 0
                index2 = 0
                empModalDelete.value = false
            })
    }

    onMounted(() => {
        return showEmployees(null, currentPage.value)
    })
</script>

<template>
    <main>
        <ModalDialog v-model:show="itemInfoShow" size="xl">
            <template #dialog-title>
                <b class="tw-text-2xl">Detalle del Empleado </b>
            </template>

            <div class="container">
                <div
                    class="row tw-pb-3 align-content-center justify-content-center gy-2">
                    <template
                        v-for="(d, k) in detailSelectedItem.item"
                        :key="k">
                        <div class="row" v-if="k == 'created_at'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Fecha de creación:</span
                            >
                            <span class="col-6">{{
                                moment(
                                    detailSelectedItem?.item?.created_at
                                ).format('DD/MM/YYYY')
                            }}</span>
                        </div>
                        <div class="row" v-if="k == 'created_at'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Hora de creación:</span
                            >
                            <span class="col-6">{{
                                moment(
                                    detailSelectedItem?.item?.created_at
                                ).format('HH:mm:ss')
                            }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'created_by'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Creado por:</span
                            >
                            <span class="col-6">{{
                                detailSelectedItem?.item?.created_by?.name
                            }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'name'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Nombres:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'lastname'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Apellidos:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'cid'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Cédula:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                        <div class="row" v-if="k == 'role'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Rol:</span
                            >
                            <span class="col-6">{{
                                detailSelectedItem?.item?.role?.name
                            }}</span>
                        </div>
                        <div class="row" v-else-if="k == 'phone_number'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Celular:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>

                        <div class="row" v-if="k == 'gender'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Sexo:</span
                            >
                            <span class="col-6">{{
                                detailSelectedItem?.item?.gender?.name
                            }}</span>
                        </div>
                        <div class="row" v-if="k == 'address'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Dirección:</span
                            >
                            <span class="col-6">{{ d }}</span>
                        </div>
                        <div class="row" v-if="k == 'is_active'">
                            <span class="tw-w-1/2 tw-font-bold col-6"
                                >Estado:</span
                            >
                            <span class="col-6">{{
                                detailSelectedItem?.item?.is_active
                                    ? 'Activo'
                                    : 'Inactivo'
                            }}</span>
                        </div>
                    </template>
                </div>
            </div>
        </ModalDialog>
        <ModalDialog
            id="client-modal"
            v-model:show="empModalDelete"
            title="Eliminar Cliente"
            ok-text="Eliminar"
            @ok="acceptace"
            button-type="ok-cancel">
            <h1 style="font-size: 15px; color: black; text-align: left">
                ¿Está seguro de eliminar al empleado?
            </h1>
        </ModalDialog>
        <WaitOverlay :show="showWaitOverlay">
            <!--
            <ModalDialog id="employee-modal" v-model:show="employeeModalShow" title="Detalle del empleado">
                <h1>nombre: {{ selectedEmployee?.name }}</h1>
                <span>Cantidad: ${{ selectedEmployee?.id }}</span>
            </ModalDialog>
            -->

            <ECard>
                <ERow>
                    <h1
                        class="tw-text-black first-line:dark:tw-text-neutral-300"
                        style="font-size: 35px">
                        {{ pageName }}
                    </h1>
                </ERow>
                <nav class="navbar">
                    <div class="container-fluid align_button">
                        <EButton variant="secondary" @click="goAdd"
                            >+ Agregar empleado
                        </EButton>
                    </div>
                </nav>
                <BTable :fields="formFields" :items="form.employees">
                    <template #cell(date)="{ index }">{{
                        moment(form.employees[index].created_at).format(
                            'DD/MM/YYYY'
                        )
                    }}</template>
                    <template #cell(hour)="{ index }">{{
                        moment(form.employees[index].created_at).format(
                            'HH:mm:ss'
                        )
                    }}</template>
                    <template #cell(role)="{ index }">{{
                        form.employees[index].role?.name
                    }}</template>
                    <template #cell(is_active)="{ index }">
                        <div class="form-check form-switch">
                            <input
                                class="form-check-input"
                                name="status"
                                type="checkbox"
                                role="switch"
                                :checked="form.employees[index].is_active"
                                @change="changeStatus(form.employees[index])" />
                        </div>
                    </template>

                    <template #cell(Acciones)="{ item, index }">
                        <div class="t-button-group">
                            <e-button
                                left-icon="fa-eye"
                                variant="secondary"
                                @click="showItem(item)"
                                >Ver detalles
                            </e-button>
                            <e-button
                                left-icon="fa-edit"
                                variant="success"
                                @click="goEdit(item['id'])"
                                >Editar
                            </e-button>
                            <e-button
                                left-icon="fa-trash-can"
                                variant="cancel"
                                @click="deleteProduct(item['id'], index)">
                                Eliminar
                            </e-button>
                        </div>
                    </template>
                </BTable>
                <b-pagination
                    align="center"
                    v-model="currentPage"
                    :total-rows="totalRows"
                    :per-page="perPage"
                    @page-click="showEmployees"
                    :limit="5"
                    next-text="Siguiente"
                    prev-text="Anterior"
                    hide-goto-end-buttons
                    class="paginator">
                </b-pagination>

                <!-- </ECol>
            </ERow> -->
            </ECard>
        </WaitOverlay>
    </main>
</template>

<style lang="scss">
    .align_button {
        padding: 0;
    }
</style>
