<script lang="ts">
    import { defineComponent } from 'vue'
    import type Item from '@/interfaz/items'
    import type { Status } from '@store/types'
    import ItemDataService from '@/store/item'
    import { useAuthStore } from '@store'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import ECard from '@components/custom/ECard.vue'
    import InputText from '@components/custom/InputText.vue'
    import { useRoute, useRouter } from 'vue-router'
    import { Field, ErrorMessage } from 'vee-validate'
    import { Form as EForm } from 'vee-validate'

    export default defineComponent({
        name: 'AddProductView',
        data() {
            const route = useRoute()
            const authStore = useAuthStore()
            const name = authStore.userData?.name
            const employee_id = authStore.userData?.employee as number
            const tiempoTranscurrido = Date.now()
            const hoy = new Date(tiempoTranscurrido)
            const normalValue = ref('')
            const productModalShow = ref(false)
            const productModalShowError = ref(false)
            const msm400 = ref('')
            const router = useRouter()
            const formStatus = ref<Status>({
                id: 0,
                name: 'active',
            })

            return {
                formStatus,
                route,
                router,
                hoy,
                normalValue,
                productModalShow,
                productModalShowError,
                msm400,
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
                    quantity: normalValue,
                    item_id: 0,
                    codigo: '',
                },
            }
        },
        components: {
            EForm,
            Field,
            ErrorMessage,
            ECard,
            ModalDialog,
            InputText,
        },
        methods: {
            async loadStatus(name: string) {
                this.formStatus = await ItemDataService.fetchStatus(name)
                this.entrada.status_id = this.formStatus.id
                console.log(this.entrada.status_id)
            },
            validarCheckbox() {
                const checkbox = document.getElementById(
                    'check'
                ) as HTMLInputElement
                if (!checkbox.checked) {
                    //this.entrada.status_id = 1
                    this.loadStatus('inactive')
                } else {
                    //this.entrada.status_id = 3
                    this.loadStatus('active')
                }
            },
            async showAllCategory() {
                ItemDataService.getAllCategory()
                    .then(response => {
                        this.category = response.data
                    })
                    .catch((e: Error) => {
                        console.log(e)
                    })
            },
            async showAllWarehouses() {
                ItemDataService.getAllWarehouses()
                    .then(response => {
                        this.warehouses = response.data
                    })
                    .catch((e: Error) => {
                        console.log(e)
                    })
            },
            obtenerImagen(e: any) {
                this.image_field = e.target.files[0]
                this.cargarImagen(this.image_field)
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
                formDataItem.append(
                    'status_id',
                    this.entrada.status_id.toString()
                )
                formDataItem.append('codename', this.entrada.codigo)
                return formDataItem
            },
            performUploadInventory(id: number) {
                const formDataInventory = new FormData()

                formDataInventory.append('created_at', this.hoy.toISOString())
                formDataInventory.append('updated_at', this.hoy.toISOString())
                formDataInventory.append('deleted_at', this.hoy.toISOString())

                formDataInventory.append(
                    'quantity',

                    this.normalValue
                )
                console.log(this.normalValue)
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
            emitValue(e: Event) {
                this.normalValue = (e.target as HTMLInputElement).value
                console.log(this.normalValue)
            },
            async guardarDatos(formDataItem: FormData) {
                ItemDataService.createItem(formDataItem)
                    .then(response => {
                        const ite = response.data
                        this.entrada.item_id = ite.id
                        ItemDataService.createInventory(
                            this.performUploadInventory(ite.id)
                        ).then(response => {
                            this.$router.push({ path: '/inventario' })
                        })
                    })
                    .catch(error => {
                        if (error.response.status == 400) {
                            this.productModalShowError = true
                            this.msm400 = JSON.stringify(error.response.data)
                        }
                    })
            },
            cargarImagen(file: any) {
                const reader = new FileReader()
                reader.onload = (e: any) => {
                    this.imagenM = e.target.result
                }
                reader.readAsDataURL(file)
            },
            onSubmit(value: any) {
                console.log('probando')
                this.productModalShow = true
            },
            validateCode(value: any) {
                if (!value) {
                    return 'Este campo es requerido'
                }
                if (isNaN(value)) {
                    return 'Inválido'
                }

                return true
            },
            validateName(value: any) {
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
            },
            validateMarca(value: any) {
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
            },

            validateModelo(value: any) {
                // if the field is empty
                if (!value) {
                    return 'Este campo es requerido'
                }

                return true
            },
            validateCategoria(value: any) {
                // if the field is empty
                if (!value) {
                    return 'Este campo es requerido'
                }

                return true
            },
            validatePrecio(value: any) {
                // if the field is empty
                if (!value) {
                    return 'Este campo es requerido'
                }
                if (isNaN(value)) {
                    return 'Inválido'
                }
                if (value < 0) {
                    return 'Inválido'
                }

                return true
            },

            validateIva(value: any) {
                // if the field is empty
                if (isNaN(value)) {
                    return 'Inválido'
                }
                if (value < 0) {
                    return 'Inválido'
                }
                if (value == 0 || value == 12) {
                    return true
                } else {
                    return 'Inválido'
                }

                return true
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
            this.loadStatus(this.formStatus.name.toString())
            //console.log("hola"+this.formStatus.value.name)
        },
    })
</script>

<template>
    <main>
        <ModalDialog
            id="product-modal-error"
            v-model:show="productModalShowError"
            title="Información">
            <h1 style="font-size: 15px; color: black; text-align: left">{{ msm400 }}</h1>
        </ModalDialog>
        <ModalDialog
            id="product-modal"
            v-model:show="productModalShow"
            title="Agregar Producto"
            ok-text="Guardar"
            @ok="guardarDatos(performUpload())"
            button-type="ok-cancel">
            <h1 style="font-size: 15px; color: black; text-align: left">¿Esta seguro de guardar el producto?</h1>
        </ModalDialog>

        <ECard>
            <EForm @submit="onSubmit">
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
                                        <Field
                                            name="code"
                                            type="text"
                                            class="form-control"
                                            :rules="validateCode"
                                            v-model="entrada.codigo" />
                                        <div class="col">
                                            <ErrorMessage
                                                name="code"
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
                                            Nombre *
                                        </h6>
                                        <Field
                                            name="name"
                                            type="text"
                                            class="form-control"
                                            :rules="validateName"
                                            v-model="entrada.name" />
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
                                            Marca *
                                        </h6>
                                        <Field
                                            name="marca"
                                            type="text"
                                            class="form-control"
                                            :rules="validateMarca"
                                            v-model="entrada.brand" />
                                        <div class="col">
                                            <ErrorMessage
                                                name="marca"
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
                                            Modelo*
                                        </h6>
                                        <Field
                                            name="modelo"
                                            type="text"
                                            class="form-control"
                                            placeholder=""
                                            aria-label="First name"
                                            :rules="validateModelo"
                                            v-model="entrada.model" />
                                        <div class="col">
                                            <ErrorMessage
                                                name="marca"
                                                style="
                                                    font-size: 10px;
                                                    color: red;
                                                    text-align: left;
                                                " />
                                        </div>
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
                                        :value="catego['id']"
                                        :key="catego['id']">
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
                                    Precio*
                                </h6>
                                <Field
                                    name="precio"
                                    type="text"
                                    class="form-control"
                                    :rules="validatePrecio"
                                    v-model="entrada.price" />
                                <div class="col">
                                    <ErrorMessage
                                        name="precio"
                                        style="
                                            font-size: 10px;
                                            color: red;
                                            text-align: left;
                                        " />
                                </div>
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
                                    Iva*
                                </h6>
                                <Field
                                    name="iva"
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    aria-label="First name"
                                    :rules="validateIva"
                                    v-model="entrada.iva" />
                                <div class="col">
                                    <ErrorMessage
                                        name="iva"
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
                                        type="checkbox"
                                        role="switch"
                                        id="check"
                                        @change="validarCheckbox()"
                                        checked />
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
                                                :value="warehouse['id']"
                                                :key="warehouse['id']">
                                                {{ warehouse['name'] }}
                                            </option>
                                        </select>
                                    </div>

                                    <div class="col">
                                        <InputText
                                            label="Cantidad del Producto"
                                            type="number"
                                            @input="emitValue" />
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

                    <!--Espacio demas-->
                </div>
            </EForm>
        </ECard>
    </main>
</template>