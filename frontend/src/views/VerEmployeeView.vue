<script setup lang="ts">
    
     import ECard from '@components/custom/ECard.vue'
    import ERow from  '@components/custom/ERow.vue'
    import ECol from  '@components/custom/ECol.vue'
    import ListBox from  '@components/custom/ListBox.vue'
    import InputText from  '@components/custom/InputText.vue'
    import EButton from  '@components/custom/EButton.vue'
    import ModalDialog from  '@components/custom/ModalDialog.vue'
    import Title from  '@components/custom/Title.vue'
    import Table from  '@components/holders/Table.vue'
    import { computed, reactive } from 'vue'

    import {
        useRoute,
        useRouter,
    } from 'vue-router'
    const router = useRouter()

    function go2():void {
        router.push({ path: '/empleado' })
    }

</script>


<template>
    <main>
        <ECard> 

          <div
             class="container"
             style="
                border-radius: 5px;
             ">
            <!--BOTONES Usuario-->
            <div
                class="container text-center"
                style="padding: 10px">
                <div class="row">
                    <div class="col">
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
                                    disabled=false
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
                                    disabled=false
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
                                    placeholder="Admin"
                                    disabled=false
                                    aria-label="First name" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!--DIV DE BOTONES Y NAV-->
            <div class="container text-center">
                <div class="row">
                    <div class="col">
                        <div class="row g-3">
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Cédula *
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                     disabled=false
                                    aria-label="First name" />
                            </div>
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
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                     disabled=false
                                    aria-label="First name" />
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
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                     disabled=false
                                    aria-label="First name" />
                            </div>


                </div>
            </div>

            <!--BOTONES Usuario-->
            <div
                class="container text-center"
                style="padding: 10px">
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
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    disabled=false
                                    aria-label="First name" />
                                    
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
                                    disabled=false
                                    aria-label="Default select example">
                                    <option
                                        selected>
                                        Femenino
                                    </option>
                                    <option
                                        value="1">
                                        Masculino
                                    </option>
                                    <option
                                        value="2">
                                        Otro
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
                                    Estado
                                </h6>
                                <p> Icono </p>
       
                    </div>


                    
                </div>
            </div>

            <!--DIV DE BOTONES Y NAV-->
            <div class="container text-center">
                <div class="row">
                    <div class="col">
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
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    disabled=false
                                    aria-label="First name" />
                            </div>
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
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    disabled=false
                                    aria-label="First name" />
                                    
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
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    disabled=false
                                    aria-label="First name" />
                                     
                            </div>


                </div>

            </div>

            <div class="container text-center">
                <div class="row">
                    <div class="col">
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
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    disabled=false
                                    aria-label="First name" />
                                    
                            </div>
                        </div>
                    </div>
                </div>
             </div>

            <div class="container text-center">
               <div class="row">
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
                                    disabled=false
                                    aria-label="Default select example">
                                    <option
                                        selected>
                                        Cajero
                                    </option>
                                    <option
                                        value="1">
                                        Vendedor
                                    </option>
                                    <option
                                        value="2">
                                        Two
                                    </option>
                                    <option
                                        value="3">
                                        Three
                                    </option>
                                </select>
                            </div>
               </div>

            </div>



            <!--Espacio demas-->
            <div
                class="container text-center"
                style="padding: 10px"></div>
        </div>

        </ECard>

    </main>
</template>
