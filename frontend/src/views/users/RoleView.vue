<script setup lang="ts">
import EButton from '@components/custom/EButton.vue'
import ECard from '@components/custom/ECard.vue'
import ERow from '@components/custom/ERow.vue'
import ECol from '@components/custom/ECol.vue'
import InputText from '@components/custom/InputText.vue'
import * as VeeValidate from 'vee-validate'
import { Field, ErrorMessage } from 'vee-validate'
import { Form as EForm } from 'vee-validate'
import { useRoute, useRouter } from 'vue-router'
import { computed, reactive, onMounted } from 'vue'
import { useAuthStore } from '@store'
import { useRoleStore } from '@store/role'
import type { Role } from '@store/types'

const model = ref(null)
const router = useRouter()

/*Name of the page*/
const pageName = 'Roles'

/*Stores*/
const roleRepository = useRoleStore()
const authStore = useAuthStore()

/* Variables del front */
const date = new Date()
const createdBy = authStore.userData?.name

/*Info de roles*/
const roles = ['Cajero', 'Vendedor', 'Bodeguero']

const tiposeleccion = ref(0)
const datos = []

/*Loading*/
const showWaitOverlay = ref<boolean>(true)

/*Pagination*/
const perPage = ref(7)
let currentPage = ref(1)
let totalRows = ref(100)

function onSubmit(value: any) {
    tiposeleccion.value = 0
}

function btn_guardar(): void {
    tiposeleccion.value = 0
}

function btn_editar(): void {
    tiposeleccion.value = 1
}

function btn_agregar(): void {
    tiposeleccion.value = 1
}

function obtenerdatos(item: string): void {
    tiposeleccion.value = 2
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

const form = ref<Form>({
    roles: [],
})
type Form = {
    roles: Role[]
}


async function showRoles(event: any, page: number) {
    showWaitOverlay.value = true
    try {
        let dataEmployeeTable = await roleRepository.fetchRoles({ page: page, per_page: perPage.value })
        form.value.roles = dataEmployeeTable.data
        totalRows.value = dataEmployeeTable.total
    } catch (error) {
        console.log(error)
    } finally {
        showWaitOverlay.value = false
    }
}

onMounted(() => {
    return showRoles(null, 1)
})
</script>

<template>
    <WaitOverlay :show="showWaitOverlay">
        <ECard>
            <ERow>
                <h1 class="tw-text-black first-line:dark:tw-text-neutral-300" style="font-size: 35px">{{ pageName }}
                </h1>
            </ERow>
            <nav class="navbar">
                <div class="container-fluid" style="padding:0">
                    <EButton @click="btn_agregar()" type="secondary">+ Agregar rol
                    </EButton>
                </div>
            </nav>
            <div class="row d-inline-flex allign-content-center tw-bg-slate-50 dark:tw-bg-slate-700">
                <div class="col-2 mx-1 tw-flex-col tw-rounded-lg  tw-bg-white  dark:tw-bg-slate-800 ">
                    <b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="perPage" button
                        aria-controls="b-list-warehouses" align="center" @page-click="onPageChanged" :limit=3
                        hide-goto-end-buttons class="paginator"></b-pagination>


                    <b-list-group :per-page="perPage" :current-page="currentPage" class="button-group">
                        <b-list-group-item v-for="role, index in form.roles " button>
                            {{ role.name }}

                        </b-list-group-item>
                    </b-list-group>
                </div>
                <div v-if="tiposeleccion == 1" class="col-md tw-bg-slate-50 dark:tw-bg-slate-700">
                    <EForm @submit="onSubmit">
                        <ERow>
                            <ECol cols="12" lg="6" xl="6">
                                <InputText label="Nombre del rol" placeholder="Escriba el nombre del rol" />
                            </ECol>
                            <ECol cols="12" lg="6" xl="6">
                                <InputText label="Fecha de creación" :placeholder="date.toLocaleDateString()"
                                    readonly />
                            </ECol>

                        </ERow>
                        <ERow>
                            <ECol>
                                <InputText label="Hora de creación" :placeholder="date.toLocaleTimeString()" readonly />
                            </ECol>
                            <ECol>
                                <InputText label="Creado por" :placeholder="createdBy" readonly />
                            </ECol>
                        </ERow>
                        <ERow>
                            <label class="form-label">
                                Permisos
                            </label>
                        </ERow>
                        <EButton left-icon="fa-floppy-disk" icon-provider="awesome" @click="">
                            Guardar
                        </EButton>
                    </EForm>
                </div>
            </div>


        </ECard>
    </WaitOverlay>
</template>
