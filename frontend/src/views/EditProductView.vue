<script lang="ts">
    import { defineComponent } from 'vue'
    import { stringifyQuery, useRoute, useRouter } from 'vue-router'
    import type Item from '@/interfaz/items'
    import type Item3 from '@/interfaz/Items3'

    export default defineComponent({
        name: 'EditProductView',
        data() {
            const route = useRoute()

            return {
                route,
                items: {} as Item,
                fecha_hora: {
                    fecha: String,
                    hora: String,
                },
                imagenM: '',
            }
        },
        methods: {
            async showAllProducts(id: string) {
                ItemDataService.get(String(id))
                    .then(response => {
                        this.items = response.data
                        console.log(this.items)
                        this.fecha_hora.fecha = this.items['0'].created_at.substring(
                            0,
                            10
                        )
                        this.fecha_hora.hora = this.items['0'].created_at.substring(
                            11,
                            16
                        )
                        console.log(this.items['0'])
                    })
                    .catch((e: Error) => {
                        console.log(e)
                    })
            },
            obtenerImagen(e: any) {
                const file = e.target.files[0]
                console.log(file)
                this.cargarImagen(file)
                //this.items["0"].img=file
            },
            cargarImagen(file: any) {
                const reader = new FileReader()
                reader.onload = (e: any) => {
                    this.imagenM = e.target.result
                }
                reader.readAsDataURL(file)
            },
        },
        computed: {
            imagen() {
                return this.imagenM
            },
        },
        mounted() {
            if (typeof this.route.params.id === 'string')
                this.showAllProducts(String(this.route.params.id))
        },
    })
</script>

<script setup lang="ts">
    import ECard from '@components/custom/ECard.vue'
    import ERow from '@components/custom/ERow.vue'
    import ECol from '@components/custom/ECol.vue'
    import ListBox from '@components/custom/ListBox.vue'
    import InputText from '@components/custom/InputText.vue'
    import EButton from '@components/custom/EButton.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import Title from '@components/custom/Title.vue'
    import Table from '@components/holders/Table.vue'
    import { computed, reactive, onMounted, onBeforeMount } from 'vue'
    import ItemDataService from '@/store/item'

    const router = useRouter()

    function go2(): void {
        router.push({ path: '/inventario' })
    }
</script>

<template>
    <main>
        <ECard v-for="item in items" :key="item.id">
            <div class="container" style="border-radius: 5px">
                <!--BOTONES Usuario-->
                <div class="container text-center" style="padding: 10px">
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
                                        Codigo *
                                    </h6>
                                    <input
                                        type="text"
                                        class="form-control"
                                        v-model="item.id"
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
                                        Nombre *
                                    </h6>
                                    <input
                                        type="text"
                                        class="form-control"
                                        v-model="item.name"
                                        aria-label="First name" />
                                </div>

                                <div class="col">
                                    <h6
                                        style="
                                            font-size: 15px;
                                            color: black;
                                            text-align: left;
                                        ">
                                        Marca *
                                    </h6>
                                    <input
                                        type="text"
                                        class="form-control"
                                        placeholder="Admin"
                                        v-model="item.brand"
                                        aria-label="First name" />
                                </div>

                                <div class="col">
                                    <h6
                                        style="
                                            font-size: 15px;
                                            color: black;
                                            text-align: left;
                                        ">
                                        Modelo
                                    </h6>
                                    <input
                                        type="text"
                                        class="form-control"
                                        placeholder="Admin"
                                        v-model="item.model"
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
                            <h6
                                style="
                                    font-size: 15px;
                                    color: black;
                                    text-align: left;
                                ">
                                Categoría*
                            </h6>
                            <select
                                class="form-select"
                                aria-label="Default select example">
                                <option selected>Femenino</option>
                                <option value="1">Masculino</option>
                                <option value="2">Unisex</option>
                            </select>
                        </div>

                        <div class="col">
                            <h6
                                style="
                                    font-size: 15px;
                                    color: black;
                                    text-align: left;
                                ">
                                Descripción *
                            </h6>
                            <input
                                type="text"
                                class="form-control"
                                placeholder=""
                                v-model="item.model"
                                aria-label="First name" />
                        </div>

                        <div class="col">
                            <h6
                                style="
                                    font-size: 15px;
                                    color: black;
                                    text-align: left;
                                ">
                                Precio*
                            </h6>
                            <input
                                type="text"
                                class="form-control"
                                placeholder=""
                                v-model="item.price"
                                aria-label="First name" />
                        </div>
                        <div class="col">
                            <h6
                                style="
                                    font-size: 15px;
                                    color: black;
                                    text-align: left;
                                ">
                                Peso
                            </h6>
                            <input
                                type="text"
                                class="form-control"
                                placeholder=""
                                aria-label="First name" />
                        </div>
                    </div>
                </div>

                <!--BOTONES Usuario-->
                <div class="container text-center" style="padding: 10px">
                    <div class="row">
                        <div class="col">
                            <h6
                                style="
                                    font-size: 15px;
                                    color: black;
                                    text-align: left;
                                ">
                                Tipo*
                            </h6>
                            <input
                                type="text"
                                class="form-control"
                                placeholder=""
                                aria-label="First name" />
                        </div>

                        <div class="col">
                            <h6
                                style="
                                    font-size: 15px;
                                    color: black;
                                    text-align: left;
                                ">
                                Iva*
                            </h6>
                            <input
                                type="text"
                                class="form-control"
                                placeholder=""
                                v-model="item.iva"
                                aria-label="First name" />
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
                                    v-if="item.status_id === 1"
                                    class="form-check-input"
                                    type="checkbox"
                                    role="switch"
                                    id="flexSwitchCheckDefault"
                                    checked />
                                <input
                                    v-else
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
                </div>

                <!--DIV DE BOTONES Y NAV-->
                <div class="container text-center">
                    <div class="row">
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
                                v-model="fecha_hora.fecha"
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
                                v-model="fecha_hora.hora"
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
                                placeholder="Admin"
                                v-model="item.created_by"
                                disabled="false"
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
                                        Elegir Bodega
                                    </h6>
                                    <input type="checkbox" id="jack" value="Jack" />
                                    <label for="jack"> Bodega 1 </label>
                                    <input type="checkbox" id="john" value="John" />
                                    <label for="john"> Bodega 2 </label>
                                    <input type="checkbox" id="mike" value="Mike" />
                                    <label for="mike"> Bodega 3 </label>
                                </div>

                                <div class="col">
                                    <InputText
                                        label="Cantidad del Producto"
                                        type="number" />
                                </div>

                                <div class="col">
                                    <h6
                                        style="
                                            font-size: 15px;
                                            color: black;
                                            text-align: left;
                                        ">
                                        Descuento
                                    </h6>
                                    <input
                                        type="text"
                                        class="form-control"
                                        aria-label="First name" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="container text-left col">
                    <form enctype="multipart/form-data">
                        <div class="col form-group">
                            <div class="row">
                                <label for="imagen">Imagen</label>
                            </div>
                            <input
                                type="file"
                                ref="file"
                                @change="obtenerImagen"
                                class="form-control-file" />

                            <figure>
                                <img
                                    width="200"
                                    height="200"
                                    :src="imagen"
                                    alt="Foto del producto"
                                    v-if="imagenM" />
                            </figure>
                        </div>
                    </form>
                </div>

                <div class="container text-center" style="padding: 10px">
                    <div class="row">
                        <EButton type="secondary" @click="go2">Guardar </EButton>
                    </div>
                </div>

                <!--Espacio demas-->
                <div class="container text-center" style="padding: 10px"></div>
            </div>
        </ECard>
    </main>
</template>
