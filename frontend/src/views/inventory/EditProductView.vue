<script lang="ts">
    import type Item from '@/interfaz/items'
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import InputText from '@components/custom/InputText.vue'
    import ModalDialog from '@components/custom/ModalDialog.vue'
    import { useAuthStore } from '@store'
    import ItemDataService from '@store/item'
    import type { Status } from '@store/types'

    import { defineComponent } from 'vue'
    import { useRoute, useRouter } from 'vue-router'

    export default defineComponent({
        name: 'EditProductView',
        data() {
            const authStore = useAuthStore()
            const route = useRoute()
            const normalValue = ref('')
            const tiempoTranscurrido = Date.now()
            const hoy = new Date(tiempoTranscurrido)
            const productModalShow = ref(false)
            const productModalShowError = ref(false)
            const msm400 = ref('')
            const router = useRouter()
            const employee_id = authStore.userData?.employee as number
            const formStatus = ref<Status>({
                id: 0,
                name: 'active',
            })
            const checked = ref(false)

            return {
                checked,
                formStatus,
                route,
                normalValue,
                employee_id,
                productModalShow,
                productModalShowError,
                msm400,
                router,
                items: {} as Item,
                hoy,
                fecha_hora: {
                    fecha: '',
                    hora: '',
                },
                imagenM: '',

                image_field: '',
                category: [],
                warehouses: [],
                entrada: {
                    created_at: '',
                    updated_at: '',
                    brand: '',
                    category_id: 0,
                    iva: 12,
                    model: '',
                    name: '',
                    price: 0,

                    warehouse_id: 0,
                    quantity: normalValue,
                    item_id: 0,
                    codigo: '',
                    created_by: '',
                    created_id: 0,
                    is_active: true,
                },
            }
        },
        methods: {
            showProduct() {
                this.productModalShow = true
            },

            validarCheckbox() {
                this.entrada.is_active = !this.entrada.is_active
                console.log(this.entrada.is_active)
            },
            performUpload() {
                const formDataItem = new FormData()
                console.log(typeof this.image_field)
                formDataItem.append('created_at', this.entrada.created_at)
                formDataItem.append('updated_at', this.entrada.updated_at)
                formDataItem.append('brand', this.entrada.brand)
                if (typeof this.image_field != 'string') {
                    formDataItem.append('img', this.image_field)
                }
                if (this.checked) {
                    console.log('no entiendo')
                    console.log(this.checked)
                    this.entrada.iva = 0
                } else {
                    this.entrada.iva = 12
                }
                formDataItem.append('iva', (this.entrada.iva / 100).toString())
                formDataItem.append('model', this.entrada.model)
                formDataItem.append('name', this.entrada.name)
                formDataItem.append('price', this.entrada.price.toString())
                formDataItem.append(
                    'category_id',
                    this.entrada.category_id.toString()
                )
                formDataItem.append(
                    'created_by',
                    this.entrada.created_id.toString()
                )
                console.log(this.entrada.created_id)

                this.validarCheckbox()
                formDataItem.append(
                    'is_active',
                    this.entrada.is_active.toString()
                )
                formDataItem.append('codename', this.entrada.codigo)
                return formDataItem
            },
            performUploadInventory() {
                const formDataInventory = new FormData()

                formDataInventory.append('created_at', this.entrada.created_at)
                formDataInventory.append('updated_at', this.entrada.updated_at)

                formDataInventory.append(
                    'quantity',

                    this.normalValue
                )
                formDataInventory.append(
                    'item_id',
                    this.entrada.item_id.toString()
                )
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
            },
            async guardarDatos(formDataItem: FormData) {
                /*ItemDataService.updateItem(this.entrada.item_id, formDataItem)
                        .then(response=>{
                            this.$router.push({ path: '/inventario' })

                        })  .catch((error) => {

                                if (error.response.status==400){
                                    this.productModalShowError = true
                                    this.msm400=JSON.stringify(error.response.data)
                                }
                                })*/

                ItemDataService.updateInventory(
                    Number(this.route.params.id),
                    this.performUploadInventory()
                )
                    .then(response => {
                        const ite = response.data

                        ItemDataService.updateItem(
                            this.entrada.item_id,
                            formDataItem
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
            async showAllProducts(id: string) {
                ItemDataService.get(String(id))
                    .then(response => {
                        this.items = response.data
                        console.log(this.items)
                        this.entrada.category_id =
                            this.items['0'].category_id_Item
                        this.imagenM =
                            //'https://proyectoadmin.pythonanywhere.com/'
                            //http://127.0.0.1:8000
                            'https://proyectoadmin.pythonanywhere.com/storage/' +
                            this.items['0'].imgItem
                        console.log(this.imagenM)
                        this.entrada.warehouse_id = this.items['0'].warehouse_id
                        this.entrada.created_by =
                            this.items['0'].created_by_Item.name +
                            ' ' +
                            this.items['0'].created_by_Item.lastname
                        this.entrada.created_at = this.items['0'].created_at
                        this.entrada.updated_at = this.hoy.toISOString()
                        this.entrada.created_id =
                            this.items['0'].created_by_Item.created_by
                        console.log('hh' + this.entrada.created_id)
                        this.entrada.item_id = this.items['0'].item_id
                        this.entrada.codigo = this.items['0'].codename_Item
                        this.entrada.brand = this.items['0'].brandItem
                        this.entrada.price = this.items['0'].priceItem
                        this.entrada.model = this.items['0'].modelItem
                        this.entrada.iva = this.items['0'].ivaItem
                        if (this.items['0'].ivaItem == 0) {
                            this.checked = true
                        }
                        this.entrada.quantity = this.items['0'].quantity

                        this.entrada.name = this.items['0'].nombreItem
                        this.entrada.is_active = this.items['0'].is_active

                        this.fecha_hora.fecha = new Date(
                            this.items['0'].created_at
                        ).toLocaleDateString()
                        this.fecha_hora.hora = new Date(
                            this.items['0'].created_at
                        ).toLocaleTimeString()

                        console.log(this.items['0'])
                    })
                    .catch((e: Error) => {
                        console.log(e)
                    })
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
            obtenerImagen(e: any) {
                this.image_field = e.target.files[0]
                console.log(this.image_field)
                console.log(typeof this.image_field)
                this.cargarImagen(this.image_field)
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
            this.showAllCategory()
            this.showAllWarehouses()
        },
        components: {
            ECard,
            ModalDialog,
            InputText,
            EButton,
        },
    })
</script>

<template>
    <main>
        <ModalDialog
            id="product-modal-error"
            v-model:show="productModalShowError"
            title="Información">
            <h1 style="font-size: 15px; color: black; text-align: left">
                {{ msm400 }}
            </h1>
        </ModalDialog>
        <ModalDialog
            id="product-modal"
            v-model:show="productModalShow"
            title="Modificar Producto"
            ok-text="Guardar"
            @ok="guardarDatos(performUpload())"
            button-type="ok-cancel">
            <h1 style="font-size: 15px; color: black; text-align: left">
                ¿Está seguro de modificar el producto?
            </h1>
        </ModalDialog>
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
                                        Codigo *
                                    </h6>
                                    <input
                                        type="text"
                                        class="form-control"
                                        v-model="entrada.codigo"
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
                                        v-model="entrada.name"
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
                                        v-model="entrada.brand"
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
                                        v-model="entrada.model"
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
                            <input
                                type="text"
                                class="form-control"
                                placeholder=""
                                v-model="entrada.price"
                                aria-label="First name" />
                        </div>
                    </div>
                </div>

                <!--BOTONES Usuario-->
                <div class="container text-center" style="padding: 10px">
                    <div class="row">
                        <div class="col">
                            <InputText label="IVA" model-value="12" />
                        </div>
                        <div class="col" style="display: flex">
                            <input
                                type="checkbox"
                                id="checkbox"
                                v-model="checked" />
                            <label
                                style="
                                    align-self: center;
                                    font-weight: 700;
                                    font-size: 1rem;
                                "
                                for="checkbox"
                                >IVA 0</label
                            >
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
                                    :checked="entrada.is_active" />
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
                                v-model="entrada.created_by"
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
                                        v-model="entrada.quantity"
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

                <div class="container text-center" style="padding: 10px">
                    <div class="row">
                        <EButton variant="secondary" @click="showProduct()"
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
