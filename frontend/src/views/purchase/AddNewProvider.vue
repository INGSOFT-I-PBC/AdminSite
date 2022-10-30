<template>
    <ECard>
        <Title size="3xl">Informacion general</Title>
        <ValidationForm
            @submit="onSubmit"
            @invalid-submit="onFailedSubmit"
            :validation-schema="vSchema">
            <div class="row align-items-middle">
                <div class="col col-12 col-lg-6 col-xxl-4">
                    <Field
                        name="name"
                        v-slot="{ field, handleChange, errorMessage }"
                        rules="required">
                        <InputText
                            label="Nombre"
                            :model-value="field.value as string"
                            @update:model-value="handleChange"
                            info-status="danger"
                            :info-label="errorMessage" />
                    </Field>
                </div>
                <div class="col col-12 col-lg-6 col-xxl-4">
                    <Field
                        name="bussiness_name"
                        v-slot="{ field, handleChange, errorMessage }"
                        rules="required">
                        <InputText
                            label="Razón Social"
                            :model-value="field.value as string"
                            @update:model-value="handleChange"
                            info-status="danger"
                            :info-label="errorMessage" />
                    </Field>
                </div>
                <div class="col col-12 col-lg-6 col-xxl-4">
                    <Field
                        name="document_path"
                        label="documento"
                        v-slot="{ field, handleChange, errorMessage }">
                        <InputText
                            label="RUC/Cédula/Pasaporte"
                            :model-value="field.value as string"
                            @update:model-value="handleChange"
                            info-status="danger"
                            :info-label="errorMessage" />
                    </Field>
                </div>

                <div class="col col-12 col-lg-3 col-xxl-3">
                    <Field
                        name="phone_no"
                        v-slot="{ field, handleChange, errorMessage }">
                        <InputText
                            label="Número de teléfono"
                            :model-value="field.value as string"
                            @update:model-value="handleChange"
                            info-status="danger"
                            :info-label="errorMessage" />
                    </Field>
                </div>
                <div class="col col-12 col-lg-7 col-xxl-3">
                    <Field
                        name="website"
                        v-slot="{ field, handleChange, errorMessage }">
                        <InputText
                            label="Sitio Web"
                            :model-value="field.value as string"
                            @update:model-value="handleChange"
                            info-status="danger"
                            :info-label="errorMessage" />
                    </Field>
                </div>
                <div class="col col-lg-5 col-xxl-3">
                    <Field
                        name="email"
                        v-slot="{ field, handleChange, errorMessage }">
                        <InputText
                            label="Correo electrónico"
                            :model-value="field.value as string"
                            @update:model-value="handleChange"
                            info-status="danger"
                            :info-label="errorMessage" />
                    </Field>
                </div>
                <div class="col col-12">
                    <Title size="2xl" class="tw-mb-2"
                        >Localización del proveedor</Title
                    >
                    <ol-map
                        ref="map"
                        :load-tiles-while-animating="true"
                        :load-tiles-while-interacting="true"
                        @singleclick="setLocation"
                        style="
                            height: 20rem;
                            color: black;
                            font-weight: bolder;
                        ">
                        <ol-view
                            ref="view"
                            v-model:center="center"
                            :rotation="rotation"
                            :zoom="zoom"
                            :projection="projection" />
                        <ol-overviewmap-control>
                            <ol-tile-layer>
                                <ol-source-osm />
                            </ol-tile-layer>
                        </ol-overviewmap-control>
                        <ol-overlay :position="markPosition" v-if="hasChanged">
                            <font-awesome-icon
                                icon="fa-solid fa-location-dot"
                                size="3x"
                                color="rgb(17, 24, 39)"
                                transform="left-6 up-16.5" />
                        </ol-overlay>

                        <!-- Controls layer-->
                        <ol-scaleline-control />
                        <ol-rotate-control />
                        <ol-zoom-control />
                        <ol-mouseposition-control />

                        <!-- Map Layer-->
                        <ol-tile-layer>
                            <ol-source-osm />
                        </ol-tile-layer>
                    </ol-map>
                </div>
                <div class="col col-6 col-xxl-3 mt-2">
                    <InputText
                        label="Latitud"
                        readonly
                        placeholder="--.-------"
                        :model-value="mark.latitude" />
                </div>
                <div class="col col-6 col-xxl-3 mt-2">
                    <InputText
                        label="Longitud"
                        readonly
                        placeholder="--.-------"
                        :model-value="mark.longitude" />
                </div>
            </div>
            <div class="row">
                <div class="col col-12 col-xxl-3 mt-3">
                    <EButton class="tw-w-full">Guardar</EButton>
                </div>
            </div>
        </ValidationForm>
    </ECard>
</template>

<script lang="ts" setup>
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import InputText from '@components/custom/InputText.vue'
    import Title from '@components/custom/Title.vue'
    import { useProviderStore } from '@store/provider'
    import type { ProviderModel } from '@store/types/provider.model'
    import type { Coordinate } from 'ol/coordinate'
    import type MapBrowserEvent from 'ol/MapBrowserEvent'
    import {
        defineRule,
        Field,
        Form as ValidationForm,
        type SubmissionContext,
    } from 'vee-validate'
    import { computed } from 'vue'
    import { useToast } from 'vue-toastification'
    import * as yup from 'yup'
    defineRule('required', (value: unknown): boolean | string => {
        switch (typeof value) {
            case 'string':
                return value?.length > 0 ? true : 'El campo es obligatorio'
            default:
                return true
        }
    })
    /**
     * Utility
     */
    const toast = useToast()
    const providerRepository = useProviderStore()
    /**
     * Map definition refs
     */
    //#region map
    const center = ref<Coordinate>([-79.897453, -2.203816])
    const rotation = ref(0)

    const markPosition = ref<Coordinate>()
    const zoom = ref(8)
    const projection = ref('EPSG:4326')
    const map = ref()
    const view = ref()
    const hasChanged = ref(false)
    //#endregion
    /**
     * Provider Form rules and definition
     */
    const vSchema = yup.object({
        name: yup
            .string()
            .min(5, 'EL campo debe tener mínimo 5 caracteres')
            .max(128, 'Máximo 128 caracteres permitidos')
            .matches(/^\S.*\S$/g, 'No debe contener espacios al inicio o final')
            .required('El campo es obligatorio'),
        bussiness_name: yup
            .string()
            .matches(/^\S.*\S$/g, 'No debe contener espacios al inicio o final')
            .max(128, 'Máximo 128 caracteres permitidos')
            .min(5, 'La razón social debe contener mínimo 5 caracteres')
            .required('El campo es obligatorio'),
        website: yup
            .string()
            .matches(
                /[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/,
                'El campo debe ser un url válido'
            )
            .max(100, 'El url es demasiado largo')
            .min(7, 'El url debe contener mínimo 7 caracteres'),
        email: yup
            .string()
            .email('Debe ser un email válido')
            .max(64, 'Email demasiado extenso')
            .min(10, 'El email debe contener mínimo 10 caracteres'),
        phone_no: yup
            .string()
            .min(8, 'Número de teléfono muy corto')
            .max(25, 'Número de teléfono muy extenso')
            .matches(/\d/g, 'El campo solo debe contener dígitos')
            .required(),
        document_path: yup
            .string()
            .min(7, 'Mínimo 7 dígitos')
            .max(128, 'El documento ingresado es muy extenso')
            .matches(/\d/g, 'El campo solo debe contener dígitos')
            .required('El campo es obligatorio'),
    })

    const mark = computed(() => ({
        latitude: markPosition.value?.length
            ? markPosition.value[0].toString()
            : undefined,
        longitude: markPosition.value?.length
            ? markPosition.value[1].toString()
            : undefined,
        // longitude: markPosition.value?[1]
    }))

    function setLocation(event: MapBrowserEvent<MouseEvent>) {
        if (!hasChanged.value) {
            hasChanged.value = true
        }
        markPosition.value = event.coordinate
        console.debug('Coordinated of mark: ', event.coordinate)
    }
    function onFailedSubmit() {
        toast.error('Verifique los datos del formulario')
    }

    function onSubmit(value: unknown, { resetForm }: SubmissionContext) {
        console.debug('validation object: ', value)
        const data = Object.assign({}, value, mark.value)
        providerRepository
            .createProvider(data as unknown as ProviderModel)
            .then(() => {
                toast.success('Proveedor guardado exitosamente')
                resetForm()
                mark.value.latitude = undefined
                mark.value.longitude = undefined
                hasChanged.value = false
            })
            .catch(error => {
                console.error(error)
                if (error?.code && error?.response?.status >= 400) {
                    toast.error('Proveedor ya existente')
                } else {
                    toast.error('No se pudo guardar el proveedor')
                }
            })
    }
</script>

<style scoped></style>
