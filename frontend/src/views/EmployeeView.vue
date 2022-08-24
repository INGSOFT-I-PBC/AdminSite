<script setup lang="ts">
    import EButton from '@components/custom/EButton.vue'
    import ERow from '@components/custom/ERow.vue'
    import InputText from '@components/custom/InputText.vue'

    import {
        useRoute,
        useRouter,
    } from 'vue-router'
    const router = useRouter()

    function go():void {
        router.push({ path: '/empleado/agregar' })
    }

    function rol():void {
        router.push({ path: '/role' })
    }

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
                    Empleados
                </h1>

                <nav class="navbar">
                    <div class="container-fluid">
                        <EButton type="secondary" @click="go" >+ Agregar empleado </EButton>

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

                        <EButton @click="rol">Roles</EButton>
                    </div>


                </nav>

               
            </div>

            <!--TABLA DE EMPLEADOS-->
            <div
                class="container"
                style="background-color: white">
                <table
                    class="table table-bordered">
                    <thead class="table-dark">
                        <tr>
                            <th scope="col">
                                Fecha de creación
                            </th>
                            <th scope="col">
                                Hora de creación
                            </th>
                            <th scope="col">
                                Creado por
                                
                            </th>
                            <th scope="col">
                                Identificación
                            </th>
                            <th scope="col">
                                Nombres y apellidos
                            </th>
                            <th scope="col">
                               Estado
                            </th>
                            <th scope="col">
                                Acciones
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>20/08/2022</th>
                            <td>15:00</td>
                            <td>Admin</td>
                            <td>0945674839 </td>
                            <td>Dennisse Aguirre</td>
                            <td>Icono</td>
                            <td>Icono</td>
                        </tr>
                        <tr>
                             <th>20/08/2022</th>
                            <td>15:00</td>
                            <td>Admin</td>
                            <td>0945674839 </td>
                            <td>Pamela Rugel</td>
                            <td>Icono</td>
                            <td>Icono</td>
                        </tr>
                        <tr>
                            <th>20/08/2022</th>
                            <td>15:00</td>
                            <td>Admin</td>
                            <td>0945674839 </td>
                            <td>Alejandra Quimi</td>
                            <td>Icono</td>
                            <td>Icono</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
</template>
