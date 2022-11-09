<script setup lang="ts">
    import { useCommonStore, useEmployeeStore, useUserStore } from '@store'
    import type { Employee } from '@store/types'
    import type { Group } from '@store/types/common.model'
    import type { FullUser, RawUser } from '@store/types/user.model'
    import { BIconPerson } from 'bootstrap-icons-vue'
    import { type SubmissionHandler, useField } from 'vee-validate'
    import { ref as field_ref, object, string } from 'yup'

    import type { PropType } from 'vue'
    import { useToast } from 'vue-toastification'

    import {
        EButton,
        ECard,
        InputText,
        ListBox,
        ModalDialog,
        WaitOverlay,
    } from '@custom-components'

    import EmployeeSearch from '../utils/EmployeeSearch.vue'

    /**
     * Setting up the component
     */
    const props = defineProps({
        editMode: {
            type: Boolean,
            default: false,
        },
        userModel: {
            type: Object as PropType<RawUser>,
            default: undefined,
        },
    })

    const emits = defineEmits(['onSuccess', 'onError'])

    /**
     * Utility
     */
    const toast = useToast()
    /**
     * Stores
     */
    const userRepository = useUserStore()
    const commonRepository = useCommonStore()
    const employeeRepository = useEmployeeStore()

    /**
     * Form
     */

    const formSchema = {
        username: useField('username', string().required()),
        email: useField('email', string().email().required()),
        group: useField('group', object().required()),
        password: useField('password', string().required()),
        password_confirm: useField(
            'password_confirm',
            string().required('Needed for any')
        ),
        employee: useField('employee', object().required()),
    }

    /**
     * View-reactive variables
     */
    const isUploadingUser = ref(false)

    const targetEmployee = ref<Employee>()
    const showEmployeeDialog = ref(false)
    type UserForm = {
        username?: string
        email?: string
        group?: Group
        password?: string
        password_confirm?: string
        employee?: Employee
    }
    const initialValues = ref<UserForm>({
        username: '',
        email: undefined,
        group: undefined,
        password: undefined,
        password_confirm: undefined,
        employee: undefined,
    })
    /**
     * Functions
     */
    function submit(data: Required<UserForm>) {
        if (targetEmployee.value == undefined) {
            toast.error('No ha seleccionado algún empleado')
            return
        }
        if (props.userModel == undefined) {
            return
        }
        if (data.password || data.password_confirm) {
            if (data.password != data.password_confirm) {
                toast.error('Contraseñas no coinciden')
                return
            }
        }

        const userData: RawUser = {
            email: data.email,
            username: data.username,
            employee: (targetEmployee.value as Required<Employee>).id,
            group: (data.group as Required<Group>).id,
            id: props.userModel.id,
            is_active: true,
        }
        isUploadingUser.value = true
        userRepository
            .updateUser(userData.id, userData)
            .then(() => {
                toast.success('Se actualizó el usuario correctamente')
                emits('onSuccess')
            })
            .catch((err: unknown) => {
                console.error(err)
                toast.error(
                    'No se pudo actualizar el usuario, inténtelo más tarde'
                )
                emits('onError')
            })
            .finally(() => {
                isUploadingUser.value = false
            })
    }

    async function prepare(user: RawUser) {
        isUploadingUser.value = true
        const employee = await employeeRepository.fetchEmployee(user.employee)
        targetEmployee.value = employee
        const formattedUser: FullUser = { ...user } as unknown as FullUser
        formattedUser.employee = employee
        formattedUser.group = await commonRepository.fetchGroup(user.group)
        Object.entries(formattedUser).forEach(([field, value]) => {
            if (field in initialValues.value) {
                ;(initialValues.value as Record<string, any>)[field] = value
            }
        })
        isUploadingUser.value = false
    }
    if (props.editMode && props.userModel) {
        prepare(props.userModel)
    }
</script>

<template>
    <ModalDialog
        :show="showEmployeeDialog"
        title="Búsqueda por empleado"
        size="3xl">
        <EmployeeSearch
            @item-select="
                employee => {
                    targetEmployee = employee
                    // userForm.employee.value = employee
                    showEmployeeDialog = false
                }
            " />
    </ModalDialog>
    <!-- :validation-schema="userForm"
            :initial-values="initialValues"
        :form
            @submit="submit"
            @invalid-submit="toast.error('El formulario contiene errores')"
        :validation-schema="formSchema"-->
    <WaitOverlay :show="isUploadingUser">
        <VeeForm
            :initial-values="initialValues"
            :validation-schema="formSchema"
            @abort="toast.warning('Aborted')"
            @submit="submit as SubmissionHandler<UserForm, unknown>"
            @invalid-submit="
                (it: unknown) => {
                    toast.error('El formulario contiene errores')
                }
            ">
            <div class="row gy-3 align-items-end">
                <div class="col col-auto">
                    <ECard>
                        <BIconPerson width="3rem" height="3rem" />
                    </ECard>
                </div>
                <div class="col col-5">
                    <VeeField
                        name="username"
                        v-slot="{ field, handleChange, errorMessage }">
                        <InputText
                            label="Nombre de usuario"
                            :model-value="field.value as string"
                            :model-modifiers="{ lower: true }"
                            @update:model-value="handleChange"
                            :info-label="errorMessage"
                            :formatter="(str: string) => str
                            .replace(' ', '_')
                            .substring(0, 15)"
                            info-status="danger" />
                    </VeeField>
                </div>

                <div class="col col-5">
                    <VeeField
                        name="email"
                        v-slot="{ field, handleChange, errorMessage }">
                        <InputText
                            label="Correo Electrónico"
                            :model-value="field.value as string"
                            :model-modifiers="{ lower: true }"
                            @update:model-value="handleChange"
                            :info-label="errorMessage"
                            info-status="danger" />
                    </VeeField>
                </div>
                <div class="col col-auto">
                    <VeeField
                        name="group"
                        v-slot="{ field, handleChange, errorMessage }">
                        <ListBox
                            :options="commonRepository.groups"
                            :model-value="field.value as Record<string, any>"
                            @update:model-value="handleChange"
                            label="name"
                            top-label="Grupo de permisos"
                            placeholder="No seleccionado" />
                        <small
                            class="tw-text-red-700 dark:tw-text-red-500 tw-italic tw-text-tiny"
                            >{{ errorMessage }} &ZeroWidthSpace;</small
                        >
                    </VeeField>
                </div>
                <div class="col col-12 col-lg-6">
                    <VeeField name="employee" v-slot="{ errorMessage }">
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
                            :info-label="errorMessage" />
                    </VeeField>
                </div>
                <div class="col col-12 col-lg-4">
                    <VeeField
                        name="password"
                        v-slot="{ field, handleChange, errorMessage }">
                        <!-- v-model="userForm.password.value"
                         -->
                        <InputText
                            :model-value="field.value as string"
                            @update:model-value="handleChange"
                            type="password"
                            label="Contraseña"
                            info-status="danger"
                            :info-label="errorMessage" />
                    </VeeField>
                </div>
                <div class="col col-12 col-lg-4">
                    <VeeField
                        name="password_confirm"
                        v-slot="{ field, handleChange, errorMessage }">
                        <InputText
                            :model-value="field.value as string"
                            @update:model-value="handleChange"
                            type="password"
                            label="Confirmar Contraseña"
                            info-status="danger"
                            :info-label="errorMessage" />
                    </VeeField>
                </div>
                <div class="col col-12 col-md-3">
                    <EButton class="tw-w-full">
                        {{ editMode ? 'Actualizar datos' : 'Guardar' }}
                    </EButton>
                </div>
            </div>
        </VeeForm>
    </WaitOverlay>
</template>
