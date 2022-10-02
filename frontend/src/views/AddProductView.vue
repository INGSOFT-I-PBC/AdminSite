<script lang="ts">
    import { defineComponent } from 'vue'
    import type Item from '@/interfaz/items'
    import type Item3 from '@/interfaz/Items3'
    import ItemDataService from '@/store/item'

    import axios from 'axios'

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
                image_field: null,
                data: {
                    created_at: '2022-09-14T04:31:55Z',
                    updated_at: '2022-09-14T04:31:55Z',
                    deleted_at: null,
                    brand: 'marca',
                    category_id: 1,
                    created_by_id: 1,
                    img: this.image_field,
                    iva: '0.13',
                    model: 'modelo',
                    name: 'blusa',
                    price: '20.000',
                    status_id: 1,
                },
            }
        },
        methods: {
            obtenerImagen(e: any) {
                let file = e.target.files[0]
                console.log(file)
                this.cargarImagen(file)

                this.image_field = file
                this.performUpload(this.image_field)
                //this.items["0"].img=file
            },

            performUpload(image_field: any) {
                let formData = new FormData()
                formData.append('created_at', '2022-09-14T04:31:55Z')
                formData.append('updated_at', '2022-09-14T04:31:55Z')
                //formData.append('updated_at', '2022-09-14T04:31:55Z')
                formData.append('brand', 'brand')
                formData.append('img', image_field)
                formData.append('iva', '0.10')
                formData.append('model', 'model')
                formData.append('name', 'name')
                formData.append('price', '90.00')
                formData.append('category_id', '1')
                formData.append('created_by', '1')
                formData.append('status_id', '1')
                //this.image_field = formData

                return ItemDataService.createItem(formData)
            },
            cargarImagen(file: any) {
                let reader = new FileReader()
                reader.onload = (e: any) => {
                    this.imagenM = e.target.result
                    //console.log(this.imagenM)
                }
                reader.readAsDataURL(file)
            },
        },
        computed: {
            imagen() {
                return this.imagenM
            },
        },
        mounted() {},
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
    import { computed, reactive } from 'vue'

    import { useRoute, useRouter } from 'vue-router'
    const router = useRouter()

    function go2(): void {
        router.push({ path: '/inventario' })
    }
</script>

<template>
    <main>
        <ECard>
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
                                        Código *
                                    </h6>
                                    <input
                                        type="text"
                                        class="form-control"
                                        placeholder="23/08/2022"
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
                                        placeholder="15:00"
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
                                placeholder="Admin"
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
