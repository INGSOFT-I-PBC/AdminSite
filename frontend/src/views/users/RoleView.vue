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


const model = ref(null)
const router = useRouter()

/* Variables del front */
const date = new Date()
const authStore = useAuthStore()
const createdBy = authStore.userData?.name

/*Info de roles*/
const array = ['Cajero', 'Vendedor', 'Bodeguero']

const tiposeleccion = ref(0)
const datos = []

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

onMounted(() => {
    return showRoles()
})
</script>

<template>
    <ECard>
        <nav class="navbar">
            <div class="container-fluid" style="padding:0">
                <EButton @click="btn_agregar()" type="secondary">+ Agregar rol
                </EButton>
            </div>
        </nav>
        <div class="tw-flex tw-flex-rows tw-justify-items-stretch tw-min-h-screen tw-w-full tw-justify-between dark:tw-bg-neutral-900 tw-overflow-x-hidden"
            id="_root">
            <aside class="tw-h-full tw-min-w-fit tw-bg-gray-200 tw-rounded-r-xl tw-overflow-hidden tw-rounded ">
                <div id="__left-drawer "
                    class="tw-h-full tw-flex tw-flex-col tw-justify-self-stretch tw-justify-items-stretch lg:tw-min-w-fit tw-resize-x">
                    <div id="__left-menu-container"
                        class="tw-w-full tw-flex-1 tw-p-3 tw-overflow-y-auto tw-bg-gray-200">
                        <DrawerMenu>
                            <form class="d-flex" role="search">
                                <input class="form-control me-2" type="search" placeholder="Buscar rol"
                                    aria-label="Search" />
                                <button class="btn btn-outline-black" type="submit">
                                    Search
                                </button>
                            </form>
                            <TransitionGroup style="display: flex; align-items: center"
                                enter-active-class="tw-transition-all tw-duration-400"
                                enter-from-class="tw-opacity-0 -tw-translate-x-50 tw-scale-60"
                                enter-to-class="tw-opacity-100 tw-scale-100"
                                leave-active-class="tw-transition-all tw-duration-900" leave-from-class="tw-scale-105"
                                leave-to-class="tw-scale-10 tw-opacity-20 -tw-translate-x-full">
                                <div v-for="item in array" :key="item">
                                    <EButton @click="obtenerdatos(item)" style="display: flex; margin-top: 10px"
                                        class="hover:tw-text-primary hover:tw-font-bold">{{ item }}</EButton>
                                </div>
                            </TransitionGroup>
                        </DrawerMenu>
                    </div>
                </div>
            </aside>
            <!-- Resize bar -->
            <div class="resize-handle--x tw-cursor-ew-resize tw-justify-center hover:tw-bg-primary-light tw-w-1 hover:tw-animate-pulse hover:tw-transition tw-ease-in-out tw-duration-700 tw-bg-transparent"
                data-target="aside" />
            <!-- Right view -->
            <main class="tw-px-4 tw-py-2 tw-justify-items-stretch tw-w-full tw-flex-1 tw-flex tw-flex-col"
                id="right-panel">
                <!-- End of header -->
                <div id="_page-breadcrumb_row"
                    class="tw-flex tw-my-2 tw-transform-gpu tw-transition-all tw-duration-200 tw-ease-linear"></div>
                <!-- End of Breadcrumb -->
                <div class="row tw-grid tw-z-10">
                    <div v-if="tiposeleccion == 0">
                        <h1 style="
                            font-size: 30px;
                            color: black;
                            text-align: center;
                        ">
                            Información de roles
                        </h1>
                    </div>

                    <div v-else-if="tiposeleccion == 1">
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
                                    <InputText label="Hora de creación" :placeholder="date.toLocaleTimeString()"
                                        readonly />
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

                    <div v-else-if="tiposeleccion == 2">
                        <ECol>
                            <button class="tw-bg-green-600 tw-py-1 tw-text-white" style="margin-right: 40px"
                                @click="btn_editar">
                                Editar
                            </button>

                            <button class="tw-bg-red-600 tw-py-1 tw-text-white" style="margin-right: 40px">
                                Eliminar
                            </button>
                        </ECol>
                        <h1 style="font-size: 35px; text-align: center">Cajero</h1>
                        <p style="font-size: 20px; text-decoration: underline">
                            Nombre:
                        </p>
                        <p style="font-size: 15px">Nombre</p>
                        <p style="font-size: 20px; text-decoration: underline">
                            Fecha de creación:
                        </p>
                        <p style="font-size: 15px">Nombre</p>
                        <p style="font-size: 20px; text-decoration: underline">
                            Creado por:
                        </p>
                        <p style="font-size: 15px">Nombre</p>
                        <!--
                            <p style="font-size: 20px; text-decoration: underline">
                            Permisos:
                            </p>
                        -->
                    </div>
                </div>
            </main>
        </div>
    </ECard>
</template>
