<script setup lang="ts">
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import ECol from '@components/custom/ECol.vue'
    import ERow from '@components/custom/ERow.vue'
    import InputText from '@components/custom/InputText.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import Title from '@components/custom/Title.vue'
    import Table from '@components/holders/Table.vue'
    import * as VeeValidate from 'vee-validate'
    import { ErrorMessage, Field } from 'vee-validate'
    import { Form as EForm } from 'vee-validate'

    import { computed, reactive } from 'vue'
    import { useRoute, useRouter } from 'vue-router'

    const model = ref(null)

    const router = useRouter()
    const tipopago = ref(true)

    function changeCountry(event: any) {
        if (
            event.target.options[event.target.options.selectedIndex].text ==
            'En efectivo'
        ) {
            tipopago.value = true
        } else {
            tipopago.value = false
        }
    }

    function onSubmit(value: any) {
        console.log(value)
        router.push({ path: '/facturacion' })
    }

    function validateID(value: any) {
        // if the field is empty
        if (!value) {
            return 'Este campo es requerido'
        }
        if (isNaN(value)) {
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

    function validateDate2(value: any) {
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

    function validateSucursal(value: any) {
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

    function validatePago(value: any) {
        const regex = /^[a-zA-ZÀ-ÿ ]+$/
        if (tipopago.value == false && !value) {
            return 'Este campo es necesario '
        }

        if (tipopago.value == false && isNaN(value)) {
            return 'Inválido'
        }
        if (tipopago.value == false && regex.test(value)) {
            return 'Inválido'
        }

        if (tipopago.value == true) {
            return true
        }
        return true
    }
</script>

<template>
    <main>
        <div class="container" style="border-radius: 5px">
            <EForm @submit="onSubmit">
                <div class="row g-3">
                    <div class="col">
                        <h6
                            style="
                                font-size: 15px;
                                color: black;
                                text-align: left;
                            ">
                            Código de factura *
                        </h6>
                        <Field
                            name="email"
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
                    <div class="col">
                        <h6
                            style="
                                font-size: 15px;
                                color: black;
                                text-align: left;
                            ">
                            Fecha de emisión *
                        </h6>
                        <Field
                            name="fecha"
                            placeholder="dd/mm/yyyy"
                            class="form-control"
                            type="Date"
                            :rules="validateDate" />
                        <div class="col">
                            <ErrorMessage
                                name="fecha"
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
                            Fecha de devolución*
                        </h6>
                        <Field
                            name="date"
                            placeholder="dd/mm/yyyy"
                            class="form-control"
                            type="Date"
                            :rules="validateDate2" />
                        <div class="col">
                            <ErrorMessage
                                name="date"
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
                            Cajero *
                        </h6>
                        <Field
                            name="provincia"
                            class="form-control"
                            type="email"
                            :rules="validateProvincia" />
                        <div class="col">
                            <ErrorMessage
                                name="provincia"
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
                            Cliente *
                        </h6>
                        <select
                            class="form-select"
                            aria-label="Default select example">
                            <option value="1">cliente 1</option>
                            <option value="2">cliente 2</option>
                            <option value="3">cliente 3</option>
                        </select>
                    </div>
                    <div class="col">
                        <EButton variant="secondary" style="margin-top: 20px">
                            +
                        </EButton>
                    </div>
                    <div class="col">
                        <h6
                            style="
                                font-size: 15px;
                                color: black;
                                text-align: left;
                            ">
                            Identificación
                        </h6>
                        <Field name="id" class="form-control" type="email" />
                    </div>
                    <div class="col">
                        <h6
                            style="
                                font-size: 15px;
                                color: black;
                                text-align: left;
                            ">
                            Teléfono
                        </h6>
                        <Field
                            name="celular"
                            class="form-control"
                            type="email" />
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
                            Dirección
                        </h6>
                        <Field
                            name="direccion"
                            class="form-control"
                            type="email" />
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
                </div>

                <div class="row g-3">
                    <div class="col">
                        <h6
                            style="
                                font-size: 15px;
                                color: black;
                                text-align: left;
                            ">
                            Correo
                        </h6>
                        <Field
                            name="correo"
                            class="form-control"
                            type="email" />
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
                            Sucursal *
                        </h6>
                        <Field
                            name="ciudad"
                            class="form-control"
                            type="email"
                            :rules="validateSucursal" />
                        <div class="col">
                            <ErrorMessage
                                name="ciudad"
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
                            Tipo de pago:
                        </h6>
                        <select
                            class="form-select"
                            aria-label="Default select example"
                            @change="changeCountry($event)">
                            <option value="1">En efectivo</option>
                            <option value="2">Con tarjeta</option>
                        </select>
                    </div>
                    <div class="col">
                        <h6
                            style="
                                font-size: 15px;
                                color: black;
                                text-align: left;
                            ">
                            Últimos dígitos de tarjeta
                        </h6>
                        <Field
                            name="pago"
                            class="form-control"
                            type="email"
                            :rules="validatePago" />
                        <div class="col">
                            <ErrorMessage
                                name="pago"
                                style="
                                    font-size: 10px;
                                    color: red;
                                    text-align: left;
                                " />
                        </div>
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
                            Estado:
                        </h6>
                        <select
                            class="form-select"
                            aria-label="Default select example">
                            <option selected>Activa</option>
                            <option value="1">Anulada</option>
                        </select>
                    </div>
                    <div class="col">
                        <EButton variant="secondary" style="margin-top: 20px"
                            >Añadir producto</EButton
                        >
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
                    Facturar
                </button>
            </EForm>
        </div>
    </main>
</template>
