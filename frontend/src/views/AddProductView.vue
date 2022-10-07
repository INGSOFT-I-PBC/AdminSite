<script lang="ts">
    import { defineComponent } from 'vue'
    import type Item from '@/interfaz/items'
    import type Item3 from '@/interfaz/Items3'
    import ItemDataService from '@/store/item'
    import { useAuthStore } from '@store'

    import axios from 'axios'
    import { employee } from '@/router/routes/employee'

    export default defineComponent({
        name: 'AddProductView',
        data() {
            const route = useRoute()
            const authStore = useAuthStore()
            const name = authStore.userData?.name
            const employee_id = authStore.userData?.employee as number
            const tiempoTranscurrido = Date.now()
            const hoy = new Date(tiempoTranscurrido)

            return {
                route,
                hoy,
                items: {} as Item,
                fecha_hora: {
                    fecha: String,
                    hora: String,
                },
                imagenM: '',
                image_field: '',
                category: [],
                warehouses: [],
                authStore,
                name,
                employee_id,
                entrada: {
                    brand: '',
                    category_id: 0,
                    iva: 0,
                    model: '',
                    name: '',
                    price: 0,
                    status_id: 0,
                    warehouse_id: 0,
                    quantity: 0,
                    item_id: 0,
                },
            }
        },
        methods: {
            validarCheckbox() {
                const checkbox = document.getElementById('check') as HTMLInputElement
                console.log(checkbox.checked)
                if (checkbox.checked) {
                    this.entrada.status_id = 1
                } else {
                    this.entrada.status_id = 3
                }
            },
            async showAllCategory() {
                ItemDataService.getAllCategory()
                    .then(response => {
                        this.category = response.data
                        console.log(this.category)
                        console.log(this.authStore.userData?.employee)
                    })
                    .catch((e: Error) => {
                        console.log(e)
                    })
            },
            async showAllWarehouses() {
                ItemDataService.getAllWarehouses()
                    .then(response => {
                        this.warehouses = response.data
                        console.log(this.warehouses)
                    })
                    .catch((e: Error) => {
                        console.log(e)
                    })
            },
            obtenerImagen(e: any) {
                const file = e.target.files[0]
                console.log(file)
                this.cargarImagen(file)

                this.image_field = file
                //this.performUpload(this.image_field)
            },

            performUpload() {
                const formDataItem = new FormData()
                formDataItem.append('id', '')
                formDataItem.append('created_at', this.hoy.toISOString())
                formDataItem.append('updated_at', this.hoy.toISOString())
                formDataItem.append('brand', this.entrada.brand)
                formDataItem.append('img', this.image_field)
                formDataItem.append('iva', this.entrada.iva.toString())
                formDataItem.append('model', this.entrada.model)
                formDataItem.append('name', this.entrada.name)
                formDataItem.append('price', this.entrada.price.toString())
                formDataItem.append(
                    'category_id',
                    this.entrada.category_id.toString()
                )
                formDataItem.append('created_by', this.employee_id.toString())
                this.validarCheckbox()
                formDataItem.append('status_id', this.entrada.status_id.toString())
                return formDataItem
            },
            performUploadInventory(id: number) {
                const formDataInventory = new FormData()

                formDataInventory.append('created_at', this.hoy.toISOString())
                formDataInventory.append('updated_at', this.hoy.toISOString())
                formDataInventory.append('deleted_at', this.hoy.toISOString())

                formDataInventory.append(
                    'quantity',

                    this.entrada.quantity.toString()
                )
                formDataInventory.append('item_id', id.toString())
                formDataInventory.append(
                    'updated_by_id',
                    this.employee_id.toString()
                )
                formDataInventory.append(
                    'warehouse_id',
                    this.entrada.warehouse_id.toString()
                )

                return formDataInventory
            },
            async guardarDatos(formDataItem: FormData) {
                //console.log(formDataInventory.getAll('warehouse_id'))
                //console.log(formDataInventory)
                ItemDataService.createItem(formDataItem)
                    .then(response => {
                        const ite = response.data

                        this.entrada.item_id = ite.id
                        const formData = this.performUploadInventory(ite.id)
                        console.log(formData.getAll('quantity'))

                        ItemDataService.createInventory(formData).then(response => {
                            console.log(response.data)
                        })
                    })
                    .catch((e: Error) => {
                        console.log(e)
                    })

                // console.log(item.data)
                //ItemDataService.createInventory(formDataInventory)
            },
            cargarImagen(file: any) {
                const reader = new FileReader()
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
        mounted() {
            this.showAllCategory()
            this.showAllWarehouses()

            console.log(this.name)
            console.log(this.employee_id)
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
                                        aria-label="First name"
                                        v-model="entrada.name" />
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
                                        aria-label="First name"
                                        v-model="entrada.brand" />
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
                                        placeholder=""
                                        aria-label="First name"
                                        v-model="entrada.model" />
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
                                v-model="entrada.category_id"
                                class="form-select"
                                aria-label="Default select example">
                                <option
                                    v-for="catego in category"
                                    :value="catego['id']">
                                    {{ catego['name'] }}
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
                                aria-label="First name"
                                v-model="entrada.price" />
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
                                aria-label="First name"
                                v-model="entrada.iva" />
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
                                    id="check"
                                    @change="validarCheckbox()" />
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
                                aria-label="First name"
                                v-model="name" />
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
                                    <select
                                        v-model="entrada.warehouse_id"
                                        class="form-select"
                                        aria-label="Default select example">
                                        <option
                                            v-for="warehouse in warehouses"
                                            :value="warehouse['id']">
                                            {{ warehouse['name'] }}
                                        </option>
                                    </select>
                                </div>

                                <div class="col">
                                    <InputText
                                        label="Cantidad del Producto"
                                        type="number"
                                        :v-model="entrada.quantity" />
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
                        <EButton
                            type="secondary"
                            @click="guardarDatos(performUpload())"
                            >Guardar
                        </EButton>
                    </div>
                </div>

                <!--Espacio demas-->
                <div class="container text-center" style="padding: 10px"></div>
            </div>
        </ECard>
    </main>
</template>
