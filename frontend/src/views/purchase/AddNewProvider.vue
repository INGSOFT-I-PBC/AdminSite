<template>
    <ECard>
        <Title size="3xl">Informacion general</Title>
        <VeeForm
            @submit="onSubmit"
            @invalid-submit="onFailedSubmit"
            :validation-schema="vSchema"
            :initial-values="initialValues">
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
                            :formatter="(txt: string | null) => txt?.replace(/[^-+()0-9\s]/g, '') ?? ''"
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
                <div class="col col-12 col-xxl-5">
                    <SimpleFormInput name="address" label="Dirección" />
                </div>
                <template v-if="updateMode">
                    <div class="col col-12 col-lg-6">
                        <InputText
                            label="Creado por"
                            readonly
                            :model-value="`${creatorData?.name} ${creatorData?.lastname}`" />
                    </div>
                    <div class="col col-12 col-lg-6">
                        <InputText
                            label="Fecha creación"
                            readonly
                            :model-value="
                                moment(updateProviderModel?.created_at).format(
                                    'YYYY-MM-DD'
                                )
                            " />
                    </div>
                </template>
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
                <div class="col col-auto mt-2">
                    <InputText
                        label="Latitud"
                        readonly
                        placeholder="--.-------"
                        :model-value="mark.latitude" />
                </div>
                <div class="col col-auto mt-2">
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
        </VeeForm>
    </ECard>
</template>

<script lang="ts" setup>
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import InputText from '@components/custom/InputText.vue'
    import Title from '@components/custom/Title.vue'
    import { useEmployeeStore } from '@store'
    import { useProviderStore } from '@store/provider'
    import type {
        BadValidationResponse,
        Employee,
        MessageResponse,
    } from '@store/types'
    import type { Provider, ProviderModel } from '@store/types/provider.model'
    import axios from 'axios'
    import moment from 'moment'
    import type MapBrowserEvent from 'ol/MapBrowserEvent'
    import type { Coordinate } from 'ol/coordinate'
    import { Field, type SubmissionContext, defineRule } from 'vee-validate'
    import { object, string } from 'yup'

    import { type PropType, computed } from 'vue'
    import { useToast } from 'vue-toastification'

    import { SimpleFormInput } from '@custom-components'

    defineRule('required', (value: unknown): boolean | string => {
        switch (typeof value) {
            case 'string':
                return value?.length > 0 ? true : 'El campo es obligatorio'
            default:
                return true
        }
    })

    const props = defineProps({
        updateMode: {
            type: Boolean,
            default: false,
        },
        updateProviderModel: {
            type: Object as PropType<Provider>,
            default: undefined, // fallback
        },
    })

    const emits = defineEmits(['onSuccess', 'onError'])

    /**
     * Utility
     */
    const toast = useToast()
    const providerRepository = useProviderStore()
    const employeeRepo = useEmployeeStore()
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
    const creatorData = ref<Employee>()
    //#endregion
    /**
     * Provider Form rules and definition
     */
    const initialValues = ref<Record<string, string>>({
        name: '',
        bussiness_name: '',
        website: '',
        email: '',
        phone_no: '',
        document_path: '',
        address: '',
    })

    const vSchema = object({
        name: string()
            .min(5, 'EL campo debe tener mínimo 5 caracteres')
            .max(128, 'Máximo 128 caracteres permitidos')
            .matches(/^\S.*\S$/g, 'No debe contener espacios al inicio o final')
            .required('El campo es obligatorio'),
        bussiness_name: string()
            .matches(/^\S.*\S$/g, 'No debe contener espacios al inicio o final')
            .max(128, 'Máximo 128 caracteres permitidos')
            .min(5, 'La razón social debe contener mínimo 5 caracteres')
            .required('El campo es obligatorio'),
        website: string()
            .matches(
                // /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)/,
                /^(http(s?)\:\/\/){0,1}(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$/g,
                'El campo debe ser un url válido'
            )
            .max(100, 'El url es demasiado largo')
            .min(7, 'El url debe contener mínimo 7 caracteres'),
        email: string()
            .email('Debe ser un email válido')
            .max(64, 'Email demasiado extenso')
            .min(10, 'El email debe contener mínimo 10 caracteres'),
        phone_no: string()
            .min(8, 'Número de teléfono muy corto')
            .max(25, 'Número de teléfono muy extenso')
            .required('El campo es obligatorio'),
        document_path: string()
            .min(10, 'Mínimo 10 dígitos')
            .max(128, 'El documento ingresado es muy extenso')
            .matches(/\d/g, 'El campo solo debe contener dígitos')
            .required('El campo es obligatorio'),
        address: string()
            .min(7, 'Mínimo 7 caracteres')
            .max(512, 'La dirección es muy larga')
            .required('El campo es obligatorio'),
    })

    const mark = computed(() => ({
        latitude: markPosition.value?.length
            ? markPosition.value[0].toString()
            : undefined,
        longitude: markPosition.value?.length
            ? markPosition.value[1].toString()
            : undefined,
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
        if (props.updateMode) {
            providerRepository
                .updateProvider(
                    props.updateProviderModel!.id,
                    data as unknown as ProviderModel
                )
                .then(it => emits('onSuccess', it))
                .catch(err => emits('onError', err))
            return
        }
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
                if (
                    axios.isAxiosError(error) &&
                    (error.response?.status ?? 0) >= 400 &&
                    (error.response?.status ?? 0) < 500
                ) {
                    const request = error.response
                        ?.data as BadValidationResponse
                    if (request.website) {
                        toast.error('La URL es inválida')
                    } else {
                        toast.error('Proveedor ya existente')
                    }
                } else {
                    toast.error('No se pudo guardar el proveedor')
                }
            })
    }
    //eslint-disable-next-line vue/no-setup-props-destructure
    if (props.updateMode && props.updateProviderModel) {
        employeeRepo
            .fetchEmployee(props.updateProviderModel?.created_by)
            .then(data => {
                creatorData.value = data
            })
            .catch(err => {
                toast.error(
                    'Fallo al obtener datos adicionales, intentelo más tarde'
                )
            })
        //eslint-disable-next-line vue/no-setup-props-destructure
        const { latitude, longitude } = props.updateProviderModel
        console.debug(
            'Setting the coordinates for already existing provider:',
            [latitude, longitude]
        )
        if (latitude != null && longitude != null) {
            const newPosition = [Number(latitude), Number(longitude)]
            markPosition.value = newPosition
            center.value = newPosition
            hasChanged.value = true
        }
        Object.entries(props.updateProviderModel).forEach(([prop, value]) => {
            if (prop in initialValues.value) {
                initialValues.value[prop] = value
            }
        })
    }
</script>

<style scoped></style>
