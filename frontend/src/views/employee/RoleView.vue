<script setup lang="ts">
    import { isMessage } from '@/store/types/typesafe'
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import ECol from '@components/custom/ECol.vue'
    import ERow from '@components/custom/ERow.vue'
    import InputText from '@components/custom/InputText.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import WaitOverlay from '@components/custom/WaitOverlay.vue'
    import { useAuthStore } from '@store'
    import { useRoleStore } from '@store/role'
    import type { Role } from '@store/types'
    import moment from 'moment'
    import { Form as ValidationForm, useField } from 'vee-validate'
    import * as yup from 'yup'

    import { onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { useToast } from 'vue-toastification'

    const router = useRouter()

    /*show messages*/
    const toast = useToast()

    /*Disabled*/
    const divGuardar = ref(true)
    const divEliminarEditar = ref(false)
    const divCancelarGuardar = ref(false)

    /*Readonlys*/
    const readonlyRol = ref(false)
    const readonlyCodename = ref(false)
    const readonlyClass = ref(false)

    /*Name of the page*/
    const pageName = 'Roles'

    /*Stores*/
    const roleRepository = useRoleStore()
    const authStore = useAuthStore()

    /*Loading*/
    const showWaitOverlay = ref<boolean>(true)

    /*Pagination*/
    const perPage = ref(7)
    const currentPage = ref(1)
    const totalRows = ref(100)

    /*Selected Role*/
    const selectedRole = ref<Role | null>(null)

    /*Inactivar submit del form*/
    function inactive(e: Event) {
        e.preventDefault()
    }
    /*Modal */
    const rolModalDelete = ref(false)

    type Form = {
        roles: Role[]
    }

    const form = ref<Form>({
        roles: [],
    })

    /* Variables del front */
    const date = new Date()

    type Fecha = {
        fecha?: string
        hora?: string
    }

    const formFecha = ref<Fecha>({
        fecha: date.toLocaleDateString(),
        hora: date.toLocaleTimeString(),
    })

    const message = 'El campo es requerido'

    const roleFormValidation = ref({
        name: useField(
            'username',
            yup
                .string()
                .max(64, 'No puede tener más de 64 caracteres')
                .required(message)
        ),
        codename: useField(
            'codename',
            yup
                .string()
                .max(50, 'No puede tener más de 50 caracteres')
                .matches(/^[\S]+$/, 'No puede contener espacios')
                .required(message)
        ),
        role_class: useField(
            'role_class',
            yup
                .string()
                .max(128, 'No puede tener más de 128 caracteres')
                .required(message)
        ),
    })

    async function showRoles(e: Event | null, page: number) {
        showWaitOverlay.value = true
        try {
            const dataEmployeeTable = await roleRepository.fetchRoles({
                page: page,
                per_page: perPage.value,
            })
            form.value.roles = dataEmployeeTable.data
            totalRows.value = dataEmployeeTable.total
        } catch (error) {
            console.log(error)
        } finally {
            showWaitOverlay.value = false
        }
    }

    const f = roleFormValidation.value

    function loadData(role: Role) {
        selectedRole.value = role
        ;(f.name.value = role.name),
            (f.codename.value = role.codename),
            (f.role_class.value = role.role_class),
            (formFecha.value.fecha = moment(role.created_at).format(
                'DD/MM/YYYY'
            ))
        formFecha.value.hora = moment(role.created_at).format('HH:mm:ss')

        /*Ocultar y mostrar divs*/
        divGuardar.value = false
        divEliminarEditar.value = true
        divCancelarGuardar.value = false

        disabledInputs()
    }

    function disabledInputs() {
        readonlyClass.value = true
        readonlyCodename.value = true
        readonlyRol.value = true
    }

    function clean() {
        ;(f.name.value = ''),
            (f.codename.value = ''),
            (f.role_class.value = ''),
            (formFecha.value.fecha = date.toLocaleDateString()),
            (formFecha.value.hora = date.toLocaleTimeString())

        /*Ocultar y mostrar divs*/
        divGuardar.value = true
        divEliminarEditar.value = false
        divCancelarGuardar.value = false

        enableInputs()
    }

    function goAdd() {
        if (
            f.name.errorMessage ||
            f.codename.errorMessage ||
            f.role_class.errorMessage
        ) {
            toast.error('Verifique los datos antes de registrar el rol')
            return
        }

        roleRepository
            .saveRole({
                name: f.name.value,
                codename: f.codename.value,
                role_class: f.role_class.value,
            })
            .then(() => {
                toast.success('Rol registrado correctamente')
                clean()
                showRoles(null, currentPage.value)
            })
            .catch(err => {
                toast.error('Rol ya existente')
                /*if (isMessage(err)) {
                    toast.error(err.message)
                } else {
                    toast.error('Error desconocido')
                    console.error(err)
                }*/
            })
    }

    function goDelete() {
        rolModalDelete.value = true
    }

    function acceptace() {
        roleRepository
            .removeRole(selectedRole.value?.id as number)
            .then(() => {
                toast.success('Rol eliminado con éxito')
            })
            .catch(error => {
                console.log(error)
                toast.error('Error al eliminar rol empleado')
            })
            .finally(() => {
                showRoles(null, currentPage.value)
                rolModalDelete.value = false
            })
    }

    function enableFields() {
        /*Ocultar y mostrar divs*/
        divGuardar.value = false
        divEliminarEditar.value = false
        divCancelarGuardar.value = true
        enableInputs()
    }
    function enableInputs() {
        readonlyRol.value = false
        readonlyCodename.value = false
        readonlyClass.value = false
    }

    function goEdit() {
        showWaitOverlay.value = true
        if (
            f.name.errorMessage ||
            f.codename.errorMessage ||
            f.role_class.errorMessage
        ) {
            toast.error('Verifique los datos')
            return
        }

        roleRepository
            .updateRole(selectedRole.value?.id as number, {
                id: selectedRole.value?.id,
                name: f.name.value,
                codename: f.codename.value,
                role_class: f.role_class.value,
            })
            .then(() => {
                toast.success('Rol actualizado correctamente')
                showRoles(null, currentPage.value)
            })
            .catch(err => {
                toast.error('Rol ya existente')
                /*if (isMessage(err)) {
                    toast.error(err.message)
                } else {
                    toast.error('Error desconocido')
                    console.error(err)
                }*/
            })
            .finally(() => {
                showWaitOverlay.value = false
            })
    }

    function cancel(rol: Role) {
        /*Ocultar y mostrar divs*/
        loadData(selectedRole.value as Role)
    }

    onMounted(() => {
        return showRoles(null, 1)
    })
</script>

<template>
    <ModalDialog
        id="role-modal"
        v-model:show="rolModalDelete"
        title="Eliminar Rol"
        ok-text="Eliminar"
        @ok="acceptace"
        button-type="ok-cancel">
        <h1 style="font-size: 15px; color: black; text-align: left">
            ¿Está seguro de eliminar el rol?
        </h1>
    </ModalDialog>
    <WaitOverlay :show="showWaitOverlay">
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
                    <EButton @click="clean">+ Agregar Rol </EButton>
                </div>
            </nav>
            <div
                class="row d-inline-flex allign-content-center tw-bg-slate-50 dark:tw-bg-slate-800">
                <div
                    class="col-2 mx-1 tw-flex-col tw-rounded-lg tw-bg-white dark:tw-bg-slate-800">
                    <b-pagination
                        v-model="currentPage"
                        :total-rows="totalRows"
                        :per-page="perPage"
                        @page-click="showRoles"
                        :limit="5"
                        hide-goto-end-buttons
                        class="paginator"></b-pagination>

                    <b-list-group
                        :per-page="perPage"
                        :current-page="currentPage"
                        class="button-group">
                        <b-list-group-item
                            v-for="role in form.roles"
                            :key="role.id"
                            button
                            @click="loadData(role)">
                            {{ role.name }}
                        </b-list-group-item>
                    </b-list-group>
                </div>
                <div class="col-md tw-bg-slate-50 dark:tw-bg-slate-800">
                    <ValidationForm
                        @onsubmit.prevent="inactive"
                        :validation-schema="roleFormValidation">
                        <ERow>
                            <ECol cols="12" lg="3" xl="4">
                                <InputText
                                    label="Fecha de creación"
                                    :placeholder="formFecha.fecha"
                                    readonly />
                            </ECol>
                            <ECol cols="12" lg="3" xl="4">
                                <InputText
                                    label="Hora de creación"
                                    :placeholder="formFecha.hora"
                                    readonly />
                            </ECol>
                        </ERow>
                        <ERow>
                            <ECol cols="12" lg="3" xl="4">
                                <InputText
                                    label="Nombre del rol"
                                    placeholder="Escriba el nombre del rol"
                                    v-model="roleFormValidation.name.value"
                                    :info-label="
                                        roleFormValidation.name.errorMessage
                                    "
                                    :status="
                                        Boolean(
                                            roleFormValidation.name.errorMessage
                                        )
                                    "
                                    info-status="danger"
                                    :readonly="readonlyRol" />
                            </ECol>
                            <ECol cols="12" lg="3" xl="4">
                                <InputText
                                    label="Codename"
                                    placeholder="Escriba el codename del rol"
                                    v-model="roleFormValidation.codename.value"
                                    :info-label="
                                        roleFormValidation.codename.errorMessage
                                    "
                                    :status="
                                        Boolean(
                                            roleFormValidation.codename
                                                .errorMessage
                                        )
                                    "
                                    info-status="danger"
                                    :readonly="readonlyCodename" />
                            </ECol>
                            <ECol cols="12" lg="3" xl="4">
                                <InputText
                                    label="Class"
                                    placeholder="Escriba la class del rol"
                                    v-model="
                                        roleFormValidation.role_class.value
                                    "
                                    :info-label="
                                        roleFormValidation.role_class
                                            .errorMessage
                                    "
                                    :status="
                                        Boolean(
                                            roleFormValidation.role_class
                                                .errorMessage
                                        )
                                    "
                                    info-status="danger"
                                    :readonly="readonlyClass" />
                            </ECol>
                        </ERow>
                        <!--
                            <ERow>
                            <label class="form-label"> Permisos </label>
                            </ERow>
                        -->
                        <ERow v-if="divGuardar">
                            <ECol>
                                <EButton
                                    left-icon="fa-floppy-disk"
                                    icon-provider="awesome"
                                    @click="goAdd()">
                                    Guardar
                                </EButton>
                            </ECol>
                        </ERow>
                        <ERow v-if="divEliminarEditar">
                            <ECol>
                                <EButton
                                    left-icon="fa-trash-can"
                                    variant="cancel"
                                    @click="goDelete()">
                                    Eliminar
                                </EButton>
                            </ECol>
                            <ECol>
                                <EButton
                                    left-icon="fa-edit"
                                    variant="success"
                                    @click="enableFields()">
                                    Editar
                                </EButton>
                            </ECol>
                        </ERow>
                        <ERow v-if="divCancelarGuardar">
                            <ECol>
                                <EButton
                                    left-icon="fa-cancel"
                                    variant="cancel"
                                    @click="cancel">
                                    Cancelar
                                </EButton>
                            </ECol>
                            <ECol>
                                <EButton
                                    left-icon="fa-floppy-disk"
                                    icon-provider="awesome"
                                    @click="goEdit()">
                                    Guardar
                                </EButton>
                            </ECol>
                        </ERow>
                    </ValidationForm>
                </div>
            </div>
        </ECard>
    </WaitOverlay>
</template>
