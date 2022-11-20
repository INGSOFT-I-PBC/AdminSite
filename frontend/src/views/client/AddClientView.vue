<!-- eslint-disable vue/valid-v-model -->
<!-- eslint-disable vue/valid-v-model -->
<script setup lang="ts">
    import ECard from '@components/custom/ECard.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import { useAuthStore } from '@store'
    import { useClientStore } from '@store/client'
    import type {
        City,
        Client,
        Gender,
        MetaData,
        Province,
        Status,
    } from '@store/types'
    import { ErrorMessage, Field } from 'vee-validate'
    import { Form as EForm } from 'vee-validate'

    import { onMounted } from 'vue'
    import { useRouter } from 'vue-router'

    import WaitOverlay from '../../components/custom/WaitOverlay.vue'

    const hoy = new Date()
    const showWaitOverlay = ref<boolean>(false)
    const itemLoading = ref(false)
    const productModalShowError = ref(false)
    const productModalShow = ref(false)
    const tipoid = ref(true)
    const authStore = useAuthStore()
    const nameEmployee = authStore.userData?.name
    const router = useRouter()
    const itemStore = useClientStore()
    const form = ref<Form>({
        provinces: [],
    })
    type Form = {
        provinces: Province[]
    }
    const formGender = ref<FormGender>({
        genders: [],
    })
    type FormGender = {
        genders: Gender[]
    }
    const formCity = ref<FormCity>({
        cities: [],
    })
    type FormCity = {
        cities: City[]
    }
    const formStatus = ref<Status>({
        id: 0,
        name: 'active',
    })

    const formClientError2: MetaData = {}

    const formClient = ref<Client>({
        number_id: '',
        name: '',
        address: '',
        business_name: 'razon social',
        email: '',
        phone_number: '',
        city: null,
        province: null,
        created_by: authStore.userData?.employee,
        gender: null,
        status: 0,
    })

    const loadProvince = async () => {
        itemLoading.value = true
        form.value.provinces = await itemStore.fetchAllProvince()
        console.log(form.value.provinces)
        itemLoading.value = false
    }
    const loadCity = async () => {
        if (
            Number(formClient.value.province) != 0 &&
            formClient.value.province != null
        ) {
            formCity.value.cities = await itemStore.fetchAllCity(
                Number(formClient.value.province)
            )

            console.log(formCity.value.cities)
        }
    }
    const loadStatus = async (name: string) => {
        formStatus.value = await itemStore.fetchStatus(name)
        formClient.value.status = formStatus.value.id

        console.log(formStatus.value)
    }
    const loadGender = async () => {
        formGender.value.genders = await itemStore.fetchAllGender()
        console.log(formGender.value.genders)
    }
    function onShowModalGender() {
        loadGender()
    }
    function validarCheckbox() {
        const checkbox = document.getElementById(
            'checkClient'
        ) as HTMLInputElement
        if (formClient.value.status != 0) {
            if (!checkbox.checked) {
                loadStatus('inactive')
            } else {
                loadStatus('active')
            }
        }
    }
    function onShowModalCityClick() {
        loadCity()
    }
    function onShowModalClick() {
        loadProvince()
    }
    function saveClient() {
        itemStore
            .saveClient(formClient.value)
            .then(() => {
                router.push({ path: '/usuarios/clientes' })
            })
            .catch(error => {
                if (error.response.status == 400) {
                    productModalShowError.value = true
                    formClientError2.value = error.response.data
                    showWaitOverlay.value = false
                }
            })
    }

    onMounted(() => {
        return (
            onShowModalClick(),
            loadStatus(formStatus.value.name),
            onShowModalGender()
        )
    })

    function changeCountry(event: any) {
        if (
            event.target.options[event.target.options.selectedIndex].text ==
            'Cédula'
        ) {
            tipoid.value = true
        } else {
            tipoid.value = false
        }
    }

    function onSubmit(value: any) {
        productModalShow.value = true
        showWaitOverlay.value = true
    }
    function validateID(value: any) {
        // if the field is empty
        if (!value) {
            return 'Este campo es requerido'
        }
        if (isNaN(value)) {
            return 'Inválido'
        }
        if (tipoid.value == true && value.length != 10) {
            return 'Inválido # de cédula'
        }
        if (tipoid.value == false && value.length != 13) {
            return 'Inválido # de RUC'
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
    function validateDireccion(value: any) {
        // if the field is empty
        if (!value) {
            return 'Este campo es requerido'
        }

        return true
    }

    function validateRazon(value: any) {
        const regex = /^[a-zA-ZÀ-ÿ ]+$/

        if (tipoid.value == false && !value) {
            return 'Este campo es necesario '
        }
        if (tipoid.value == false && !isNaN(value)) {
            return 'Inválido'
        }

        if (tipoid.value == false && !regex.test(value)) {
            return 'Inválido'
        }

        if (tipoid.value == true) {
            return true
        }

        return true
    }
</script>

<template>
    <main>
        <WaitOverlay :show="showWaitOverlay">
            <ModalDialog v-model:show="productModalShowError" size="xl">
                <template #dialog-title>
                    <b class="tw-text-2xl">ERROR</b>
                </template>
                <div class="container">
                    <div
                        class="row tw-pb-3 align-content-center justify-content-center gy-2">
                        <template
                            v-for="[k, d] of Object.entries(
                                formClientError2.value
                            )"
                            :key="k">
                            <div class="row">
                                <span class="tw-w-1/2 tw-font-bold col-6"
                                    >{{ k }}:
                                </span>
                                <span class="col-6">{{ d?.toString() }}</span>
                            </div>
                        </template>
                    </div>
                </div>
            </ModalDialog>

            <ModalDialog
                id="product-modal"
                v-model:show="productModalShow"
                title="Agregar Producto"
                ok-text="Guardar"
                @ok="saveClient"
                button-type="ok-cancel">
                <h1 style="font-size: 15px; color: black; text-align: left">
                    ¿Está seguro de guardar al Cliente?
                </h1>
            </ModalDialog>
            <div class="container" style="border-radius: 5px">
                <ECard>
                    <EForm @submit="onSubmit">
                        <div class="row g-3">
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Fecha de creación
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    :placeholder="hoy.toLocaleDateString()"
                                    disabled="false"
                                    aria-label="Firs
                            t name" />
                            </div>

                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Hora de creación
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    disabled="false"
                                    aria-label="First name"
                                    :placeholder="hoy.toLocaleTimeString()" />
                            </div>
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Creado por
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    disabled="false"
                                    aria-label="First name"
                                    v-model="nameEmployee" />
                            </div>
                        </div>
                        <div class="row g-3">
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Tipo de identificación:
                                </h6>

                                <select
                                    @change="changeCountry($event)"
                                    class="form-select"
                                    aria-label="Default select example">
                                    <option selected value="1">Cédula</option>
                                    <option value="2">RUC</option>
                                </select>
                            </div>

                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Identificación*
                                </h6>
                                <Field
                                    name="email"
                                    v-model="formClient.number_id"
                                    class="form-control"
                                    type="email"
                                    :rules="validateID" />
                                <div class="col">
                                    <ErrorMessage
                                        name="email"
                                        style="
                                            font-size: 10px;
                                            color: red;
                                            text-align: left;
                                        " />
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Razón Social *
                                </h6>
                                <Field
                                    name="name"
                                    class="form-control"
                                    type="email"
                                    v-model="formClient.name"
                                    :rules="validateName" />
                                <div class="col">
                                    <ErrorMessage
                                        name="name"
                                        style="
                                            font-size: 10px;
                                            color: red;
                                            text-align: left;
                                        " />
                                </div>
                            </div>
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Sexo
                                </h6>
                                <select
                                    required
                                    id="selectGender"
                                    name="gender"
                                    class="form-select"
                                    v-model="formClient.gender"
                                    aria-label="Default select example">
                                    <option :value="null" selected disabled>
                                        --Seleccione--
                                    </option>
                                    <option
                                        v-for="gender in formGender.genders"
                                        :value="gender.id"
                                        :key="gender.id">
                                        {{ gender.name }}
                                    </option>
                                </select>
                            </div>
                        </div>
                        <div class="row g-3">
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Teléfono*
                                </h6>
                                <Field
                                    name="celular"
                                    class="form-control"
                                    type="email"
                                    v-model="formClient.phone_number"
                                    :rules="validateCell" />
                                <div class="col">
                                    <ErrorMessage
                                        name="celular"
                                        style="
                                            font-size: 10px;
                                            color: red;
                                            text-align: left;
                                        " />
                                </div>
                            </div>
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Provincia *
                                </h6>
                                <select
                                    @change="onShowModalCityClick()"
                                    :required="true"
                                    name="province"
                                    id="selectProvincia"
                                    class="form-select"
                                    v-model="formClient.province">
                                    <option :value="null" selected disabled>
                                        --Seleccione--
                                    </option>
                                    <option
                                        v-for="prov in form.provinces"
                                        :key="prov.id"
                                        :value="prov.id">
                                        {{ prov.name }}
                                    </option>
                                </select>
                            </div>
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Ciudad *
                                </h6>
                                <select
                                    required
                                    id="selectCiudad"
                                    name="city"
                                    class="form-select"
                                    aria-label="Default select example"
                                    v-model="formClient.city">
                                    <option :value="null" selected disabled>
                                        --Seleccione--
                                    </option>
                                    <option
                                        v-for="city in formCity.cities"
                                        :value="city.id"
                                        :key="city.id">
                                        {{ city.name }}
                                    </option>
                                </select>
                            </div>
                        </div>
                        <div class="row g-3">
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Correo*
                                </h6>
                                <Field
                                    name="correo"
                                    class="form-control"
                                    type="email"
                                    v-model="formClient.email"
                                    :rules="validateEmail" />
                                <div class="col">
                                    <ErrorMessage
                                        name="correo"
                                        style="
                                            font-size: 10px;
                                            color: red;
                                            text-align: left;
                                        " />
                                </div>
                            </div>
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Dirección domiciliaria*
                                </h6>
                                <Field
                                    name="address"
                                    class="form-control"
                                    type="email"
                                    v-model="formClient.address"
                                    :rules="validateDireccion" />
                                <div class="col">
                                    <ErrorMessage
                                        name="direccion"
                                        style="
                                            font-size: 10px;
                                            color: red;
                                            text-align: left;
                                        " />
                                </div>
                            </div>
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Estado
                                </h6>
                                <div class="form-check form-switch">
                                    <input
                                        class="form-check-input"
                                        name="status"
                                        type="checkbox"
                                        role="switch"
                                        id="checkClient"
                                        @change="validarCheckbox()"
                                        checked />
                                    <label
                                        class="form-check-label"
                                        for="flexSwitchCheckDefault"></label>
                                </div>
                            </div>
                        </div>

                        <button
                            style="
                                font-size: 15px;
                                color: black;
                                text-align: center;
                                width: 50%;
                                margin-left: 25%;
                                margin-right: 25%;
                                margin-top: 10px;
                                color: white;
                                background-color: #555555;
                            ">
                            Guardar
                        </button>
                    </EForm>
                </ECard>
            </div>
        </WaitOverlay>
    </main>
</template>
