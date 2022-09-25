<script >
     import ECard from '@components/custom/ECard.vue'
    import ERow from '@components/custom/ERow.vue'
    import ECol from '@components/custom/ECol.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import InputText from '@components/custom/InputText.vue'
    import EButton from '@components/custom/EButton.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import Title from '@components/custom/Title.vue'
    import Table from '@components/holders/Table.vue'
    import { computed, reactive } from 'vue'
    import * as VeeValidate from 'vee-validate'
    import { Field, ErrorMessage } from 'vee-validate';
    import { Form as EForm } from 'vee-validate';



    export default {
      components: {
        EForm,
        Field,
        ErrorMessage,
      },
      methods: {
        onSubmit(value) {
          console.log(value, null, 2);



        },

        validateId(value) {
          // if the field is empty
          if (!value) {
            return 'Este campo es requerido';
          }
          if( value.length!=10 || isNaN(value) ){
            return 'Inválido';

          }
          // if the field is not a valid email
          // All is good
          return true;
        },

        validateName(value) {
          // if the field is empty
          if (!value) {
            return 'Este campo es requerido';
          }
          if(!isNaN(value)){
            return 'Inválido';

          }
          // if the field is not a valid email
          // All is good
          return true;
        },

        validateEmail(value) {
          // if the field is empty
          if (!value) {
            return 'This field is required';
          }
          // if the field is not a valid email
          // All is good
          return true;
        },
      },
    };
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
                            Fecha de creación
                        </h6>
                        <input
                            type="text"
                            class="form-control"
                            placeholder="23/08/2022"
                            disabled="false"
                            aria-label="First name" />
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
                            placeholder="15:00"
                            disabled="false"
                            aria-label="First name" />
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
                            aria-label="First name" />
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
    Cédula* </h6>
    <Field name="email"  class="form-control" type="email" :rules="validateId" />
    <div class="col">
    <ErrorMessage name="email"  style="
        font-size: 10px;
        color: red;
        text-align: left;
    "/>
    </div>
 </div>
 <div class="col">
                <h6
                    style="
                        font-size: 15px;
                        color: black;
                        text-align: left;
                    ">
                    Nombres y apellidos *
                </h6>
                <Field name="name"  class="form-control" type="email" :rules="validateName" />
                 <div class="col">
                   <ErrorMessage name="name"  style="  font-size: 10px;  color: red; text-align: left;"/>
                 </div>
</div>
<div class="col">
                <h6
                    style="
                        font-size: 15px;
                        color: black;
                        text-align: left;
                    ">
                    Fecha de Nacimiento*
                </h6>
                <Field name="date"  class="form-control" type="email"  />
                 <div class="col">
                   <ErrorMessage name="date"  style="  font-size: 10px;  color: red; text-align: left;"/>
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
                    Teléfono
                </h6>
                <Field name="celular"  class="form-control" type="email"  />
                 <div class="col">
                   <ErrorMessage name="celular"  style="  font-size: 10px;  color: red; text-align: left;"/>
                 </div>
            </div>
            <div class="col">
                <h6
                    style="
                        font-size: 15px;
                        color: black;
                        text-align: left;
                    ">
                    Sexo*
                </h6>
                <select
                    class="form-select"
                    aria-label="Default select example">
                    <option selected>Femenino</option>
                    <option value="1">Masculino</option>
                    <option value="2">Otro</option>
                </select>
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
                        type="checkbox"
                        role="switch"
                        id="flexSwitchCheckDefault" />
                    <label
                        class="form-check-label"
                        for="flexSwitchCheckDefault"></label>
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
                            Provincia *
                        </h6>
                        <Field name="provincia"  class="form-control" type="email"  />
                 <div class="col">
                   <ErrorMessage name="provincia"  style="  font-size: 10px;  color: red; text-align: left;"/>
                 </div>

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
                <Field name="ciudad"  class="form-control" type="email"  />
                 <div class="col">
                   <ErrorMessage name="ciudad"  style="  font-size: 10px;  color: red; text-align: left;"/>
                 </div>
            </div>
            <div class="col">
                <h6
                    style="
                        font-size: 15px;
                        color: black;
                        text-align: left;
                    ">
                    Correo*
                </h6>
                <Field name="correo"  class="form-control" type="email"  />
                 <div class="col">
                   <ErrorMessage name="correo"  style="  font-size: 10px;  color: red; text-align: left;"/>
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
                            Dirección domiciliaria
                        </h6>
                        <Field name="direccion"  class="form-control" type="email"  />
                 <div class="col">
                   <ErrorMessage name="direccion"  style="  font-size: 10px;  color: red; text-align: left;"/>
                 </div>
                    </div>
                    <div class="col">
                <h6
                    style="
                        font-size: 15px;
                        color: black;
                        text-align: left;
                    ">
                    Rol:
                </h6>
                <select
                    class="form-select"
                    aria-label="Default select example">
                    <option selected>Cajero</option>
                    <option value="1">Vendedor</option>
                    <option value="2">Two</option>
                    <option value="3">Three</option>
                </select>
            </div>

                </div>



        <button > Sign up</button>
      </EForm>
      </div>
    </main>
  </template>
