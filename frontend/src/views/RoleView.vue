<script setup lang="ts">
    import { ref } from 'vue'
    import EButton from '@components/custom/EButton.vue'
    import ERow from '@components/custom/ERow.vue'
    import ECol from '@components/custom/ECol.vue'
    const message = ref('TODO: Make this view')
</script>


<template>
    <main>
        <ECard>
            <!--
            <h1 class="align-center text-center text-3xl font-bold">
                Bienvenido
            </h1>

            <div class="flex gap-3">
                <EButton>Test primary Button</EButton>
                <EButton type="secondary">Test secondary
                    Button</EButton>
            </div>
             -->
        </ECard>

        <div
            class="container"
            style="
                background-color: white;
                border-radius: 5px;
            ">
            <div
                class="container"
                style="
                    background-color: white;
                    padding: 10px;
                ">
                <h1
                    style="
                        font-size: 35px;
                        color: black;
                    ">
                    Roles
                </h1>

                <nav class="navbar">
                    <div class="container-fluid">
                      <ECol>
                         <EButton type="secondary" >+ Agregar rol </EButton>
                        <ECard style="background-color: #F8F9F9 " text>

                          <form
                            class="d-flex"
                            role="search">
                            <input
                                class="form-control me-2"
                                type="search"
                                placeholder="Buscar empleado"
                                aria-label="Search" />
                            <button
                                class="btn btn-outline-black"
                                type="submit">
                                Search
                            </button>
                          </form>
                          <h3 > Cajero </h3>
                          <h3 > Vendedor </h3>

                          </ECard>


                      </ECol>
                        <h1  style="
                        font-size: 35px;
                        color: black;
                        "> 
                        Cajero</h1>
                        
                        

                      <ECol>

                      </ECol>


                       

                        
                    </div>


                </nav>

               
            </div>

            
            <div
                class="container"
                style="background-color: white">
               
            </div>
        </div>
    </main>
</template>
