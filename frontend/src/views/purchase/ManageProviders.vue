<script setup lang="ts">
    import { type ProviderSearchParam, useProviderStore } from '@store/provider'
    import type { Provider } from '@store/types/provider.model'
    import { BBadge, BvEvent } from 'bootstrap-vue-3'
    import * as yup from 'yup'

    import { useToast } from 'vue-toastification'

    import {
        EButton,
        EButtonGroup,
        ECard,
        InputText,
        ModalDialog,
        Title,
        WaitOverlay,
    } from '@custom-components'

    import AddNewProvider from './AddNewProvider.vue'

    /**
     * Type helper definitions for this view
     */
    type ConfirmationType = 'delete' | 'update' | 'activate'
    /**
     * Utility constants and variables
     */
    const providerRepository = useProviderStore()
    const toast = useToast()
    const isLoading = ref(false)
    const showConfirmationDialog = ref(false)
    const confirmationType = ref<ConfirmationType>('delete')
    const confirmationTarget = ref<Provider>()
    const showUpdateDialog = ref(false)
    const targetUpdateProvider = ref<Provider>()

    // Search Params
    type SearchParam = PaginationOptions & ProviderSearchParam
    const searchParam: SearchParam = {
        page: 1,
        name: undefined,
        document_path: undefined,
        email: undefined,
        per_page: 25,
    }
    /**
     * Search form
     */
    const searchSchema = yup.object({
        name: yup.string(),
        email: yup.string(),
        document_path: yup.string(),
    })

    function searchProviders(searchData: ProviderSearchParam) {
        console.debug('Search with params:', searchData)
        searchParam.document_path = searchData.document_path
        searchParam.email = searchData.email
        searchParam.name = searchData.name
        searchParam.page = 1
        makeSearch()
    }
    function makeSearch() {
        isLoading.value = true
        providerRepository
            .fetchProviders(searchParam)
            .catch(() => {
                toast.error('No se pudo realizar la búsqueda ')
            })
            .finally(() => {
                isLoading.value = false
            })
    }
    function deleteItem(provider: Provider) {
        providerRepository
            .deleteProvider(provider.id)
            .then(() => {
                toast.success('Desactivado correctamente')
                searchParam.page = 1
                makeSearch()
            })
            .catch(err => {
                console.error(err)
                toast.error(
                    `No se pudo eliminar el usuario ${provider.bussiness_name}`
                )
            })
    }

    function dispatchConfirmation(type: ConfirmationType, target?: Provider) {
        if (target == undefined) {
            console.warn("Couldn't complete the operation target undefined")
            return
        }
        switch (type) {
            case 'delete':
                console.debug('Launching delete method')
                deleteItem(target)
                break
            case 'update':
                // TODO: Make this if necessary
                break
            case 'activate':
                console.debug('Launching update method')
                providerRepository
                    .createProvider(target)
                    .then(() => {
                        toast.success('Proveedor reactivado con éxito')
                        searchParam.page = 1
                        makeSearch()
                    })
                    .catch(() => {
                        toast.error('No se pudo reactivar al proveedor')
                    })
            // updateProvider(target)
        }
        showConfirmationDialog.value = false
    }
    function onPaginationClick(event: BvEvent, page: number) {
        searchParam.page = page
        makeSearch()
    }
    /**
     * Initial execution
     */
    makeSearch()
</script>

<template>
    <!-- Confirmation dialog -->
    <ModalDialog
        v-model:show="showConfirmationDialog"
        button-type="ok-cancel"
        title="¿Está seguro de continuar?"
        ok-text="Proceder"
        @ok="dispatchConfirmation(confirmationType, confirmationTarget)">
        <span>
            El proveedor va a ser
            {{
                confirmationType == 'delete'
                    ? 'borrado'
                    : confirmationType == 'activate'
                    ? 'reactivado'
                    : 'actualizado'
            }}, ¿está seguro de continuar la operación?
        </span>
    </ModalDialog>
    <!-- Update provider values Dialog -->
    <ModalDialog
        :show="showUpdateDialog"
        button-type="cancel-only"
        ok-text="Modificar"
        title="Actualizando datos del proveedor"
        size="3xl"
        @cancel="
            () => {
                showUpdateDialog = false
            }
        ">
        <AddNewProvider
            update-mode
            :update-provider-model="targetUpdateProvider"
            @on-success="
                () => {
                    toast.success('Proveedor actualizado correctamente')
                    showUpdateDialog = false
                }
            "
            @on-error="
                () => {
                    toast.error(
                        'Se produjo un error al actualizar el proveedor, inténtelo más tarde'
                    )
                }
            " />
    </ModalDialog>
    <!-- Main card with the screen -->
    <ECard>
        <Title size="3xl">Gestión de proveedores</Title>
        <WaitOverlay :show="isLoading">
            <div class="row align-items-middle justify-content-center p-3">
                <div class="col col-12 col-xxl-11">
                    <div>
                        <Title
                            class="tw-absolute tw-w-auto -tw-top-4 tw-left-5 tw-z-[2] tw-bg-slate-50 dark:tw-bg-slate-800 px-2">
                            Cuadro de búsqueda
                        </Title>
                        <div
                            class="tw-ring tw-ring-slate-800 dark:tw-ring-primary tw-py-3 tw-px-5 tw-mt-4 tw-rounded-md">
                            <VeeForm
                                @submit="searchProviders"
                                :validation-schema="searchSchema">
                                <div class="row align-items-end gy-3 gx-2">
                                    <div class="col col-12 col-lg-6 col-xxl-4">
                                        <VeeField
                                            name="name"
                                            v-slot="{ field, handleInput }">
                                            <InputText
                                                label="Nombre"
                                                :model-value="field.value as string"
                                                @update:model-value="
                                                    handleInput
                                                "
                                                no-info-label />
                                        </VeeField>
                                    </div>
                                    <div class="col col-12 col-lg-6 col-xxl-5">
                                        <VeeField
                                            name="email"
                                            v-slot="{ field, handleInput }">
                                            <InputText
                                                label="Correo"
                                                :model-value="field.value as string"
                                                @update:model-value="
                                                    handleInput
                                                "
                                                no-info-label />
                                        </VeeField>
                                    </div>
                                    <div class="col col-12 col-lg-6 col-xxl-3">
                                        <VeeField
                                            name="document_path"
                                            v-slot="{ field, handleInput }">
                                            <InputText
                                                label="Ruc/Cedula/Pasaporte"
                                                :model-value="field.value as string"
                                                @update:model-value="
                                                    handleInput
                                                "
                                                no-info-label />
                                        </VeeField>
                                    </div>
                                    <div class="col col-12 col-md-3 col-xxl-2">
                                        <EButton class="tw-w-full">
                                            Buscar
                                        </EButton>
                                    </div>
                                    <div class="col col-12 col-md-3 col-xxl-2">
                                        <EButton type="reset" class="tw-w-full">
                                            Limpiar
                                        </EButton>
                                    </div>
                                </div>
                            </VeeForm>
                        </div>
                    </div>
                </div>
                <!-- Content of the data-->
                <div class="col-12">
                    <div class="row gx-2 gy-3 my-4">
                        <div
                            class="col col-12"
                            v-if="!providerRepository.providers?.data?.length">
                            <Title
                                class="tw-text-center"
                                size="2xl"
                                text-color-class="tw-text-secondary dark:tw-text-slate-300"
                                >No hay datos disponibles</Title
                            >
                        </div>
                        <div
                            v-else
                            class="col col-12 col-md-6 col-lg-4 col-xxl-3 px-3"
                            v-for="provider in providerRepository.providers
                                ?.data"
                            :key="provider.id">
                            <BCard no-body dark>
                                <BCardBody>
                                    <div class="row justify-items-stretch">
                                        <div
                                            class="col-auto"
                                            v-if="!provider.is_active">
                                            <BBadge variant="warning"
                                                >Desactivado</BBadge
                                            >
                                        </div>
                                        <div class="col col-auto">
                                            <Title size="2xl">{{
                                                provider.name
                                            }}</Title>
                                        </div>
                                        <div class="col justify-items-stretch">
                                            <small
                                                class="tw-text-gray-600 tw-text-sm">
                                                {{ provider.phone_no }}
                                            </small>
                                        </div>
                                    </div>
                                    <span>{{ provider.bussiness_name }}</span>
                                </BCardBody>
                                <BCardFooter>
                                    <EButtonGroup>
                                        <template v-if="provider.is_active">
                                            <EButton
                                                class="tw-bg-green-500 tw-text-white"
                                                variant="success"
                                                left-icon="edit"
                                                @click="
                                                    () => {
                                                        targetUpdateProvider =
                                                            provider
                                                        showUpdateDialog = true
                                                    }
                                                ">
                                                Editar
                                            </EButton>
                                            <EButton
                                                variant="cancel"
                                                left-icon="trash"
                                                @click="
                                                    () => {
                                                        confirmationTarget =
                                                            provider
                                                        confirmationType =
                                                            'delete'
                                                        showConfirmationDialog = true
                                                    }
                                                ">
                                                Desactivar
                                            </EButton>
                                        </template>
                                        <EButton
                                            v-else
                                            variant="success"
                                            class="tw-bg-green-500 tw-text-white"
                                            left-icon="upload"
                                            @click="
                                                () => {
                                                    confirmationTarget =
                                                        provider
                                                    confirmationType =
                                                        'activate'
                                                    showConfirmationDialog = true
                                                }
                                            ">
                                            Activar
                                        </EButton>
                                    </EButtonGroup>
                                </BCardFooter>
                            </BCard>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <BPagination
                    align="center"
                    :total-rows="providerRepository.providers?.total ?? 1"
                    :per-page="searchParam.per_page ?? 10"
                    next-text="Siguiente"
                    prev-text="Anterior"
                    @page-click="onPaginationClick" />
            </div>
        </WaitOverlay>
    </ECard>
</template>

<style lang="scss" scoped>
    .card {
        --bs-card-bg: theme(backgroundColor.slate.100);
        @media (prefers-color-scheme: dark) {
            --bs-card-bg: theme(backgroundColor.slate.600);
        }
    }
    .pagination {
        --bs-pagination-active-bg: theme(backgroundColor.primary.light);
        @media (prefers-color-scheme: dark) {
            --bs-pagination-active-color: theme(backgroundColor.slate.700);
            --bs-pagination-bg: theme(backgroundColor.slate.800);
            --bs-pagination-color: #ff0;
            --bs-pagination-disabled-bg: theme(backgroundColor.slate.700);
            --bs-pagination-disabled-border-color: theme(
                backgroundColor.slate.900
            );
        }
    }
</style>
