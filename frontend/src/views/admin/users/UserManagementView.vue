<script lang="ts" setup>
    import { TabPanel } from '@headlessui/vue'
    import { useCommonStore } from '@store/common'
    import { type Employee, isMessage } from '@store/types'
    import type { Group } from '@store/types/common.model'
    import type { RawUser, SimpleUser, UserForm } from '@store/types/user.model'
    import { useUserStore } from '@store/users'
    import { BIconPerson } from 'bootstrap-icons-vue'
    import { BPagination, type BvEvent } from 'bootstrap-vue-3'
    import { Form as ValidationForm, useField } from 'vee-validate'
    import * as yup from 'yup'

    import { computed, watch } from 'vue'
    import { useToast } from 'vue-toastification'

    import {
        EButton,
        ECard,
        ETab,
        InputText,
        ListBox,
        ModalDialog,
        UserCardItem,
        WaitOverlay,
    } from '@custom-components'

    import EmployeeSearch from '../utils/EmployeeSearch.vue'
    import UserFormView from './UserFormView.vue'

    const toast = useToast()
    /**
     * Stores
     */
    const userRepository = useUserStore()
    const commonRepository = useCommonStore()
    /**
     * Form related variable definition
     */
    const pagination = ref<PaginationOptions & UserForm>({
        per_page: 10,
        page: 1,
        employee: undefined,
        email: undefined,
        group: undefined,
        is_active: true,
    })
    const targetDeleteUser = ref<Optional<SimpleUser>>(null)
    const targetUpdateUser = ref<Optional<SimpleUser>>(null)

    const targetEmployee = ref<Employee>()

    const filterOption = ref<
        {
            label: string
            value: 'username' | 'email'
        }[]
    >([
        { label: 'Usuario', value: 'username' },
        { label: 'Correo', value: 'email' },
    ])
    const filterName = ref(filterOption.value[0])
    const filterGroup = ref<Group | undefined>()
    const filterText = ref<string>('')
    /**
     * Rx Flags used to control UI
     */
    const isLoadingUsers = ref(true)
    const showDeleteDialog = ref(false)
    const showEmployeeDialog = ref(false)
    const isEditingUser = ref(false)
    const isUploadingUser = ref(false)

    /**
     *
     */
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
    const passwordErrorMsg = computed(() => {
        const f = userForm.value
        return f.password.value !== f.passwordConfirm.value
            ? 'Contraseñas no coinciden'
            : f.passwordConfirm.errorMessage
    })
    // #region User management functions
    function makeSearch() {
        pagination.value.username = undefined
        pagination.value.email = undefined
        if (filterText.value)
            pagination.value[filterName.value.value] = filterText.value
        isLoadingUsers.value = true
        userRepository.fetchUsers(pagination.value).finally(() => {
            isLoadingUsers.value = false
        })
    }

    function onPaginationClick(event: BvEvent, page: number, a: unknown) {
        pagination.value.page = page
        isLoadingUsers.value = true
        makeSearch()
    }

    function cleanFilters() {
        const filter = pagination.value
        filter.email = undefined
        filter.group = undefined
        filter.username = undefined
        filterGroup.value = undefined
        filterText.value = ''
    }
    function deleteUser() {
        if (Boolean(targetDeleteUser.value)) {
            userRepository
                .removeUser(targetDeleteUser.value?.username ?? '')
                .then(() => {
                    pagination.value.page = 1
                    makeSearch()
                    toast.success('Usuario eliminado correctamente')
                })
                .catch(() => {
                    toast.error('Error al borrar usuario')
                })
        }
        showDeleteDialog.value = false
    }
    function submitUpdate() {
        console.debug('Update') // TODO: avoid empty function
    }
    watch(filterGroup, newValue => {
        pagination.value.group = newValue?.id
    })
    makeSearch()
    commonRepository.fetchAllGroups()
    // #endregion
    //#region User creation form
    function getFormErrors() {
        const form = userForm.value
        return [
            form.email.errorMessage,
            form.group.errorMessage,
            form.username.errorMessage,
        ]
    }
    const submitNewUser = (values: unknown) => {
        const f = userForm.value
        if (
            f.email.errorMessage ||
            f.employee.errorMessage ||
            f.group.errorMessage ||
            f.employee.errorMessage ||
            f.password.errorMessage ||
            passwordErrorMsg.value
        ) {
            toast.error('Verifique los datos antes de registrar usuario')
            return
        }
        isUploadingUser.value = true
        userRepository
            .saveUser({
                email: f.email.value,
                employee: f.employee.value.id as number,
                group: f.group.value.id as number,
                username: f.username.value,
                password: f.password.value,
                password_confirm: f.passwordConfirm.value,
            })
            .then(() => {
                toast.success('Usuario registrado correctamente')
                f.email.value = ''
                f.employee.value = undefined
                f.group.value = undefined
                f.password.value = ''
                f.passwordConfirm.value = ''
                f.username.value = ''
                targetEmployee.value = undefined
            })
            .catch(err => {
                if (isMessage(err)) {
                    toast.error(err.message)
                } else {
                    toast.error('Error desconocido')
                    console.error(err)
                }
            })
            .finally(() => {
                isUploadingUser.value = false
            })
    }
    // #endregion
</script>

<template>
    <ECard>
        <ModalDialog
            :show="showDeleteDialog"
            title="AVISO!"
            button-type="ok-cancel"
            cancel-text="Cancelar"
            ok-text="Continuar"
            @ok="deleteUser"
            @cancel="
                () => {
                    showDeleteDialog = false
                }
            ">
            <span>
                ¿Está Seguro de eliminar al usuario:
                {{ targetDeleteUser?.username }} ?
            </span>
        </ModalDialog>
        <!-- #region User data update -->
        <ModalDialog
            :show="isEditingUser"
            size="3xl"
            :title="`Editando usuario '${targetUpdateUser?.username}'`"
            button-type="cancel-only"
            @ok="submitUpdate"
            @cancel="isEditingUser = false">
            <UserFormView
                edit-mode
                :user-model="targetUpdateUser as RawUser"
                @on-success="
                    () => {
                        isEditingUser = false
                        isLoadingUsers = true
                        pagination.page = 1
                        makeSearch()
                    }
                " />
        </ModalDialog>
        <!-- #endregion -->
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
        <ETab :tabs="['Mantenimiento usuarios', 'Crear usuario']">
            <!--
                Sección Mantenimiento
             -->
            <TabPanel class="container tw-min-w-full">
                <div class="row tw-px-4 gy-3">
                    <div class="search-box row mt-3 col-12 gy-2">
                        <span class="outline-label">
                            Filtros de búsqueda de usuarios
                        </span>
                        <div class="col-12 col-lg-6 col-xl-3">
                            <ListBox
                                v-model="filterGroup"
                                :options="commonRepository.groups"
                                label="name"
                                top-label="Por grupo"
                                placeholder="No seleccionado" />
                        </div>
                        <div class="col-12 col-lg-6 col-xl-3">
                            <ListBox
                                :clearable="true"
                                v-model="filterName"
                                top-label="Filtrar por:"
                                :options="filterOption" />
                        </div>
                        <div class="col-12 col-lg-12 col-xl-6">
                            <InputText
                                v-model="filterText"
                                label="Cuadro de búsqueda"
                                :placeholder="`Búsqueda por ${filterName.label}`" />
                        </div>

                        <div class="col-12 col-md-6 col-xl-auto">
                            <EButton class="tw-min-w-full" @click="makeSearch"
                                >Buscar</EButton
                            >
                        </div>
                        <div class="col-12 col-md-6 col-xl-auto">
                            <EButton class="tw-min-w-full" @click="cleanFilters"
                                >Limpiar</EButton
                            >
                        </div>
                    </div>
                    <!-- User card Item grid -->
                    <WaitOverlay :show="isLoadingUsers">
                        <div class="row justify-content-evenly gy-2 gx-2">
                            <div
                                class="col-12 col-md-6 col-lg-4 col-xxl-2"
                                v-for="user of userRepository.users?.data"
                                :key="user.id">
                                <UserCardItem
                                    :user-model="user"
                                    show-id
                                    @edit-click="
                                        () => {
                                            targetUpdateUser = user
                                            isEditingUser = true
                                        }
                                    "
                                    @clean-click="
                                        () => {
                                            targetDeleteUser = user
                                            showDeleteDialog = true
                                        }
                                    " />
                            </div>
                        </div>
                    </WaitOverlay>
                    <!-- Pagination -->
                    <div class="col col-12">
                        <BPagination
                            align="center"
                            :total-rows="userRepository.users?.total ?? 1"
                            :per-page="pagination.per_page"
                            v-model="pagination.page"
                            next-text="Siguiente"
                            prev-text="Anterior"
                            @page-click="onPaginationClick" />
                    </div>
                </div>
            </TabPanel>

            <!--#region
                User creation tab
             -->
            <TabPanel>
                <WaitOverlay :show="isUploadingUser">
                    <ValidationForm
                        @submit="submitNewUser"
                        :validation-schema="userForm">
                        <div class="row gy-3 align-items-end">
                            <div class="col col-auto">
                                <ECard>
                                    <BIconPerson width="3rem" height="3rem" />
                                </ECard>
                            </div>
                            <div class="col col-5">
                                <InputText
                                    label="Nombre de usuario"
                                    v-model.lower="userForm.username.value"
                                    :info-label="userForm.username.errorMessage"
                                    :status="
                                        Boolean(userForm.username.errorMessage)
                                    "
                                    :formatter="(str: string) => str
                                .replace(' ', '_')
                                .substring(0, 15)"
                                    info-status="danger" />
                            </div>

                            <div class="col col-5">
                                <InputText
                                    label="email"
                                    v-model.lower="userForm.email.value"
                                    :info-label="userForm.email.errorMessage"
                                    info-status="danger" />
                            </div>
                            <div class="col col-auto">
                                <ListBox
                                    :options="commonRepository.groups"
                                    v-model="userForm.group.value"
                                    label="name"
                                    top-label="Grupo de permisos"
                                    placeholder="No seleccionado" />
                                <small
                                    class="tw-text-red-700 dark:tw-text-red-500 tw-italic tw-text-tiny"
                                    >{{
                                        userForm.group.errorMessage
                                    }}
                                    &ZeroWidthSpace;</small
                                >
                            </div>
                            <div class="col col-12 col-lg-6">
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
                                    @right-icon-click="
                                        showEmployeeDialog = true
                                    "
                                    info-status="danger"
                                    :info-label="
                                        userForm.employee.errorMessage
                                    " />
                            </div>
                            <div class="col col-12 col-lg-4">
                                <InputText
                                    v-model="userForm.password.value"
                                    type="password"
                                    label="Contraseña"
                                    info-status="danger"
                                    :info-label="
                                        userForm.password.errorMessage
                                    " />
                            </div>
                            <div class="col col-12 col-lg-4">
                                <InputText
                                    v-model="userForm.passwordConfirm.value"
                                    type="password"
                                    label="Confirmar Contraseña"
                                    info-status="danger"
                                    :info-label="passwordErrorMsg" />
                            </div>
                            <div class="col col-12 col-md-3">
                                <EButton class="tw-w-full"> Guardar </EButton>
                            </div>
                        </div>
                    </ValidationForm>
                </WaitOverlay>
            </TabPanel>
            <!-- #endregion -->
        </ETab>
    </ECard>
</template>
<style lang="scss">
    .search-box {
        border-radius: 0.45rem;
        padding: 1rem 1.5rem;
        display: flex;
        border-width: 0.16rem;
        @apply tw-ring-secondary dark:tw-ring-primary;

        > span.outline-label {
            display: flex;
            position: absolute;
            max-width: fit-content;
            font-size: large;

            @apply tw-bg-slate-50 dark:tw-bg-gray-800;
            top: -0.85rem;
        }
    }
</style>
