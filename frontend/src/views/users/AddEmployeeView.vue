<script setup lang="ts">
import ECard from '@components/custom/ECard.vue'
import ERow from '@components/custom/ERow.vue'
import ECol from '@components/custom/ECol.vue'
import ListBox from '@components/custom/ListBox.vue'
import InputText from '@components/custom/InputText.vue'
import EButton from '@components/custom/EButton.vue'
import TextArea from '@components/custom/TextArea.vue'
import { useField, useForm, Form as ValidationForm } from 'vee-validate'
import { useToast } from 'vue-toastification'
import * as yup from 'yup'
import ModalDialog from '@components/custom/ModalDialog.vue'
import Title from '@components/custom/Title.vue'
import Table from '@components/holders/Table.vue'
import { computed, reactive } from 'vue'
import { Field, ErrorMessage } from 'vee-validate'
import { useRoute, useRouter } from 'vue-router'

const model = ref(null)
const toast = useToast()
const router = useRouter()
const isUploadingEmployee = ref(false)

function onSubmit(value: any) {
    router.push({ path: '/usuarios/empleados' })
}

const employeeForm   = ref({
    cid: useField(
        'cid',
        yup.string().required('Este campo es requerido')
    ),
    name: useField(
        'name',
        yup.string().required('Este campo es requerido')
    ),
    lastName: useField(
        'latName',
        yup.string().required('Este campo es requerido')
    ),
    email: useField('email', yup.string().email().required('Este campo es requerido')),
    cell: useField('cell', yup.string().matches(/^[0-9]+$/).required('Telefono inválido')),
})

/*
function validateID(value: any) {
    // if the field is empty
    if (!value) {
        return 'Este campo es requerido'
    }
    if (value.length != 10 || isNaN(value)) {
        return 'Inválido'
    }

    return true
}

function validateCell(value: any) {
    // if the field is empty
    if (!value) {
        return 'Este campo es requerido'
    }
    if (value.length != 10 || isNaN(value)) {
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

function validateName(value: any) {
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
function validateDate(value: any) {
    // if the field is empty
    if (!value) {
        return 'Este campo es requerido'
    }

    return true
}

function validateEmail(value: any) {
    if (!value) {
        return 'Este campo es requerido'
    }

    const correo = /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/
    if (!correo.test(value)) {
        return 'Inválido'
    }

    return true
}

function validateProvincia(value: any) {
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

function validateCiudad(value: any) {
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


    return true
}*/
function validateDireccion(value: any) {
    // if the field is empty
    if (!value) {
        return 'Este campo es requerido'
    }
}

const submitNewUser = (values: unknown) => {
        const f = employeeForm.value
        if (
            f.cid.errorMessage||
            f.name.errorMessage ||
            f.lastName.errorMessage ||
            f.email.errorMessage ||
            f.cell.errorMessage
        ) {
            toast.error('Verifique los datos antes de registrar usuario')
            return
        }
        /*
        isUploadingEmployee.value = true
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
                isUploadingEmployee.value = false
            })*/
    }
</script>

<template>
    <main>
        <ECard>
            <ValidationForm @submit="onSubmit">
                <ERow align-v="start">
                    <ECol cols="12" lg="6" xl="3">
                        <InputText label="Fecha de creación" placeholder="23/08/2022" readonly />
                    </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <InputText label="Hora de creación" placeholder="15:00" readonly />
                    </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <InputText label="Creado por" placeholder="23/08/2022" readonly />
                    </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <ListBox top-label="Rol" placeholder="No ha seleccionado un rol"/>
                    </ECol>
                </ERow>
                <ERow align-v="start">
                    <ECol cols="12" lg="6" xl="3">
                        <InputText label="Cédula" v-model="employeeForm.cid.value"
                            :info-label="employeeForm.cid.errorMessage" info-status="danger" />
                        <ErrorMessage name="email" style="font-size: 10px;color: red;text-align: left;" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <InputText label="Nombres" name="name"
                            v-model="employeeForm.name.value" :info-label="employeeForm.name.errorMessage"
                            info-status="danger" />
                        <ErrorMessage name="name" style="font-size: 10px;color: red;text-align: left;" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <InputText label="Apellidos" name="name"
                            v-model="employeeForm.lastName.value" :info-label="employeeForm.lastName.errorMessage"
                            info-status="danger" />
                        <ErrorMessage name="name" style="font-size: 10px;color: red;text-align: left;" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <span class="tw-pl-0.5 tw-font-bold tw-text-md lg:tw-text-base">Fecha de nacimiento</span>
                        <Field name="date" placeholder="dd/mm/yyyy"
                            class="tw-relative tw-w-full tw-cursor-default tw-rounded-lg tw-bg-neutral-500/5 dark:tw-bg-slate-900 tw-py-2 tw-pl-3 tw-pr-10 tw-text-left tw-shadow-md focus:tw-outline-none focus-visible:tw-border-indigo-500 focus-visible:tw-ring-2 focus-visible:tw-ring-white focus-visible:tw-ring-opacity-75 focus-visible:tw-ring-offset-2 focus-visible:tw-ring-offset-orange-300 sm:tw-text-md tw-text-md lg:tw-text-base tw-ring-1 tw-ring-zinc-300 dark:tw-ring-neutral-600"
                            type="date" :rules="validateDate" />
                        <ErrorMessage name="date" style="font-size: 10px;color: red;text-align: left;" />
                    </ECol>
                </ERow>
                <ERow align-v="start">
                    <ECol cols="12" lg="6" xl="3">
                        <InputText label="Correo" name="correo" type="email"
                            v-model.lower="employeeForm.email.value" :info-label="employeeForm.email.errorMessage"
                            info-status="danger" />
                        <ErrorMessage name="correo" style="font-size: 10px;color: red;text-align: left;" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <InputText label="Teléfono" name="cell"
                            v-model="employeeForm.cell.value" :info-label="employeeForm.cell.errorMessage"
                            info-status="danger" />
                        <ErrorMessage name="celula" style="font-size: 10px;color: red;text-align: left;" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <ListBox top-label="Sexo" placeholder="No ha seleccionado un sexo" label="name" />
                        <ErrorMessage name="celula" style="font-size: 10px;color: red;text-align: left;" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <span class="tw-pl-0.5 tw-font-bold tw-text-md lg:tw-text-base">Estado</span>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault" />
                            <label class="form-check-label" for="flexSwitchCheckDefault"></label>
                        </div>
                    </ECol>
                </ERow>
                <ERow align-v="start">
                    <ECol cols="12" lg="6" xl="3">
                        <ListBox top-label="Provincia" placeholder="No ha seleccionado una provincia" name="provincia"
                             />
                        <ErrorMessage name="provincia" style="font-size: 10px;color: red;text-align: left;" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <ListBox top-label="Ciudad" placeholder="No ha seleccionado una ciudad" name="ciudad"
                            />
                        <ErrorMessage name="provincia" style="font-size: 10px;color: red;text-align: left;" />
                    </ECol>
                    <ECol cols="12" lg="6" xl="3">
                        <div class="tw-flex tw-flex-col">
                            <label for="prod-det" class="form-label">
                                Dirección
                            </label>
                            <TextArea id="direc" name="direccion" :rules="validateDireccion" resize="vertical" />
                        </div>
                        <ErrorMessage name="direccion" style="font-size: 10px;color: red;text-align: left;" />
                    </ECol>
                </ERow>
                <ERow>
                    <div class="col col-12 col-md-1">
                        <EButton class="tw-w-full"> Guardar </EButton>
                    </div>
                </ERow>
            </ValidationForm>
        </ECard>
    </main>
</template>
