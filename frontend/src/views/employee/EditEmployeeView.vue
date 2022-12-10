<script setup lang="ts">
    import { isMessage } from '@/store/types/typesafe'
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import ECol from '@components/custom/ECol.vue'
    import ERow from '@components/custom/ERow.vue'
    import InputText from '@components/custom/InputText.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import WaitOverlay from '@components/custom/WaitOverlay.vue'
    import { useClientStore } from '@store/client'
    import { useEmployeeStore } from '@store/employee'
    import { useRoleStore } from '@store/role'
    import type { Employee, Gender, Role } from '@store/types'
    import { Form as ValidationForm, useField } from 'vee-validate'
    import * as yup from 'yup'

    import { onMounted } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    import { useToast } from 'vue-toastification'

    const router = useRouter()

    /*loading*/
    const showWaitOverlay = ref<boolean>(true)

    /*show messages*/
    const toast = useToast()

    const isUploadingEmployee = ref(false)

    const employeeRepository = useEmployeeStore()

    /*Fecha actual */
    const hoy = new Date()

    /*Formulario del Sexo*/
    const clientStore = useClientStore()

    const formGender = ref<FormGender>({
        genders: [],
    })

    type FormGender = {
        genders: Gender[]
    }
    const loadGender = async () => {
        try {
            formGender.value.genders = await clientStore.fetchAllGender()
        } catch (error) {
            console.log(error)
        }
    }

    /*Formulario de Rol*/
    const roleStore = useRoleStore()

    const formRole = ref<FormRole>({
        roles: [],
    })

    type FormRole = {
        roles: Role[]
    }

    const loadRole = async () => {
        try {
            formRole.value.roles = await (await roleStore.fetchRoles()).data
        } catch (error) {
            console.log(error)
        }
    }

    type UseForm = {
        is_active: boolean
        created_by: Maybe<Employee> | null | number
    }

    /*Formulario*/

    const form = ref<UseForm>({
        is_active: true,
        created_by: null,
    })

    const message = 'El campo es requerido'

    const employeeFormValidation = ref({
        role: useField('role', yup.object().required(message)),
        name: useField(
            'username',
            yup
                .string()
                .matches(/^[a-zA-Z\s]+$/, 'Nombre inválido')
                .required(message)
        ),
        lastName: useField(
            'lastName',
            yup
                .string()
                .matches(/^[a-zA-Z\s]+$/, 'Apellido inválido')
                .required(message)
        ),
        cid: useField(
            'cid',
            yup
                .string()
                .matches(/^\d{10}$/, 'Formato incorrecto (10 dígitos)')
                .required(message)
        ),
        phone_number: useField(
            'phone_number',
            yup
                .string()
                .matches(/^\d{10}$/, 'Formato incorrecto (10 dígitos)')
                .required(message)
        ),
        gender: useField('gender', yup.object().required(message)),
        address: useField(
            'address',
            yup.string().nullable().max(256, 'Máximo 256 caracteres')
        ),
    })

    function changeStatus() {
        form.value.is_active = !form.value.is_active
    }

    const route = useRoute()
    const f = employeeFormValidation.value

    async function loadInfo() {
        showWaitOverlay.value = true
        try {
            const infoEmployee = await employeeRepository.fetchEmployee(
                Number(route.params.id)
            )
            ;(f.name.value = infoEmployee.name),
                (f.lastName.value = infoEmployee.lastname),
                (f.cid.value = infoEmployee.cid),
                (form.value.is_active = infoEmployee.is_active),
                (f.role.value = infoEmployee.role),
                (f.phone_number.value = infoEmployee.phone_number),
                (form.value.created_by = infoEmployee.created_by),
                (f.gender.value = infoEmployee.gender),
                (f.address.value =
                    infoEmployee.address == '' ? null : infoEmployee.address)
        } catch (error) {
            console.log(error)
        } finally {
            showWaitOverlay.value = false
        }
        console.log(f)
    }

    function submit() {
        if (
            f.role.errorMessage ||
            f.cid.errorMessage ||
            f.name.errorMessage ||
            f.lastName.errorMessage ||
            f.phone_number.errorMessage ||
            f.gender.errorMessage ||
            f.address.errorMessage
        ) {
            toast.error('Verifique los datos')
            return
        }
        employeeRepository
            .updateEmployee(Number(route.params.id), {
                name: f.name.value,
                lastname: f.lastName.value,
                cid: f.cid.value,
                is_active: form.value.is_active,
                role: f.role.value.id as number,
                phone_number: f.phone_number.value,
                gender: f.gender.value.id as number,
                address: f.address.value,
            })
            .then(() => {
                toast.success('Empleado actualizado correctamente')
                router.push({ path: '/usuarios/empleados' })
            })
            .catch(err => {
                if (isMessage(err)) {
                    toast.error(err.message)
                } else {
                    toast.error('Error al actualizar el empleado')
                    console.error(err)
                }
            })
            .finally(() => {
                isUploadingEmployee.value = false
            })
    }

    onMounted(() => {
        return loadGender(), loadRole(), loadInfo()
    })

    const creador = computed(() => {
        if (form.value.created_by instanceof Object) {
            return form.value.created_by?.name
        }
        return 'No asignado'
    })
</script>

<template>
    <main>
        <WaitOverlay :show="showWaitOverlay">
            <ECard>
                <ValidationForm
                    @submit="submit"
                    :validation-schema="employeeFormValidation">
                    <ERow align-v="start">
                        <ECol cols="12" lg="6" xl="3">
                            <InputText
                                label="Fecha de creación"
                                :placeholder="hoy.toLocaleDateString()"
                                readonly />
                        </ECol>
                        <ECol cols="12" lg="6" xl="3">
                            <InputText
                                label="Hora de creación"
                                :placeholder="hoy.toLocaleTimeString()"
                                readonly />
                        </ECol>
                        <ECol cols="12" lg="6" xl="3">
                            <InputText
                                label="Creado por"
                                :placeholder="creador"
                                readonly />
                        </ECol>
                        <ECol cols="12" lg="6" xl="3">
                            <ListBox
                                top-label="Rol"
                                v-model="employeeFormValidation.role.value"
                                placeholder="No ha seleccionado un rol"
                                label="name"
                                :options="formRole.roles ?? []" />
                            <small
                                class="tw-text-red-700 dark:tw-text-red-500 tw-italic tw-text-tiny">
                                {{ employeeFormValidation.role.errorMessage }}
                                &ZeroWidthSpace;
                            </small>
                        </ECol>
                    </ERow>
                    <ERow align-v="start">
                        <ECol cols="12" lg="6" xl="3">
                            <InputText
                                label="Cédula"
                                v-model="employeeFormValidation.cid.value"
                                :info-label="
                                    employeeFormValidation.cid.errorMessage
                                "
                                :status="
                                    Boolean(
                                        employeeFormValidation.cid.errorMessage
                                    )
                                "
                                info-status="danger" />
                        </ECol>
                        <ECol cols="12" lg="6" xl="3">
                            <InputText
                                label="Nombres"
                                v-model="employeeFormValidation.name.value"
                                :info-label="
                                    employeeFormValidation.name.errorMessage
                                "
                                :status="
                                    Boolean(
                                        employeeFormValidation.name.errorMessage
                                    )
                                "
                                info-status="danger" />
                        </ECol>
                        <ECol cols="12" lg="6" xl="3">
                            <InputText
                                label="Apellidos"
                                v-model="employeeFormValidation.lastName.value"
                                :info-label="
                                    employeeFormValidation.lastName.errorMessage
                                "
                                :status="
                                    Boolean(
                                        employeeFormValidation.lastName
                                            .errorMessage
                                    )
                                "
                                info-status="danger" />
                        </ECol>
                        <ECol cols="12" lg="6" xl="3">
                            <span
                                class="tw-pl-0.5 tw-font-bold tw-text-md lg:tw-text-base"
                                >Estado</span
                            >
                            <div class="form-check form-switch">
                                <input
                                    class="form-check-input"
                                    name="status"
                                    type="checkbox"
                                    role="switch"
                                    :checked="form.is_active"
                                    @change="changeStatus()" />
                            </div>
                        </ECol>
                    </ERow>
                    <ERow align-v="start">
                        <ECol cols="12" lg="6" xl="3">
                            <InputText
                                label="Teléfono"
                                v-model="
                                    employeeFormValidation.phone_number.value
                                "
                                :info-label="
                                    employeeFormValidation.phone_number
                                        .errorMessage
                                "
                                :status="
                                    Boolean(
                                        employeeFormValidation.phone_number
                                            .errorMessage
                                    )
                                "
                                info-status="danger" />
                        </ECol>
                        <ECol cols="12" lg="6" xl="3">
                            <ListBox
                                top-label="Sexo"
                                v-model="employeeFormValidation.gender.value"
                                placeholder="No ha seleccionado un sexo"
                                label="name"
                                :options="formGender.genders ?? []" />
                            <small
                                class="tw-text-red-700 dark:tw-text-red-500 tw-italic tw-text-tiny">
                                {{ employeeFormValidation.gender.errorMessage }}
                                &ZeroWidthSpace;
                            </small>
                        </ECol>
                        <ECol cols="12" lg="6" xl="6">
                            <InputText
                                label="Dirección"
                                v-model="employeeFormValidation.address.value"
                                :info-label="
                                    employeeFormValidation.address.errorMessage
                                "
                                :status="
                                    Boolean(
                                        employeeFormValidation.address
                                            .errorMessage
                                    )
                                "
                                info-status="danger" />
                        </ECol>
                    </ERow>
                    <ERow>
                        <ECol>
                            <EButton
                                left-icon="fa-floppy-disk"
                                icon-provider="awesome">
                                Guardar
                            </EButton>
                        </ECol>
                    </ERow>
                </ValidationForm>
            </ECard>
        </WaitOverlay>
    </main>
</template>
