<script  setup lang="ts">
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
    import { useRoute, useRouter } from 'vue-router'
    const model = ref(null)

    const router = useRouter()


     function onSubmit(value:any) {
        console.log(value)

    }



      function validateID(value:any) {
          // if the field is empty
          if (!value) {
            return 'Este campo es requerido';
          }
          if( value.length!=10 || isNaN(value) ){
            return 'Inválido'; }

          return true;
        }

        function validateCell(value:any) {
          // if the field is empty
          if (!value) {
            return 'Este campo es requerido';
          }
          if( value.length!=10 || isNaN(value) ){
            return 'Inválido'; }

          return true;
        }

        function validateId(value:any) {
          // if the field is empty
          if (!value) {
            return 'Este campo es requerido';
          }
          if( value.length!=10 || isNaN(value) ){
            return 'Inválido'; }

          return true;
        }

      function validateName(value:any) {
          // if the field is empty
          if (!value) {
            return 'Este campo es requerido';
          }
          if(!isNaN(value)){
            return 'Inválido';

          }
          var regex = /^[a-zA-ZÀ-ÿ ]+$/

          if(!regex.test(value)){
            return 'Inválido';

          }

          return true;
        }
        function validateDate(value:any) {
          // if the field is empty
          if (!value) {
            return 'Este campo es requerido';
          }
          var date_regex = /^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$/
          if(!date_regex.test(value)){
             return 'Inválido';


          }

          return true;
        }

        function validateEmail(value:any) {

          if (!value) {
            return 'Este campo es requerido';
          }

          var correo=/^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/
          if(!correo.test(value)){
            return 'Inválido';
          }


          return true;
        }

        function validateProvincia(value:any) {
          // if the field is empty
          if (!value) {
            return 'Este campo es requerido';
          }
          if(!isNaN(value)){
            return 'Inválido';

          }
          var regex = /^[a-zA-ZÀ-ÿ ]+$/

          if(!regex.test(value)){
            return 'Inválido';

          }

          return true;
        }

        function validateCiudad(value:any) {
          // if the field is empty
          if (!value) {
            return 'Este campo es requerido';
          }
          if(!isNaN(value)){
            return 'Inválido';

          }
          var regex =/^[a-zA-ZÀ-ÿ ]+$/

          if(!regex.test(value)){
            return 'Inválido';

          }

          return true;
        }
        function validateDireccion(value:any) {
          // if the field is empty
          if (!value) {
            return 'Este campo es requerido';
          }

          return true;
        }
    </script>


<template>
    <main>
        <div class="container" style="border-radius: 5px">
      <EForm @submit="onSubmit" action='/usuarios/empleados' method="get">
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
    <Field name="email"  class="form-control" type="email" :rules="validateID" />
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
                <Field name="date"  placeholder="dd/mm/yyyy" class="form-control" type="email"  :rules="validateDate"/>
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
                    Teléfono*
                </h6>
                <Field name="celular"  class="form-control" type="email" :rules="validateCell" />
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
                    Sexo
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
                        <Field name="provincia"  class="form-control" type="email" :rules="validateProvincia" />
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
                <Field name="ciudad"  class="form-control" type="email" :rules="validateCiudad"/>
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
                <Field name="correo"  class="form-control" type="email" :rules="validateEmail"/>
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
                            Dirección domiciliaria*
                        </h6>
                        <Field name="direccion"  class="form-control" type="email" :rules="validateDireccion" />
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



        <button  style="
                        font-size: 15px;
                        color: black;
                        text-align: center;
                        width:50%;
                        margin-left:25%;
                        margin-right:25%;
                        margin-top:10px;
                        color: white;
                        background-color: #555555;

                    ">  Guardar </button>
      </EForm>
      </div>
    </main>
  </template>
