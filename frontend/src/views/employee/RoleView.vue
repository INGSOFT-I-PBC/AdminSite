<script setup lang="ts">
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import ECol from '@components/custom/ECol.vue'
    import ERow from '@components/custom/ERow.vue'
    import InputText from '@components/custom/InputText.vue'
    import { useAuthStore } from '@store'
    import { useRoleStore } from '@store/role'
    import type { Role } from '@store/types'
    import { Form as EForm } from 'vee-validate'

    import { onMounted } from 'vue'

    /*Name of the page*/
    const pageName = 'Roles'

    /*Stores*/
    const roleRepository = useRoleStore()
    const authStore = useAuthStore()

    /* Variables del front */
    const date = new Date()
    const createdBy = authStore.userData?.name

    const tiposeleccion = ref(0)

    /*Loading*/
    const showWaitOverlay = ref<boolean>(true)

    /*Pagination*/
    const perPage = ref(7)
    const currentPage = ref(1)
    const totalRows = ref(100)

    function onSubmit() {
        tiposeleccion.value = 0
    }

    function btn_agregar(): void {
        tiposeleccion.value = 1
    }

    const form = ref<Form>({
        roles: [],
    })
    type Form = {
        roles: Role[]
    }

    async function showRoles(page: number) {
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

    onMounted(() => {
        return showRoles(null, 1)
    })
</script>

<template>
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
                <div class="container-fluid" style="padding: 0">
                    <EButton @click="btn_agregar()" variant="secondary"
                        >+ Agregar rol
                    </EButton>
                </div>
            </nav>
            <div
                class="row d-inline-flex allign-content-center tw-bg-slate-50 dark:tw-bg-slate-700">
                <div
                    class="col-2 mx-1 tw-flex-col tw-rounded-lg tw-bg-white dark:tw-bg-slate-800">
                    <b-pagination
                        v-model="currentPage"
                        :total-rows="totalRows"
                        :per-page="perPage"
                        button
                        aria-controls="b-list-warehouses"
                        align="center"
                        @page-click="onPageChanged"
                        :limit="3"
                        hide-goto-end-buttons
                        class="paginator"></b-pagination>

                    <b-list-group
                        :per-page="perPage"
                        :current-page="currentPage"
                        class="button-group">
                        <b-list-group-item
                            v-for="role in form.roles"
                            :key="role.id"
                            button>
                            {{ role.name }}
                        </b-list-group-item>
                    </b-list-group>
                </div>
                <div
                    v-if="tiposeleccion == 1"
                    class="col-md tw-bg-slate-50 dark:tw-bg-slate-700">
                    <EForm @submit="onSubmit">
                        <ERow>
                            <ECol cols="12" lg="6" xl="6">
                                <InputText
                                    label="Nombre del rol"
                                    placeholder="Escriba el nombre del rol" />
                            </ECol>
                            <ECol cols="12" lg="6" xl="6">
                                <InputText
                                    label="Fecha de creación"
                                    :placeholder="date.toLocaleDateString()"
                                    readonly />
                            </ECol>
                        </ERow>
                        <ERow>
                            <ECol>
                                <InputText
                                    label="Hora de creación"
                                    :placeholder="date.toLocaleTimeString()"
                                    readonly />
                            </ECol>
                            <ECol>
                                <InputText
                                    label="Creado por"
                                    :placeholder="createdBy"
                                    readonly />
                            </ECol>
                        </ERow>
                        <ERow>
                            <label class="form-label"> Permisos </label>
                        </ERow>
                        <EButton
                            left-icon="fa-floppy-disk"
                            icon-provider="awesome">
                            Guardar
                        </EButton>
                    </EForm>
                </div>
            </div>
        </ECard>
    </WaitOverlay>
</template>
