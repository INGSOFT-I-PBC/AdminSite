<script setup lang="ts">
    import {
        EButton,
        ECard,
        InputText,
        Title,
        WaitOverlay,
    } from '@custom-components'
    // import { Field, Form as ValidationForm } from 'vee-validate'
    import * as yup from 'yup'

    /**
     * Search form
     */
    const searchSchema = yup.object({
        name: yup.string(),
    })

    function searchProviders(searchData: unknown) {
        console.debug('Search with params:', searchData)
    }
</script>

<template>
    <ECard>
        <Title size="3xl">Gestión de proveedores</Title>
        <WaitOverlay>
            <div class="container">
                <div class="row align-items-middle justify-content-center p-3">
                    <div class="col col-12 col-xxl-11">
                        <div>
                            <Title
                                class="tw-absolute -tw-top-4 tw-left-5 tw-z-10 tw-bg-white dark:tw-bg-slate-800 px-2">
                                Cuadro de búsqueda
                            </Title>
                            <div
                                class="tw-ring tw-ring-slate-800 dark:tw-ring-primary tw-py-3 tw-px-5 tw-mt-4 tw-rounded-md">
                                <VeeForm
                                    @submit="searchProviders"
                                    :validation-schema="searchSchema">
                                    <div class="row align-items-end">
                                        <div class="col">
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
                                        <div
                                            class="col col-12 col-md-3 col-xxl-2">
                                            <EButton class="tw-w-full">
                                                Buscar
                                            </EButton>
                                        </div>
                                        <div
                                            class="col col-12 col-md-3 col-xxl-2">
                                            <EButton
                                                type="reset"
                                                class="tw-w-full">
                                                Limpiar
                                            </EButton>
                                        </div>
                                    </div>
                                </VeeForm>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Content of the data-->
                <div class="row">
                    <div class="col col-12"></div>
                </div>
                <div class="row">
                    <BPagination align="center" />
                </div>
            </div>
        </WaitOverlay>
    </ECard>
</template>
