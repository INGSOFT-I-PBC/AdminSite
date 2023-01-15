<script setup lang="ts">
    import { useItemStore } from '@/store'
    import { usePurchaseStore } from '@store/purchase'
    import {
        type FullTomaFisicaDetail,
        type MessageResponse,
        type Movement,
        type PaginatedResponse,
        type ProductProps,
        type ProductVariant,
        type Purchase,
        type SimpleProduct,
        type TomaFisica,
        type Warehouse,
        type WarehouseStock,
        type WhWithTomaFisica,
        isMessage,
    } from '@store/types'
    import { useWarehouseStore } from '@store/warehouse'
    import Datepicker from '@vuepic/vue-datepicker'
    import {
        BBadge,
        BForm,
        BFormCheckbox,
        BFormInput,
        BListGroup,
        BListGroupItem,
        BPagination,
        BTab,
        BTable,
        BTabs,
        type ColorVariant,
        type TableField,
    } from 'bootstrap-vue-3'
    import { Form as ValidationForm, useField } from 'vee-validate'
    import * as yup from 'yup'

    import { computed, ref, watch } from 'vue'
    import { useRouter } from 'vue-router'
    import { useToast } from 'vue-toastification'

    import {
        EButton,
        ECard,
        InputText,
        LoadingBar,
        ModalDialog,
        WaitOverlay,
    } from '@custom-components'

    const router = useRouter()

    /**
     * Contains the current status name stored in the database that correspons to a delivered purchase
     */
    const DELIVERED_PURCHASE_STATUS = ref('entregado')

    type SelectedItem = {
        product: SimpleProduct | null
        variant: ProductVariant | null
        props: ProductProps[]
    }

    type whCardController = {
        currentPage: number
        totalRows: number
    }

    type warehouseInformation = {
        bodega: Warehouse
        inventory: WarehouseStock[]
        purchases: Purchase[]
        tomasFisicas: TomaFisica[]
        movements: Movement[]
    }

    const toast = useToast()
    /**
     * Flag to hide or show the waiting overlay
     */
    const showWaitOverlay = ref(true)
    /**
     * Flag to hide or show the purchase modal
     */
    const purchaseModalShow = ref(false)

    /**
     * References the warehouseStore
     */
    const warehouse = useWarehouseStore()
    /**
     * References the purchaseStore
     */
    const purchase = usePurchaseStore()
    /**
     * References the itemStore
     */
    const itemStore = useItemStore()

    /**
     * General value that contains the number of rows to be displayed
     */
    const whPageCount = ref(15)
    /**
     * Flag to display main page or the specific warehouse page with the tabs
     */
    const showAllWarehouses = ref<boolean>(true)
    /**
     * Flag to stop the watchers from executing
     */
    const stopWatcher = ref(true)
    /**
     * General value that contains the number of rows to be displayed on the specific warehouse tabs
     */
    const whInformationPerPage = ref(15)

    /**
     * Fields for the table displayed in the main page
     */
    const allWarehousesFields: TableField[] = [
        '#',
        { label: 'Nombre', key: 'name' },
        'FechaTomaFísica',
        'RealizadaPor',
        'Novedad',
        'Detalles',
    ]
    /**
     * Fields for the table displayed in the inventory tab
     */
    const inventoryFields: TableField[] = [
        '#',
        'Código',
        'Producto',
        'Variante',
        { label: 'Stock', key: 'stock_level' },
        'Marca',
        'PrecioVenta',
        'Acciones',
    ]
    /**
     * Fields for the table displayed in the purchase tab
     */
    const purchasesFields: TableField[] = [
        '#',
        'FechaAprobación',
        { label: 'Código Orden', key: 'reference' },
        'AprobadoPor',
        'RazonDeCompra',
        'Estado',
        'Entregado',
        'Acciones',
    ]
    /**
     * Fields for the table displayed in the tomas-fisicas tab
     */
    const tomasFisFields: TableField[] = [
        '#',
        'FechaRealizacion',
        'RealizadaPor',
        'Novedad',
        'Acciones',
    ]
    /**
     * Fields for the table displayed in the movement tab
     */
    const movementsFields: TableField[] = [
        '#',
        'Creada',
        'RealizadaPor',
        'BodegaRelacionada',
        'TipoDeMovimiento',
        { label: 'Estado', key: 'status' },
        'Notas',
    ]
    /**
     * Contains the information of the warehouse with the latest toma fisica for the main page
     */
    let allWarehousesTableInformation: WhWithTomaFisica[] = []
    /**
     * Page number to cnotrol the pagination of the aside
     */
    const currentAsidePage = ref(1)
    /**
     * Length of the total number of warehouses fetch
     */
    const whRows = ref(0)
    /**
     * Contains the information of the warehouses names for the aside
     */
    const paginatedWarehouse = ref()
    /**
     * Controller to know wich warehouse was pressed last
     */
    const activeWharehouseButton = ref(-1)
    /**
     * Contains the paginated information of the main table
     */
    const paginatedMainTable = ref<WhWithTomaFisica[]>([])

    /**
     * Controller for the main page
     * @property {number} currentPage Page number for the main table
     * @property {number} totalRows Total number of registries to fetch and display per page
     */
    const mainPageController = ref<whCardController>({
        currentPage: 1,
        totalRows: whRows.value,
    })
    /**
     * @type {warehouseInformation}
     * Contains the related information of the warehouse that was selected to display the information.
     */

    const activeWhInformation = ref<warehouseInformation>({
        bodega: {
            id: -1,
            name: 'Not Selected',
            status: { description: '', name: '', id: '' },
        },
        inventory: [],
        purchases: [],
        tomasFisicas: [],
        movements: [],
    })
    /**
     * Controller for the inventory tab
     * @property {number} currentPage Page number for the inventory tab table
     * @property {number} totalRows Total number of registries to fetch and display per page
     */
    const invTabController = ref<whCardController>({
        currentPage: 1,
        totalRows: 15,
    })
    /**Controller for the tomas-fisicas tab
     * @property {number} currentPage Page number for the tomas fisicas tab table
     * @property {number} totalRows Total number of registries to fetch and display per page
     */
    const tomasFisicasTabController = ref<whCardController>({
        currentPage: 1,
        totalRows: 15,
    })
    /**
     * Controller for the purchase tab
     * @property {number} currentPage Page number for the purchase tab table
     * @property {number} totalRows Total number of registries to fetch and display per page
     */
    const purchaseTabController = ref<whCardController>({
        currentPage: 1,
        totalRows: 15,
    })
    /**
     * Controller for the MovementTab
     * @property {number} currentPage Page number for the movement tab table
     * @property {number} totalRows Total number of registries to fetch and display per page
     */
    const movementTabController = ref<whCardController>({
        currentPage: 1,
        totalRows: 15,
    })
    /**
     * Array containing all the controllers for the tabs
     */
    const arrayControllers = [
        invTabController.value,
        tomasFisicasTabController.value,
        purchaseTabController.value,
        movementTabController.value,
    ]
    /**
     * Object that contains the validations for the inventoryForm. Uses yup
     * @property {FieldContext<any>} from_date Minimum date to query
     * @property {FieldContext<any>} from_date Maximum date to query
     * @property {FieldContext<any>} name String query to search product name
     * @property {FieldContext<any>} sku String query to search a sku code for the product
     * @property {FieldContext<any>} max_quantity Max stock_level to query
     * @property {FieldContext<any>} min_quantity Min stock_level to query
     * @property {FieldContext<any>} max_price Max product variant price to query
     * @property {FieldContext<any>} min_price Min product variant price to query
     *
     */
    const inventoryForm = ref({
        from_date: useField(
            'from_date',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr: any, orig: any) =>
                    orig === '' ? null : curr
                )
                .typeError('Fecha Invalida')
        ),
        to_date: useField(
            'to_date',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? null : curr
                )
                .typeError('Fecha Invalida')
        ),
        name: useField('name', yup.string().optional().nullable(true)),
        sku: useField('sku', yup.string().optional().nullable(true)),
        min_quantity: useField(
            'min_quantity',
            yup
                .number()
                .min(0, 'Tiene que ser mayor a 0')
                .optional()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? undefined : curr
                )
                .typeError('Ingrese un número entero')
        ),
        max_quantity: useField(
            'max_quantity',
            yup
                .number()
                .min(0, 'Tiene que ser mayor a 1')
                .optional()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? undefined : curr
                )
                .typeError('Ingrese un número entero')
        ),
        min_price: useField(
            'min_price',
            yup
                .number()
                .min(0, 'Tiene que ser mayor a 0')
                .optional()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? undefined : curr
                )
                .typeError('Ingrese un número')
        ),
        max_price: useField(
            'max_price',
            yup
                .number()
                .min(0, 'Tiene que ser mayor a 0')
                .optional()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? undefined : curr
                )
                .typeError('Ingrese un número')
        ),
    })
    /**
     * Manager computed variable to check minimum price is less thatn the maximum.
     * Contains the resulting error to be displayed
     */
    const price_message = ref<string>()
    const priceRangeError = (): void => {
        const f = inventoryForm.value
        if (f.max_price.value != '' && f.min_price.value != '') {
            if (Number(f.max_price.value) < Number(f.min_price.value)) {
                price_message.value =
                    'Precio máximo tiene que ser mayor que el mínimo'
                return
            }
        }

        price_message.value = f.max_price.errorMessage
    }

    /**
     * Manager computed variable to check minimum quantity is less thatn the maximum
     * Contains the resulting error to be displayed
     */
    const quantity_message = ref<string>()
    const quantityRangeError = (): void => {
        const f = inventoryForm.value
        if (f.max_quantity.value != '' && f.min_quantity.value != '') {
            if (Number(f.max_quantity.value) < Number(f.min_quantity.value)) {
                quantity_message.value =
                    'Cantidad máxima tiene que ser mayor que la mínima'
                return
            }
        }

        quantity_message.value = f.max_quantity.errorMessage
    }

    /**
     * Object that contains the validations for the purchase Form. Uses yup
     * @property {FieldContext<any>} from_date Minimum date to query
     * @property {FieldContext<any>} from_date Maximum date to query
     * @property {boolean} approved_date Flag: purchases approved in the range of the from_date and to_date range
     * @property {boolean} invoice_date Flag: invoice date registered in the range of the from_date and to_date range
     * @property {FieldContext<any>} done_by_name Name of the employee that created the movement for the query
     * @property {FieldContext<any>} provider_name A related warehouse name to query
     * @property {boolean} status Flag: search purchases that are confirmed delivered
     * @property {FieldContext<any>} invoice_code String query to match for the invoice code related to the pruchase
     * @property {FieldContext<any>} reference Number of the pruchase reference to query
     *
     */
    const purchaseForm = ref({
        from_date: useField(
            'to_date_p',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? null : curr
                )
                .typeError('Fecha Invalida')
        ),
        to_date: useField(
            'to_date_p',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? null : curr
                )
                .typeError('Fecha Invalida')
        ),
        approved_date: true,
        invoice_date: false,
        provider_name: useField(
            'provider_name',
            yup.string().optional().nullable(true)
        ),
        status: false,
        invoice_code: useField(
            'invoice_code',
            yup.string().optional().nullable(true)
        ),
        reference: useField(
            'reference',
            yup
                .number()
                .optional()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? undefined : curr
                )
                .typeError('Ingrese un número entero')
        ),
    })
    /**
     * Object that contains the validations for the tomasFisicasForm. Uses yup
     * @property {FieldContext<any>} from_date Minimum date to query
     * @property {FieldContext<any>} from_date Maximum date to query
     * @property {FieldContext<any>} done_by_name Name of the employee that created the movement for the query
     * @property {FieldContext<any>} novedad String query to match for the novedad field
     *
     */
    const tomasFisicasForm = ref({
        from_date: useField(
            'to_date_t',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? null : curr
                )
                .typeError('Fecha Invalida')
        ),
        to_date: useField(
            'to_date_t',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? null : curr
                )
                .typeError('Fecha Invalida')
        ),
        done_by_name: useField(
            'done_by_name',
            yup.string().optional().nullable(true)
        ),
        novedad: useField('novedad', yup.string().optional().nullable(true)),
    })
    /**
     * Object that contains the validations for the movementForm. Uses yup
     * @property {FieldContext<any>} from_date Minimum date to query
     * @property {FieldContext<any>} from_date Maximum date to query
     * @property {boolean} entrada To search movements that has the selected warehouse as destiny
     * @property {boolean} salida To search movements that has the selected warehouse as origin
     * @property {FieldContext<any>} done_by_name Name of the employee that created the movement for the query
     * @property {FieldContext<any>} warehouse_name A related warehouse name to query
     * @property {FieldContext<any>} status A status name to query
     * @property {FieldContext<any>} notes String query to match for the notes field
     *
     */
    const movementForm = ref({
        from_date: useField(
            'to_date_m',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr, orig) => (orig === '' ? null : curr))
                .typeError('Fecha Invalida')
        ),
        to_date: useField(
            'to_date_m',
            yup
                .date()
                .notRequired()
                .nullable()
                .transform((curr: any, orig: any): any =>
                    orig === '' ? null : curr
                )
                .typeError('Fecha Invalida')
        ),
        entrada: false,
        salida: false,
        done_by_name: useField(
            'done_by_name_m',
            yup.string().optional().nullable(true)
        ),
        warehouse_name: useField(
            'warehouse_name_m',
            yup.string().optional().nullable(true)
        ),
        status: useField('status_m', yup.string().optional().nullable(true)),
        notes: useField('notes_m', yup.string().optional().nullable(true)),
    })

    /**
     * Paginates the aside list that has the warehouse names
     * @param {number}page_size Size of the maximum
     * @param {number}page_number Maximum size of the table page
     */
    function paginateAside(page_size: number, page_number: number): void {
        paginatedWarehouse.value = (warehouse.getWarehouseList ?? []).slice(
            page_number * page_size,
            (page_number + 1) * page_size
        )
    }

    /**
     * Manager function to control the aside pagination
     * @param event Html event
     * @param {number}page New page number
     */
    function onAsidePageChanged(event: Event, page: number): void {
        paginateAside(whPageCount.value, page - 1)
    }

    /**
     * Slices the allWarehousesTableInformation that contains the warehouses for the main page.
     * Enables pagination
     * @param {number}page_size Maximum size for the table page
     * @param {number}page_number Number of the new page
     */
    function paginateMain(page_size: number, page_number: number): void {
        paginatedMainTable.value = allWarehousesTableInformation.slice(
            page_number * page_size,
            (page_number + 1) * page_size
        )
    }

    /**
     * Manager function to be called when a page is changed
     * @param event Html event
     * @param page New page to be switched to
     */
    function onMainPageChanged(event: Event, page: number): void {
        paginateMain(whPageCount.value, page - 1)
    }

    /**
     * Resets the information of a specific warehouse to clean the screen
     */
    function resetWhPage(): void {
        for (const controller of arrayControllers) {
            ;(controller.currentPage = 1), (controller.totalRows = 1)
        }
    }

    /**
     * General manager to fetch a warehouse information, used locally by other functions
     * @param {string}tabOption The option to know which endpoint to fetch ('inventory','purchase','tomas-fisicas','movements')
     * @param {Object}query Has the query parameters to be fetched
     * @param {PaginationOptions}paginated_opt Has the query options for the paginated response
     */

    async function fetchManager(
        tabOption: string,
        query: any,
        paginated_opt: PaginationOptions
    ): Promise<void> {
        switch (tabOption) {
            case 'inventory': {
                let res = await warehouse.fetchPaginatedWarehouseInventory(
                    query,
                    paginated_opt
                )
                if (isMessage(res)) {
                    toast.error(res.message)
                    return
                }
                res = res as PaginatedResponse<WarehouseStock>

                activeWhInformation.value.inventory = res.data
                invTabController.value.totalRows = res.total

                break
            }
            case 'purchases': {
                let res = await purchase.fetchPaginatedPurchases(
                    query,
                    paginated_opt
                )
                if (isMessage(res)) {
                    toast.error(res.message)
                    return
                }
                res = res as PaginatedResponse<Purchase>

                activeWhInformation.value.purchases = res.data
                purchaseTabController.value.totalRows = res.total
                break
            }
            case 'tomas-fisicas': {
                let res = await warehouse.fetchPaginatedWarehouseTomasFisicas(
                    query,
                    paginated_opt
                )

                if (isMessage(res)) {
                    toast.error(res.message)
                    return
                }
                res = res as PaginatedResponse<TomaFisica>

                activeWhInformation.value.tomasFisicas = res.data
                tomasFisicasTabController.value.totalRows = res.total
                break
            }
            case 'movements': {
                query.entrada = true
                query.salida = true
                let res = await warehouse.fetchPaginatedWarehouseMovements(
                    query,
                    paginated_opt
                )
                if (isMessage(res)) {
                    toast.error(res.message)
                    return
                }
                res = res as PaginatedResponse<Movement>

                activeWhInformation.value.movements = res.data
                movementTabController.value.totalRows = res.total
                break
            }
        }
    }

    /**
     * Manager for a search request. Mapped to the buttons on the forms of each tab.
     * Sends the FECTH request to the corresponding endpoint with the values in the search form
     * @param {string}tabOption The option to know which form to submit ('inventory','purchase','tomas-fisicas','movements')
     * @param {whCardController}controller whCardController that the information will be loaded to
     */
    async function onSubmit(
        tabOption: string,
        controller: whCardController
    ): Promise<void> {
        showWaitOverlay.value = true
        const query: Record<string, any> = {
            warehouse_id: activeWhInformation.value.bodega.id,
        }
        stopWatcher.value = true
        switch (tabOption) {
            case 'inventory': {
                const f = inventoryForm.value
                if (
                    f.name.errorMessage ||
                    f.sku.errorMessage ||
                    f.min_price.errorMessage ||
                    f.min_quantity.errorMessage ||
                    f.from_date.errorMessage ||
                    f.to_date.errorMessage ||
                    price_message.value ||
                    quantity_message.value
                ) {
                    toast.error('Verifique los datos antes buscar')
                    showWaitOverlay.value = false
                    return
                }
                query.name = f.name.value
                query.sku = f.sku.value
                query.max_price = f.max_price.value as number
                query.min_price = f.min_price.value as number
                query.max_quantity = f.max_quantity.value as number
                query.min_quantity = f.min_quantity.value as number
                query.from_date = f.from_date.value
                query.to_date = f.to_date.value
                fetchManager(tabOption, query, { per_page: 15, page: 1 })
                    .then((): void => {
                        if (activeWhInformation.value.inventory.length < 1) {
                            toast.error(
                                'No se ha encontrado registros en la búsqueda'
                            )
                        } else {
                            toast.success('Búsqueda exitosa')
                        }
                    })
                    .catch(err => {
                        if (isMessage(err)) {
                            toast.error(err.message)
                        } else {
                            toast.error('Error desconocido')
                        }
                    })
                    .finally((): void => {
                        controller.currentPage = 1
                        showWaitOverlay.value = false
                        stopWatcher.value = false
                    })
                break
            }
            case 'purchases': {
                const f = purchaseForm.value
                if (
                    f.from_date.errorMessage ||
                    f.to_date.errorMessage ||
                    f.provider_name.errorMessage ||
                    f.invoice_code.errorMessage ||
                    f.reference.errorMessage
                ) {
                    toast.error('Verifique los datos antes buscar')
                    showWaitOverlay.value = false
                    return
                } else if (!f.approved_date && !f.invoice_date) {
                    toast.error('Marque un tipo de búsqueda por fecha')
                    showWaitOverlay.value = false
                    return
                }
                query.from_date = f.from_date.value
                query.to_date = f.to_date.value
                query.approved_date = f.approved_date
                query.invoice_date = f.invoice_date
                query.provider_name = f.provider_name.value
                f.status
                    ? (query.status = DELIVERED_PURCHASE_STATUS.value)
                    : (query.invoice_code = f.invoice_code.value)
                query.reference = f.reference.value as number
                fetchManager(tabOption, query, { per_page: 15, page: 1 })
                    .then((): void => {
                        if (activeWhInformation.value.purchases.length < 1) {
                            toast.error(
                                'No se ha encontrado registros en la búsqueda'
                            )
                        } else {
                            toast.success('Búsqueda exitosa')
                        }
                    })
                    .catch(err => {
                        if (isMessage(err)) {
                            toast.error(err.message)
                        } else {
                            toast.error('Error desconocido')
                        }
                    })
                    .finally((): void => {
                        controller.currentPage = 1
                        showWaitOverlay.value = false
                        stopWatcher.value = false
                    })

                break
            }
            case 'tomas-fisicas': {
                const f = tomasFisicasForm.value
                if (
                    f.from_date.errorMessage ||
                    f.to_date.errorMessage ||
                    f.done_by_name.errorMessage ||
                    f.novedad.errorMessage
                ) {
                    toast.error('Verifique los datos antes buscar')
                    showWaitOverlay.value = false
                    return
                }
                query.from_date = f.from_date.value
                query.to_date = f.to_date.value
                query.done_by_name = f.done_by_name.value
                query.novedad = f.novedad.value

                fetchManager(tabOption, query, { per_page: 15, page: 1 })
                    .then((): void => {
                        if (activeWhInformation.value.tomasFisicas.length < 1) {
                            toast.error(
                                'No se ha encontrado registros en la búsqueda'
                            )
                        } else {
                            toast.success('Búsqueda exitosa')
                        }
                    })
                    .catch(err => {
                        if (isMessage(err)) {
                            toast.error(err.message)
                        } else {
                            toast.error('Error desconocido')
                        }
                    })
                    .finally((): void => {
                        controller.currentPage = 1
                        showWaitOverlay.value = false
                        stopWatcher.value = false
                    })
                break
            }
            case 'movements': {
                const f = movementForm.value
                if (
                    f.from_date.errorMessage ||
                    f.to_date.errorMessage ||
                    f.done_by_name.errorMessage ||
                    f.warehouse_name.errorMessage ||
                    f.status.errorMessage ||
                    f.notes.errorMessage
                ) {
                    toast.error('Verifique los datos antes buscar')
                    showWaitOverlay.value = false
                    return
                } else if (!f.entrada && !f.salida) {
                    toast.error('Escoga tipo de movimiento (Salida/Entrada)')
                    showWaitOverlay.value = false
                    return
                }
                query.from_date = f.from_date.value
                query.to_date = f.to_date.value
                query.done_by_name = f.done_by_name.value
                query.notes = f.notes.value
                query.warehouse_name = f.warehouse_name.value
                query.status = f.status.value
                query.entrada = f.entrada
                query.salida = f.salida
                fetchManager(tabOption, query, { per_page: 15, page: 1 })
                    .then((): void => {
                        if (activeWhInformation.value.movements.length < 1) {
                            toast.error(
                                'No se ha encontrado registros en la búsqueda'
                            )
                        } else {
                            toast.success('Búsqueda exitosa')
                        }
                    })
                    .catch(err => {
                        if (isMessage(err)) {
                            toast.error(err.message)
                        } else {
                            toast.error('Error desconocido')
                        }
                    })
                    .finally((): void => {
                        controller.currentPage = 1
                        showWaitOverlay.value = false
                        stopWatcher.value = false
                    })

                break
            }
        }
    }

    /**
     * Manager function to reset form fields on each search form.
     * Resets inventoryForm, purchaseForm, tomasFisicasForm or movementForm values
     * @param {whCardController}controller WhCardController type corresponding to the option to be reseted
     * @param {string}tabOption The option to know which form to reset ('inventory','purchase','tomas-fisicas','movements')
     */
    async function onReset(
        controller: whCardController,
        tabOption: 'inventory' | 'purchases' | 'tomas-fisicas' | 'movements'
    ): Promise<void> {
        showWaitOverlay.value = true
        switch (tabOption) {
            case 'inventory': {
                inventoryForm.value.name.resetField()
                inventoryForm.value.sku.resetField()
                inventoryForm.value.max_price.resetField()
                inventoryForm.value.min_price.resetField()
                inventoryForm.value.max_quantity.resetField()
                inventoryForm.value.min_quantity.resetField()
                inventoryForm.value.from_date.resetField()
                inventoryForm.value.to_date.resetField()
                break
            }
            case 'purchases': {
                purchaseForm.value.from_date.resetField()
                purchaseForm.value.to_date.resetField()
                purchaseForm.value.approved_date = false
                purchaseForm.value.invoice_date = false
                purchaseForm.value.provider_name.resetField()
                purchaseForm.value.status = false
                purchaseForm.value.invoice_code.resetField()
                purchaseForm.value.reference.resetField()
                break
            }
            case 'tomas-fisicas': {
                tomasFisicasForm.value.from_date.resetField()
                tomasFisicasForm.value.to_date.resetField()
                tomasFisicasForm.value.done_by_name.resetField()
                tomasFisicasForm.value.novedad.resetField()
                break
            }
            case 'movements': {
                movementForm.value.from_date.resetField()
                movementForm.value.to_date.resetField()
                movementForm.value.done_by_name.resetField()
                movementForm.value.notes.resetField()
                movementForm.value.warehouse_name.resetField()
                movementForm.value.status.resetField()
                movementForm.value.entrada = false
                movementForm.value.salida = false
                break
            }
        }
        await fetchManager(
            tabOption,
            { warehouse_id: activeWhInformation.value.bodega.id },
            { page: 1, per_page: whInformationPerPage.value }
        )
        controller.currentPage = 1
        showWaitOverlay.value = false
    }

    /**
     * Manager that fetches all the information related to a warehouse when it is pressed on the main page.
     *Fetches the stock, purchase, movements, and tomas físicas for a warehouse and assigns the information to
     *the activeWhInformation reference variable
     * @param event Button event pressed
     * @param {number}whId Id number of the warehouse
     * @param {number}index Index of the warehouse in the current table
     */
    function wharehouseButtonPressed(
        event: Event,
        whId: number,
        index: number
    ): void {
        activeWharehouseButton.value = whId

        activeWhInformation.value.bodega = (warehouse.getWarehouseList ?? [])[
            index
        ]

        showWaitOverlay.value = true
        stopWatcher.value = true
        resetWhPage()

        Promise.all([
            fetchManager(
                'inventory',
                { warehouse_id: activeWhInformation.value.bodega.id },
                {
                    page: 1,
                    per_page: whInformationPerPage.value,
                }
            ),

            fetchManager(
                'tomas-fisicas',
                { warehouse_id: activeWhInformation.value.bodega.id },
                {
                    page: 1,
                    per_page: whInformationPerPage.value,
                }
            ),
            fetchManager(
                'purchases',
                { warehouse_id: activeWhInformation.value.bodega.id },
                {
                    page: 1,
                    per_page: whInformationPerPage.value,
                }
            ),
            fetchManager(
                'movements',
                { warehouse_id: activeWhInformation.value.bodega.id },
                {
                    page: 1,
                    per_page: whInformationPerPage.value,
                }
            ),
        ])
            .then((): void => {
                showAllWarehouses.value = false
                showWaitOverlay.value = false
                stopWatcher.value = false
            })
            .catch((e): void => {
                toast.error(e.message)
                showWaitOverlay.value = false
            })
            .finally(() => {
                showWaitOverlay.value = false
            })
    }
    /**
     * Contains information for the selected Purchase to be displayed in the purchase modal popup
     */
    const selectedPurchase = ref<Purchase>({
        id: -1,
        approved_at: '',
        order_origin: { id: -1, requested_at: '', revised_by: undefined },
        reference: -1,
        status: 'Cargando',
    })
    /**
     * Manager for the confirm button in the purchase tab table, displays the modal popup
     * @param item Purchase that was clicked on to be confirmed
     */
    function purchaseConfirmHandler(item: Purchase): void {
        selectedPurchase.value = item
        purchaseModalShow.value = true
    }
    /**
     * Function to send a PUT request and update the purchase status
     * Displays a toast message on succes and error
     */
    async function confirmarPedido(): Promise<void> {
        showWaitOverlay.value = true
        const purchase_copy = {
            id: selectedPurchase.value.id,
            status: DELIVERED_PURCHASE_STATUS.value,
        }
        warehouse
            .confirmPurchaseUser(purchase_copy as Purchase)
            .then((): void => {
                toast.success('Entrega del pedido confirmada!')
                selectedPurchase.value.status = DELIVERED_PURCHASE_STATUS.value
                showWaitOverlay.value = false
            })
            .catch((error: MessageResponse) => {
                toast.error(error.message)
                showWaitOverlay.value = false
            })
    }
    /**
     * Flag to show or hide the product modal popup
     */
    const itemInfoShow = ref(false)

    /**
     * Flag to display load bar in product modal popup
     */
    const loadingProps = ref(true)
    /**
     * Contains the information of the selected product to be displayed in the product modal
     */
    const detailSelectedProduct = ref<SelectedItem>({
        product: null,
        variant: null,
        props: [],
    })

    /**
     * Loads product info to the modal popup
     * @param product WarehouseStock with and ProductVariant to fetch the props of
     */
    async function showProduct(product: WarehouseStock): Promise<void> {
        detailSelectedProduct.value.product = product.product
        detailSelectedProduct.value.variant = product.variant
        itemInfoShow.value = true
        detailSelectedProduct.value.props = []
        loadingProps.value = true
        let res = await itemStore.fetchProductProperties({
            variant_id: product.variant.id,
        })
        if (isMessage(res)) {
            loadingProps.value = false
            detailSelectedProduct.value.props[0] = {
                name: 'Error',
                value: 'No se pudo cargar los detalles',
            }
        } else {
            res = res as PaginatedResponse<ProductProps>
            detailSelectedProduct.value.props = res.data
            loadingProps.value = false
        }
    }

    /**
     * Flag for loading bar on tomas fisicas tab modal popup
     */
    const loadingToma = ref(true)
    /**
     * Flag to show or hide toma details modal popup
     */
    const showTomaDetailsModal = ref(false)

    /**
     * Contains de information of the clicked toma fisica
     */
    const selectedToma = ref<TomaFisica & { details: FullTomaFisicaDetail[] }>()

    async function getTomaDetails(): Promise<void> {
        loadingToma.value = true
        let res = await warehouse.fetchPaginatedTomasFisicasDetails(
            { toma_fisica: selectedToma.value?.id },
            { page: 1, per_page: 10000 }
        )
        if (isMessage(res)) {
            toast.error('No se pudo cargar detalles de la toma')
            loadingToma.value = false
        }
        res = res as PaginatedResponse<FullTomaFisicaDetail>

        if (selectedToma.value) {
            selectedToma.value.details = res.data
        }

        loadingToma.value = false
    }

    /**
     * Contains the string search of the main page
     */
    const searchString = ref('')
    /**
     * Filters the main page table with the seacrhString content
     */
    function filterData(): void {
        stopWatcher.value = true
        mainPageController.value.currentPage = 0

        if (searchString.value.length > 0) {
            paginatedMainTable.value = (allWarehousesTableInformation ?? [])

                .filter(warehouse => {
                    return (
                        warehouse.name.includes(searchString.value) ||
                        warehouse.whtf_done_by_lastname?.includes(
                            searchString.value
                        ) ||
                        warehouse.whtf_done_by_name?.includes(
                            searchString.value
                        ) ||
                        warehouse.whtf_novedad?.includes(searchString.value)
                    )
                })
                .slice(
                    mainPageController.value.currentPage * whPageCount.value,
                    (mainPageController.value.currentPage + 1) *
                        whPageCount.value
                )
            stopWatcher.value = false
        } else {
            stopWatcher.value = false
            paginateMain(whPageCount.value, 0)
        }
    }

    const toggle = ref(true)

    /**
     * Transform de key to a more readable Form
     * @param key Key name of Product or VariantProduct to be formated
     */
    function keyNaturalName(key: string): string {
        switch (key) {
            case 'id':
                return 'Código'
            case 'product_name':
                return 'Producto'
            case 'variant_name':
                return 'Nombre de Variante'
            case 'summary':
                return 'Descripción'
            case 'short_description':
                return 'Descripción Corta'
            case 'brand_name':
                return 'Marca'
            case 'base_price':
                return 'Precio Base'
            case 'price':
                return 'Precio de venta'
            case 'sku':
                return 'SKU'
        }
        return key
    }

    function getDisplpayStatus(status: string) {
        const s = purchase.getPurchaseStatus().find(st => (st.name = status))
        return s?.display ? s.display : 'Desconocido'
    }

    /**
     * Shortens a long text to a given lenght ending with a suffix
     * @param text  Input string to be shorten
     * @param length Maximum lenght
     * @param suffix End characters to append
     * @return shortened text
     */
    const truncate = (text: string, length: number, suffix: string): string => {
        if (typeof text == undefined || text == null) {
            return '---'
        }
        if (text.length > length) {
            return text.substring(0, length) + suffix
        } else {
            return text
        }
    }
    /**
     * Load manager for the inventory tab
     */
    const loadInv = async (): Promise<void> => {
        if (!stopWatcher.value) {
            showWaitOverlay.value = true
            await fetchManager(
                'inventory',
                { warehouse_id: activeWhInformation.value.bodega.id },
                {
                    page: invTabController.value.currentPage,
                    per_page: whInformationPerPage.value,
                }
            )
            showWaitOverlay.value = false
        }
    }
    /**
     * Load manager for the purchase tab
     */
    const loadPurchase = async (): Promise<void> => {
        if (!stopWatcher.value) {
            showWaitOverlay.value = true
            await fetchManager(
                'purchases',
                { warehouse_id: activeWhInformation.value.bodega.id },
                {
                    page: purchaseTabController.value.currentPage,
                    per_page: whInformationPerPage.value,
                }
            )
            showWaitOverlay.value = false
        }
    }
    /**
     * Load manager for the tomas físicas tab
     */
    const loadTomas = async (): Promise<void> => {
        if (!stopWatcher.value) {
            showWaitOverlay.value = true
            await fetchManager(
                'tomas-fisicas',
                { warehouse_id: activeWhInformation.value.bodega.id },
                {
                    page: tomasFisicasTabController.value.currentPage,
                    per_page: whInformationPerPage.value,
                }
            )
            showWaitOverlay.value = false
        }
    }
    /**
     * Load manager for the movements tab
     */
    const loadMovements = async (): Promise<void> => {
        if (!stopWatcher.value) {
            showWaitOverlay.value = true
            await fetchManager(
                'movements',
                { warehouse_id: activeWhInformation.value.bodega.id },
                {
                    page: movementTabController.value.currentPage,
                    per_page: whInformationPerPage.value,
                }
            )
            showWaitOverlay.value = false
        }
    }
    function statusColor(status?: string): ColorVariant {
        switch (status) {
            case 'entregado':
                return 'success'
            case 'aprovado':
                return 'primary'
            case 'transito':
                return 'warning'
            case 'rechazado':
                return 'danger'
            case 'cancelado':
                return 'dark'
            case 'pagado':
                return 'light'
            default:
                return 'info'
        }
    }

    watch(invTabController.value, loadInv)
    watch(purchaseTabController.value, loadPurchase)
    watch(tomasFisicasTabController.value, loadTomas)
    watch(movementTabController.value, loadMovements)
    watch(searchString, filterData)

    warehouse
        .fetchWarehouses()
        .then((): void => {
            whRows.value = (warehouse.getWarehouseList ?? []).length
            paginateAside(whPageCount.value, 0)
        })
        .catch((): void => {
            toast.error('Error en la carga de datos')
            showWaitOverlay.value = false
        })
    warehouse
        .fetchWarehousesLatestTomasFisicas()
        .then(it => {
            allWarehousesTableInformation = it as unknown as WhWithTomaFisica[]
            paginateMain(whPageCount.value, 0)
            showWaitOverlay.value = false
        })
        .catch((): void => {
            toast.error('Error en la carga de datos')
            showWaitOverlay.value = false
        })
</script>

<template>
    <WaitOverlay :show="showWaitOverlay">
        <ECard>
            <div
                class="row d-inline-flex allign-content-center tw-bg-slate-50 dark:tw-bg-slate-600">
                <div
                    v-if="toggle"
                    class="row col-sm-12 col-md-12 col-xl-2 mx-1 tw-flex-col tw-rounded-lg tw-bg-white dark:tw-bg-slate-800 justify-center">
                    <h1 class="title my-2 col-5">Bodegas Disponibles</h1>

                    <e-button
                        @click.left="
                            () => {
                                toggle = false
                            }
                        "
                        class="tw-text-slate-800 col-lg-3 col-md-3 col-sm-6 col-xl-6 mx-3 mb-3"
                        left-icon="chevrons-left"
                        icon-provider="feather">
                    </e-button>

                    <b-pagination
                        v-model="currentAsidePage"
                        :total-rows="whRows"
                        :per-page="whPageCount"
                        aria-controls="b-list-warehouses"
                        align="center"
                        @page-click.left="onAsidePageChanged"
                        :limit="3"
                        hide-goto-end-buttons
                        class="paginator mb-2"></b-pagination>

                    <b-list-group
                        :per-page="whPageCount"
                        :current-page="currentAsidePage"
                        class="button-group smaller-btn-group col-lg-12 col-md-6 col-sm-6">
                        <b-list-group-item
                            :class="{ active: activeWharehouseButton === -1 }"
                            button
                            @click.left="
                                () => {
                                    showAllWarehouses = true
                                    activeWharehouseButton = -1
                                }
                            ">
                            Todas las bodegas
                        </b-list-group-item>
                        <b-list-group-item
                            v-for="(wh, index) in paginatedWarehouse"
                            button
                            :class="{
                                active: wh.id === activeWharehouseButton,
                            }"
                            :key="wh.id"
                            :id="'whbtn-' + wh.id"
                            @click.left="
                                wharehouseButtonPressed($event, wh.id, index)
                            ">
                            {{ wh.name }}
                        </b-list-group-item>
                    </b-list-group>
                </div>

                <div
                    v-if="showAllWarehouses"
                    class="col-xl tw-bg-slate-50 dark:tw-bg-slate-700">
                    <div class="row">
                        <e-button
                            v-if="!toggle"
                            @click.left="
                                () => {
                                    toggle = true
                                }
                            "
                            class="mx-2 my-3 tw-text-slate-800 tw-text-sm mx-1 col-1"
                            left-icon="chevrons-right"
                            icon-provider="feather">
                        </e-button>

                        <h1 class="title tw-text-3xl tw-mt-2 mb-2 col-6">
                            Bodegas y Últimas Tomas Físicas
                        </h1>
                    </div>

                    <div class="row display-inline-flex mb-2">
                        <b-form inline class="col-3">
                            <b-form-input
                                id="wh-search"
                                v-model="searchString"
                                placeholder="Búsqueda de Bodega">
                            </b-form-input>
                        </b-form>
                        <e-button
                            type="button"
                            variant="primary"
                            class="col-2"
                            @click.left="
                                () => {
                                    searchString = ''
                                }
                            "
                            >Limpiar Búsqueda
                        </e-button>

                        <b-pagination
                            v-model="mainPageController.currentPage"
                            :total-rows="whRows"
                            :per-page="whPageCount"
                            aria-controls="b-list-warehouses"
                            align="center"
                            @page-click.left="onMainPageChanged"
                            :limit="10"
                            class="paginator col-5 tw-inline-flex"></b-pagination>
                    </div>

                    <BTable
                        outline
                        :fields="allWarehousesFields"
                        :items="paginatedMainTable"
                        class="text-center">
                        <template #cell(#)="{ index }">
                            {{ index + 1 }}
                        </template>
                        <template #cell(RealizadaPor)="{ item }">
                            {{
                                (item.whtf_done_by_name ?? '--') +
                                ' ' +
                                (item.whtf_done_by_lastname ?? '--')
                            }}
                        </template>
                        <template #cell(FechaTomaFísica)="{ item }">
                            {{ truncate(item.whtf_created_at, 10, '') }}
                        </template>
                        <template #cell(Novedad)="{ item }">
                            {{ truncate(item.whtf_novedad, 15, '...') }}
                        </template>
                        <template #cell(Detalles)="{ item, index }">
                            <e-button
                                @click.left="
                                    wharehouseButtonPressed(
                                        $event,
                                        item.id,
                                        index
                                    )
                                "
                                left-icon="fa-eye"
                                type="button"
                                variant="primary"
                                >Ver Bodega
                            </e-button>
                        </template>
                    </BTable>
                </div>

                <!-- Specific warehouse card  -->

                <div v-else class="col-xl">
                    <div
                        class="row tw-bg-slate-50 dark:tw-bg-slate-600 mt-2 mb-2">
                        <e-button
                            v-if="!toggle"
                            @click.left="
                                () => {
                                    toggle = true
                                }
                            "
                            class="tw-text-slate-800 tw-text-sm mx-1 col-1"
                            left-icon="chevrons-right"
                            icon-provider="feather">
                        </e-button>
                        <h1 class="tw-text-3xl tw-font-bold col-10">
                            {{ activeWhInformation.bodega?.name }}
                        </h1>
                    </div>

                    <b-tabs
                        active-tab-class=""
                        content-class="mt-3 tabs-style"
                        pills>
                        <!--


                            INVENTARIO TAB


                        -->

                        <b-tab title="Inventario" active>
                            <div class="row display-inline-flex mb-1">
                                <e-button
                                    v-b-toggle.collapse-1
                                    type="button"
                                    variant="primary"
                                    class="col-2 mx-1 col-md-3 col-sm-4"
                                    >Desplegar Búsqueda
                                </e-button>
                                <b-collapse id="collapse-1" class="mt-2">
                                    <ECard>
                                        <ValidationForm
                                            v-slot="{ handleReset }"
                                            @submit="
                                                () => {
                                                    onSubmit(
                                                        'inventory',
                                                        invTabController
                                                    )
                                                }
                                            "
                                            :validation-schema="inventoryForm">
                                            <div class="row" align-v="start">
                                                <div
                                                    class="col-lg-4 col-xl-3 col-sm-6">
                                                    <Datepicker
                                                        v-model="
                                                            inventoryForm
                                                                .from_date.value
                                                        "
                                                        :max-date="
                                                            inventoryForm
                                                                .to_date?.value
                                                        "
                                                        show-now-button
                                                        now-button-label="Ahora"
                                                        auto-apply
                                                        close-on-scroll
                                                        textinput
                                                        dark
                                                        teleport-center>
                                                        <template
                                                            #dp-input="{
                                                                value,
                                                            }">
                                                            <InputText
                                                                label="Fecha Min de Actualización"
                                                                :model-value="
                                                                    value
                                                                "
                                                                :info-label="
                                                                    inventoryForm
                                                                        .from_date
                                                                        .errorMessage
                                                                "
                                                                :status="
                                                                    Boolean(
                                                                        inventoryForm
                                                                            .from_date
                                                                            .errorMessage
                                                                    )
                                                                "
                                                                info-status="danger" />
                                                        </template>
                                                    </Datepicker>
                                                </div>
                                                <div
                                                    class="col-lg-4 col-xl-3 col-sm-6">
                                                    <Datepicker
                                                        v-model="
                                                            inventoryForm
                                                                .to_date.value
                                                        "
                                                        :min-date="
                                                            inventoryForm
                                                                .from_date
                                                                ?.value
                                                        "
                                                        show-now-button
                                                        now-button-label="Ahora"
                                                        auto-apply
                                                        close-on-scroll
                                                        textinput
                                                        dark
                                                        teleport-center>
                                                        <template
                                                            #dp-input="{
                                                                value,
                                                            }">
                                                            <InputText
                                                                label="Fecha Max de Actualización"
                                                                :model-value="
                                                                    value
                                                                "
                                                                :info-label="
                                                                    inventoryForm
                                                                        .to_date
                                                                        .errorMessage
                                                                "
                                                                :status="
                                                                    Boolean(
                                                                        inventoryForm
                                                                            .to_date
                                                                            .errorMessage
                                                                    )
                                                                "
                                                                info-status="danger" />
                                                        </template>
                                                    </Datepicker>
                                                </div>
                                                <div
                                                    class="col-lg-6 col-xl-3 col-sm-12 mt-auto">
                                                    <InputText
                                                        label="Código Producto"
                                                        v-model="
                                                            inventoryForm.sku
                                                                .value
                                                        "
                                                        :info-label="
                                                            inventoryForm.sku
                                                                .errorMessage
                                                        "
                                                        :status="
                                                            Boolean(
                                                                inventoryForm
                                                                    .sku
                                                                    .errorMessage
                                                            )
                                                        "
                                                        info-status="danger" />
                                                </div>
                                                <div
                                                    class="col-lg-4 col-xl-3 col-sm-6 mt-auto">
                                                    <InputText
                                                        label="Nombre Producto"
                                                        v-model="
                                                            inventoryForm.name
                                                                .value
                                                        "
                                                        :info-label="
                                                            inventoryForm.name
                                                                .errorMessage
                                                        "
                                                        :status="
                                                            Boolean(
                                                                inventoryForm
                                                                    .name
                                                                    .errorMessage
                                                            )
                                                        "
                                                        info-status="danger" />
                                                </div>
                                            </div>
                                            <div class="row" align-v="start">
                                                <div
                                                    class="col-sm-3 col-lg-4 col-xl-2">
                                                    <InputText
                                                        label="Cantidad Min"
                                                        v-model="
                                                            inventoryForm
                                                                .min_quantity
                                                                .value
                                                        "
                                                        :info-label="
                                                            inventoryForm
                                                                .min_quantity
                                                                .errorMessage
                                                        "
                                                        :status="
                                                            Boolean(
                                                                inventoryForm
                                                                    .min_quantity
                                                                    .errorMessage
                                                            )
                                                        "
                                                        info-status="danger" />
                                                </div>
                                                <div
                                                    class="col-sm-3 col-lg-4 col-xl-2">
                                                    <InputText
                                                        label="Cantidad Max"
                                                        v-model="
                                                            inventoryForm
                                                                .max_quantity
                                                                .value
                                                        "
                                                        :info-label="
                                                            quantity_message
                                                        "
                                                        :status="
                                                            Boolean(
                                                                inventoryForm
                                                                    .max_quantity
                                                                    .errorMessage
                                                            )
                                                        "
                                                        @input="
                                                            quantityRangeError
                                                        "
                                                        info-status="danger" />
                                                </div>
                                                <div
                                                    class="col-sm-3 col-lg-4 col-xl-2">
                                                    <InputText
                                                        label="Precio Min"
                                                        v-model="
                                                            inventoryForm
                                                                .min_price.value
                                                        "
                                                        :info-label="
                                                            inventoryForm
                                                                .min_price
                                                                .errorMessage
                                                        "
                                                        :status="
                                                            Boolean(
                                                                inventoryForm
                                                                    .min_price
                                                                    .errorMessage
                                                            )
                                                        "
                                                        info-status="danger" />
                                                </div>
                                                <div
                                                    class="col-sm-3 col-lg-4 col-xl-2">
                                                    <InputText
                                                        label="Precio Max"
                                                        v-model="
                                                            inventoryForm
                                                                .max_price.value
                                                        "
                                                        :info-label="
                                                            price_message
                                                        "
                                                        :status="
                                                            Boolean(
                                                                inventoryForm
                                                                    .max_price
                                                                    .errorMessage
                                                            )
                                                        "
                                                        @input="priceRangeError"
                                                        info-status="danger" />
                                                </div>
                                                <div
                                                    class="col-2 col-md-3 col-sm-4 mt-4 text-center">
                                                    <EButton class="">
                                                        Confirmar Búsqueda
                                                    </EButton>
                                                </div>
                                                <div
                                                    class="col-2 col-sm-3 col-md-3 col-sm-4 mt-4">
                                                    <e-button
                                                        @click.left="
                                                            () => {
                                                                onReset(
                                                                    invTabController,
                                                                    'inventory'
                                                                )
                                                                handleReset()
                                                            }
                                                        "
                                                        type="button"
                                                        variant="secondary">
                                                        Limpiar Búsqueda
                                                    </e-button>
                                                </div>
                                            </div>
                                        </ValidationForm>
                                    </ECard>
                                </b-collapse>
                            </div>

                            <ModalDialog
                                v-model:show="itemInfoShow"
                                size="3xl"
                                class="dark-mode-text">
                                <template #dialog-title>
                                    <b class="tw-text-2xl dark-mode-text"
                                        >Detalle del producto
                                        {{
                                            detailSelectedProduct.product
                                                ?.product_name +
                                            ' ' +
                                            detailSelectedProduct.variant
                                                ?.variant_name
                                        }}</b
                                    >
                                </template>
                                <div class="container">
                                    <h3
                                        class="tw-text-xl tw-font-bold dark-mode-text">
                                        Detalle
                                    </h3>
                                    <div
                                        class="row tw-pb-3 align-content-center justify-content-center gy-2">
                                        <template
                                            v-for="(
                                                d, k
                                            ) in detailSelectedProduct.variant"
                                            :key="k">
                                            <div
                                                class="col-12"
                                                v-if="
                                                    ![
                                                        'base_price',
                                                        'created_at',
                                                        'updated_at',
                                                        'is_active',
                                                        'deleted_at',
                                                    ].includes(k)
                                                ">
                                                <div class="row">
                                                    <span
                                                        class="tw-font-bold col-4 dark-mode-text"
                                                        >{{
                                                            keyNaturalName(k)
                                                        }}:</span
                                                    >
                                                    <span
                                                        class="col-4 dark-mode-text"
                                                        >{{ d }}</span
                                                    >
                                                </div>
                                            </div>
                                        </template>

                                        <div class="col-12">
                                            <div class="row">
                                                <span
                                                    class="col-4 tw-font-bold">
                                                    Marca:
                                                </span>
                                                <span class="col-4">
                                                    {{
                                                        detailSelectedProduct
                                                            .product?.brand_name
                                                    }}
                                                </span>
                                            </div>
                                        </div>
                                        <div class="row"></div>
                                        <div class="col-12"></div>
                                        <div class="col-12 mb-2">
                                            <div class="row dark-mode-text">
                                                <span
                                                    class="col-4 tw-font-bold">
                                                    Descripcion corta:
                                                </span>
                                                <p
                                                    class="col-4 tw-text-ellipsis">
                                                    {{
                                                        detailSelectedProduct
                                                            .product
                                                            ?.short_description
                                                    }}
                                                </p>
                                            </div>
                                        </div>
                                    </div>

                                    <LoadingBar
                                        v-show="loadingProps"
                                        class="tw-mt-5" />
                                    <div
                                        v-if="detailSelectedProduct.props"
                                        class="tw-ring-1 tw-ring-slate-500 tw-rounded tw-pb-3 row">
                                        <h3
                                            class="col-12 tw-text-xl tw-py-1.5 dark-mode-text">
                                            <b>Características del Producto</b>
                                        </h3>
                                        <template
                                            v-for="(
                                                param, idx
                                            ) in detailSelectedProduct.props"
                                            :key="idx">
                                            <div
                                                class="col-6 col-md-3 col-xl-3 tw-text-md dark-mode-text">
                                                <b>{{ param.name }}:</b>
                                            </div>
                                            <div
                                                class="col-6 col-md-3 col-xl-3 dark-mode-text">
                                                {{ param.value }}
                                            </div>
                                        </template>
                                    </div>
                                </div>
                            </ModalDialog>
                            <BTable
                                outline
                                id="whinv-table"
                                :fields="inventoryFields"
                                :items="activeWhInformation.inventory"
                                class="table">
                                <template #cell(#)="{ index }">
                                    {{
                                        index +
                                        1 +
                                        (invTabController.currentPage - 1) *
                                            whInformationPerPage
                                    }}
                                </template>
                                <template #cell(Código)="{ item }">
                                    {{ item.variant.sku }}
                                </template>
                                <template #cell(Producto)="{ item }">
                                    {{ item.product.product_name }}
                                </template>
                                <template #cell(Variante)="{ item }">
                                    {{ item.variant.variant_name }}
                                </template>
                                <template #cell(Marca)="{ item }">
                                    {{ item.product.brand_name }}
                                </template>
                                <template #cell(PrecioVenta)="{ item }">
                                    {{ Number(item.variant.price).toFixed(2) }}
                                </template>
                                <template #cell(Acciones)="{ item }">
                                    <e-button
                                        left-icon="fa-eye"
                                        @click.left="showProduct(item)"
                                        type="button"
                                        variant="primary"
                                        >Ver detalles
                                    </e-button>
                                </template>
                            </BTable>

                            <b-pagination
                                v-model="invTabController.currentPage"
                                :total-rows="invTabController.totalRows"
                                :per-page="whInformationPerPage"
                                aria-controls="whinv-table"
                                align="center"
                                :limit="10"
                                hide-goto-end-buttons
                                class="paginator"></b-pagination>
                        </b-tab>

                        <!--


                            HISTORIAL DE COMPRAS TAB


                        -->

                        <b-tab title="Historial de Compras">
                            <div class="row display-inline-flex mb-1">
                                <div class="row display-inline-flex mb-1">
                                    <e-button
                                        v-b-toggle.collapse-2
                                        type="button"
                                        variant="primary"
                                        class="col-2 mx-1 col-md-3 col-sm-4"
                                        >Desplegar Búsqueda
                                    </e-button>
                                    <b-collapse id="collapse-2" class="mt-2">
                                        <ModalDialog
                                            id="purchase-modal"
                                            v-model:show="purchaseModalShow"
                                            title="Confirmar Entrega de pedido"
                                            ok-text="Confirmar"
                                            @ok="confirmarPedido()"
                                            button-type="ok-cancel">
                                            <h1
                                                class="tw-text-3xl tw-text-black dark:tw-text-white">
                                                ¿Quiere confirmar que llegó el
                                                pedido en su totalidad?
                                            </h1>

                                            <div class="row">
                                                <div
                                                    class="row col-12 tw-rounded tw-ring-1 tw-ring-yellow-400 dark-mode-text tw-py-2">
                                                    <h3
                                                        class="tw-w-1/2 tw-font-bold col-6">
                                                        Fecha de aprobacion:
                                                    </h3>
                                                    <p class="col-6">
                                                        {{
                                                            selectedPurchase?.approved_at
                                                        }}
                                                    </p>
                                                </div>
                                                <div
                                                    class="row col-12 tw-rounded tw-ring-1 tw-ring-yellow-400 tw-py-2 dark-mode-text">
                                                    <h3
                                                        class="tw-w-1/2 tw-font-bold col-6">
                                                        Código de referencia
                                                    </h3>
                                                    <p class="col-6">
                                                        {{
                                                            selectedPurchase?.reference
                                                        }}
                                                    </p>
                                                </div>
                                            </div>
                                        </ModalDialog>
                                        <ECard>
                                            <ValidationForm
                                                v-slot="{ handleReset }"
                                                @submit="
                                                    onSubmit(
                                                        'purchases',
                                                        purchaseTabController
                                                    )
                                                "
                                                :validation-schema="
                                                    purchaseForm
                                                ">
                                                <div
                                                    class="row"
                                                    align-v="start">
                                                    <div
                                                        class="col-lg-4 col-xl-3 col-sm-6">
                                                        <Datepicker
                                                            v-model="
                                                                purchaseForm
                                                                    .from_date
                                                                    .value
                                                            "
                                                            :max-date="
                                                                purchaseForm
                                                                    .to_date
                                                                    ?.value
                                                            "
                                                            show-now-button
                                                            now-button-label="Ahora"
                                                            auto-apply
                                                            close-on-scroll
                                                            textinput
                                                            dark
                                                            teleport-center>
                                                            <template
                                                                #dp-input="{
                                                                    value,
                                                                }">
                                                                <InputText
                                                                    label="Fecha Mínima"
                                                                    :model-value="
                                                                        value
                                                                    "
                                                                    :info-label="
                                                                        purchaseForm
                                                                            .from_date
                                                                            .errorMessage
                                                                    "
                                                                    :status="
                                                                        Boolean(
                                                                            purchaseForm
                                                                                .from_date
                                                                                .errorMessage
                                                                        )
                                                                    "
                                                                    info-status="danger" />
                                                            </template>
                                                        </Datepicker>
                                                    </div>
                                                    <div
                                                        class="col-lg-4 col-xl-3 col-sm-6">
                                                        <Datepicker
                                                            v-model="
                                                                purchaseForm
                                                                    .to_date
                                                                    .value
                                                            "
                                                            :min-date="
                                                                purchaseForm
                                                                    .from_date
                                                                    ?.value
                                                            "
                                                            show-now-button
                                                            now-button-label="Ahora"
                                                            auto-apply
                                                            close-on-scroll
                                                            textinput
                                                            dark
                                                            teleport-center>
                                                            <template
                                                                #dp-input="{
                                                                    value,
                                                                }">
                                                                <InputText
                                                                    label="Fecha Máxima"
                                                                    :model-value="
                                                                        value
                                                                    "
                                                                    :info-label="
                                                                        purchaseForm
                                                                            .to_date
                                                                            .errorMessage
                                                                    "
                                                                    :status="
                                                                        Boolean(
                                                                            purchaseForm
                                                                                .to_date
                                                                                .errorMessage
                                                                        )
                                                                    "
                                                                    info-status="danger" />
                                                            </template>
                                                        </Datepicker>
                                                    </div>
                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <b-form-checkbox
                                                            class="tw-text-xl form-check-input"
                                                            v-model="
                                                                purchaseForm.approved_date
                                                            "
                                                            switch>
                                                            Buscar Por Fecha de
                                                            Creación
                                                        </b-form-checkbox>
                                                    </div>
                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <b-form-checkbox
                                                            class="tw-text-xl form-check-input"
                                                            v-model="
                                                                purchaseForm.invoice_date
                                                            "
                                                            name="checkbox-1"
                                                            switch>
                                                            Buscar Por Fecha de
                                                            Pago
                                                        </b-form-checkbox>
                                                    </div>

                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <b-form-checkbox
                                                            class="tw-text-xl form-check-input"
                                                            v-model="
                                                                purchaseForm.status
                                                            "
                                                            name="checkbox-2"
                                                            switch>
                                                            Buscar Compras
                                                            Entregadas
                                                        </b-form-checkbox>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div
                                                        class="col-lg-6 col-xl-3 col-sm-12 mt-auto">
                                                        <InputText
                                                            label="Código de Orden"
                                                            v-model="
                                                                purchaseForm
                                                                    .reference
                                                                    .value
                                                            "
                                                            :info-label="
                                                                purchaseForm
                                                                    .reference
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    purchaseForm
                                                                        .reference
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>
                                                    <div
                                                        class="col-lg-4 col-xl-3 col-sm-6 mt-auto">
                                                        <InputText
                                                            label="Nombre de Provedor"
                                                            v-model="
                                                                purchaseForm
                                                                    .provider_name
                                                                    .value
                                                            "
                                                            :info-label="
                                                                purchaseForm
                                                                    .provider_name
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    purchaseForm
                                                                        .provider_name
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>
                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <InputText
                                                            label="Código de pago"
                                                            v-model="
                                                                purchaseForm
                                                                    .invoice_code
                                                                    .value
                                                            "
                                                            :info-label="
                                                                purchaseForm
                                                                    .invoice_code
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    purchaseForm
                                                                        .invoice_code
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>
                                                    <div
                                                        class="col-2 mt-4 text-center">
                                                        <EButton class="">
                                                            Confirmar Búsqueda
                                                        </EButton>
                                                    </div>

                                                    <div
                                                        class="col-2 col-md-3 col-sm-4 mt-4">
                                                        <e-button
                                                            @click.left="
                                                                () => {
                                                                    onReset(
                                                                        purchaseTabController,
                                                                        'purchases'
                                                                    )
                                                                    handleReset()
                                                                }
                                                            "
                                                            type="button"
                                                            variant="secondary">
                                                            Limpiar Búsqueda
                                                        </e-button>
                                                    </div>
                                                </div>
                                            </ValidationForm>
                                        </ECard>
                                    </b-collapse>
                                </div>
                            </div>

                            <BTable
                                outline
                                class="tw-capitalize"
                                :fields="purchasesFields"
                                :items="activeWhInformation.purchases">
                                <template #cell(#)="{ index }">
                                    {{
                                        index +
                                        1 +
                                        (purchaseTabController.currentPage -
                                            1) *
                                            whInformationPerPage
                                    }}
                                </template>
                                <template #cell(FechaAprobación)="{ item }">
                                    {{ truncate(item.approved_at, 10, '') }}
                                </template>
                                'AprobadoPor',
                                <template #cell(AprobadoPor)="{ item }">
                                    {{
                                        truncate(
                                            item.order_origin.revised_by?.name +
                                                ' ' +
                                                item.order_origin.revised_by
                                                    ?.lastname,
                                            25,
                                            '...'
                                        )
                                    }}
                                </template>
                                <template #cell(RazonDeCompra)="{ item }">
                                    {{
                                        item.order_origin.revised_by?.comment
                                            ? truncate(
                                                  item.order_origin.revised_by
                                                      ?.comment,
                                                  25,
                                                  '...'
                                              )
                                            : '---'
                                    }}
                                </template>
                                <template #cell(Estado)="{ item }">
                                    <BBadge
                                        class="tw-text-md"
                                        :variant="statusColor(item.status)">
                                        {{ getDisplpayStatus(item.status) }}
                                    </BBadge>
                                </template>
                                <template #cell(Entregado)="{ item }">
                                    <e-button
                                        v-if="
                                            item.status ===
                                            DELIVERED_PURCHASE_STATUS
                                        "
                                        class="tw-py-1 tw-px-1"
                                        left-icon="check"
                                        type="button"
                                        variant="outline"
                                        @click.prevent>
                                        Entregado
                                    </e-button>
                                    <e-button
                                        v-else
                                        class="tw-py-1 tw-px-1"
                                        type="button"
                                        variant="primary"
                                        @click.left="
                                            purchaseConfirmHandler(item)
                                        ">
                                        Confirmar Entrega
                                    </e-button>
                                </template>
                                <template #cell(Acciones)="{ item }">
                                    <e-button
                                        left-icon="fa-eye"
                                        type="button"
                                        variant="primary"
                                        @click.left="
                                            router.push({
                                                path: `/bodegas/pedidos/${item.id}`,
                                            })
                                        "
                                        >Ver detalles
                                    </e-button>
                                </template>
                            </BTable>

                            <b-pagination
                                v-model="purchaseTabController.currentPage"
                                :total-rows="purchaseTabController.totalRows"
                                :per-page="whInformationPerPage"
                                aria-controls="whpurchase-table"
                                align="center"
                                :limit="10"
                                hide-goto-end-buttons
                                class="paginator"></b-pagination>
                        </b-tab>

                        <!--


                            TOMAS FISICAS TAB


                        -->

                        <b-tab title="Toma Física">
                            <div class="row display-inline-flex mb-1">
                                <e-button
                                    v-b-toggle.collapse-3
                                    type="button"
                                    variant="primary"
                                    class="col-2 mx-1 col-md-3 col-sm-4"
                                    >Desplegar Búsqueda
                                </e-button>
                                <e-button
                                    type="button"
                                    variant="primary"
                                    class="col-2 mx-1 col-md-3 col-sm-4"
                                    @click.left="
                                        router.push({
                                            path: `/bodegas/tomas-fisicas/${activeWhInformation.bodega.id}`,
                                        })
                                    "
                                    >Realizar Nueva Toma Física
                                </e-button>
                                <b-collapse id="collapse-3" class="mt-2">
                                    <ECard>
                                        <ValidationForm
                                            v-slot="{ handleReset }"
                                            @submit="
                                                onSubmit(
                                                    'tomas-fisicas',
                                                    tomasFisicasTabController
                                                )
                                            "
                                            :validation-schema="
                                                tomasFisicasForm
                                            ">
                                            <div class="row" align-v="start">
                                                <div
                                                    class="col-lg-6 col-xl-4 col-sm-6">
                                                    <Datepicker
                                                        v-model="
                                                            tomasFisicasForm
                                                                .from_date.value
                                                        "
                                                        :max-date="
                                                            tomasFisicasForm
                                                                .to_date?.value
                                                        "
                                                        show-now-button
                                                        now-button-label="Ahora"
                                                        auto-apply
                                                        close-on-scroll
                                                        textinput
                                                        dark
                                                        teleport-center>
                                                        <template
                                                            #dp-input="{
                                                                value,
                                                            }">
                                                            <InputText
                                                                label="Fecha Min de Actualización"
                                                                :model-value="
                                                                    value
                                                                "
                                                                :info-label="
                                                                    tomasFisicasForm
                                                                        .from_date
                                                                        .errorMessage
                                                                "
                                                                :status="
                                                                    Boolean(
                                                                        tomasFisicasForm
                                                                            .from_date
                                                                            .errorMessage
                                                                    )
                                                                "
                                                                info-status="danger" />
                                                        </template>
                                                    </Datepicker>
                                                </div>
                                                <div
                                                    class="col-lg-6 col-xl-4 col-sm-6">
                                                    <Datepicker
                                                        v-model="
                                                            tomasFisicasForm
                                                                .to_date.value
                                                        "
                                                        :min-date="
                                                            tomasFisicasForm
                                                                .from_date.value
                                                        "
                                                        show-now-button
                                                        now-button-label="Ahora"
                                                        auto-apply
                                                        close-on-scroll
                                                        textinput
                                                        dark
                                                        teleport-center>
                                                        <template
                                                            #dp-input="{
                                                                value,
                                                            }">
                                                            <InputText
                                                                label="Fecha Max de Actualización"
                                                                :model-value="
                                                                    value
                                                                "
                                                                :info-label="
                                                                    tomasFisicasForm
                                                                        .to_date
                                                                        .errorMessage
                                                                "
                                                                :status="
                                                                    Boolean(
                                                                        tomasFisicasForm
                                                                            .to_date
                                                                            .errorMessage
                                                                    )
                                                                "
                                                                info-status="danger" />
                                                        </template>
                                                    </Datepicker>
                                                </div>
                                                <div
                                                    class="col-lg-6 col-xl-4 col-sm-12 mt-auto">
                                                    <InputText
                                                        label="Realizada Por"
                                                        v-model="
                                                            tomasFisicasForm
                                                                .done_by_name
                                                                .value
                                                        "
                                                        :info-label="
                                                            tomasFisicasForm
                                                                .done_by_name
                                                                .errorMessage
                                                        "
                                                        :status="
                                                            Boolean(
                                                                tomasFisicasForm
                                                                    .done_by_name
                                                                    .errorMessage
                                                            )
                                                        "
                                                        placeholder="Ingrese un nombre o apellido"
                                                        info-status="danger" />
                                                </div>
                                                <div class="row">
                                                    <div
                                                        class="col-lg-6 col-xl-4 col-sm-6 mt-auto">
                                                        <InputText
                                                            label="Novedad"
                                                            v-model="
                                                                tomasFisicasForm
                                                                    .novedad
                                                                    .value
                                                            "
                                                            :info-label="
                                                                tomasFisicasForm
                                                                    .novedad
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    tomasFisicasForm
                                                                        .novedad
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>

                                                    <div
                                                        class="col-2 mt-4 col-sm-3 text-center">
                                                        <EButton class="">
                                                            Confirmar Búsqueda
                                                        </EButton>
                                                    </div>

                                                    <div
                                                        class="col-2 col-md-3 col-sm-4 mt-4">
                                                        <e-button
                                                            @click.left="
                                                                () => {
                                                                    onReset(
                                                                        tomasFisicasTabController,
                                                                        'tomas-fisicas'
                                                                    )
                                                                    handleReset()
                                                                }
                                                            "
                                                            type="button"
                                                            variant="secondary">
                                                            Limpiar Búsqueda
                                                        </e-button>
                                                    </div>
                                                </div>
                                            </div>
                                        </ValidationForm>
                                    </ECard>
                                </b-collapse>
                            </div>
                            <ModalDialog
                                v-model:show="showTomaDetailsModal"
                                size="3xl">
                                <template #dialog-title>
                                    <b class="tw-text-2xl dark-mode-text"
                                        >Detalle de la toma física realizada por
                                        :
                                        {{
                                            selectedToma?.done_by?.name +
                                            ' ' +
                                            selectedToma?.done_by?.lastname
                                        }}</b
                                    >
                                </template>
                                <div class="container">
                                    <h3
                                        class="tw-text-xl tw-font-bold dark-mode-text">
                                        Detalle
                                    </h3>
                                    <div
                                        class="row tw-pb-3 align-content-center justify-content-center gy-2">
                                        <template>
                                            <div
                                                class="tw-rounded tw-ring-1 tw-ring-yellow-400 tw-py-1 col-12 col-md-5 tw-mx-2">
                                                <div class="row">
                                                    <span
                                                        class="tw-w-1/2 tw-font-bold col-6 dark-mode-text"
                                                        >Notas de la toma:</span
                                                    >
                                                    <span
                                                        class="col-6 dark-mode-text"
                                                        >{{
                                                            selectedToma?.novedad
                                                        }}</span
                                                    >
                                                </div>
                                            </div>
                                        </template>
                                        <template>
                                            <div
                                                class="tw-rounded tw-ring-1 tw-ring-yellow-400 tw-py-1 col-12 col-md-5 tw-mx-2">
                                                <div class="row">
                                                    <span
                                                        class="tw-w-1/2 tw-font-bold col-6 dark-mode-text"
                                                        >Fecha de
                                                        FechaRealizacion:
                                                    </span>
                                                    <span
                                                        class="col-6 dark-mode-text"
                                                        >{{
                                                            truncate(
                                                                selectedToma?.creaed_at
                                                                    ? selectedToma.creaed_at
                                                                    : '',
                                                                10,
                                                                ''
                                                            )
                                                        }}</span
                                                    >
                                                </div>
                                            </div>
                                        </template>
                                        <LoadingBar
                                            v-show="loadingToma"
                                            class="tw-mt-5" />
                                        <template
                                            v-for="(
                                                details, idx
                                            ) in selectedToma?.details"
                                            :key="idx">
                                            <span
                                                class="tw-w-1/2 col-6 dark-mode-text"
                                                >{{
                                                    details.product
                                                        .product_name +
                                                    '/' +
                                                    details.variant.variant_name
                                                }}
                                            </span>
                                            <div
                                                class="tw-rounded tw-ring-1 tw-ring-yellow-400 tw-py-1 col-12 mb-2">
                                                <div class="row mb-1">
                                                    <span
                                                        class="tw-font-bold mx-2 col-2 dark-mode-text"
                                                        >Stock previo:</span
                                                    >
                                                    <span
                                                        class="mx-2 col-2 dark-mode-text">
                                                        {{
                                                            details.previous_stock
                                                        }}
                                                    </span>

                                                    <span
                                                        class="tw-font-bold col-2 dark-mode-text">
                                                        Nuevo stock:
                                                    </span>

                                                    <span
                                                        class="col-2 dark-mode-text"
                                                        >{{
                                                            details.new_stock
                                                        }}</span
                                                    >
                                                </div>
                                                <div class="row">
                                                    <span
                                                        class="tw-font-bold col-2 dark-mode-text mx-2">
                                                        Novedad:
                                                    </span>
                                                    <div
                                                        class="overflow-hidden text-break text-wrap dark-mode-text col-8 text-right">
                                                        {{ details.novedad }}
                                                    </div>
                                                </div>
                                            </div>
                                        </template>
                                    </div>
                                </div>
                            </ModalDialog>

                            <BTable
                                outline
                                :fields="tomasFisFields"
                                :items="activeWhInformation.tomasFisicas">
                                <template #cell(#)="{ index }">
                                    {{
                                        index +
                                        1 +
                                        (tomasFisicasTabController.currentPage -
                                            1) *
                                            whInformationPerPage
                                    }}
                                </template>
                                <template #cell(FechaRealizacion)="{ item }">
                                    {{ truncate(item.created_at, 10, '') }}
                                </template>
                                <template #cell(RealizadaPor)="{ item }">
                                    {{
                                        item.done_by.name +
                                        ' ' +
                                        item.done_by.lastname
                                    }}
                                </template>
                                <template #cell(Novedad)="{ item }">
                                    {{ truncate(item.novedad, 25, '...') }}
                                </template>
                                <template #cell(Acciones)="{ item }">
                                    <e-button
                                        left-icon="fa-eye"
                                        type="button"
                                        variant="primary"
                                        @click.left="
                                            () => {
                                                selectedToma = item
                                                showTomaDetailsModal = true
                                                getTomaDetails()
                                            }
                                        "
                                        >Ver detalles
                                    </e-button>
                                </template>
                            </BTable>

                            <b-pagination
                                v-model="tomasFisicasTabController.currentPage"
                                :total-rows="
                                    tomasFisicasTabController.totalRows
                                "
                                :per-page="whInformationPerPage"
                                aria-controls="whpurchase-table"
                                align="center"
                                :limit="10"
                                hide-goto-end-buttons
                                class="paginator"></b-pagination>
                        </b-tab>

                        <b-tab title="Movimientos">
                            <!--


                            MOVIMIENTOS DE BODEGA TAB


                        -->
                            <div class="row display-inline-flex mb-1">
                                <div class="row display-inline-flex mb-1">
                                    <e-button
                                        v-b-toggle.collapse-4
                                        type="button"
                                        variant="primary"
                                        class="col-2 mx-1 col-md-3 col-sm-4"
                                        >Desplegar Búsqueda
                                    </e-button>
                                    <b-collapse id="collapse-4" class="mt-2">
                                        <ECard>
                                            <ValidationForm
                                                v-slot="{ handleReset }"
                                                @submit="
                                                    onSubmit(
                                                        'movements',
                                                        movementTabController
                                                    )
                                                "
                                                :validation-schema="
                                                    movementForm
                                                ">
                                                <div
                                                    class="row"
                                                    align-v="start">
                                                    <div
                                                        class="col-lg-4 col-xl-3 col-sm-6">
                                                        <Datepicker
                                                            v-model="
                                                                movementForm
                                                                    .from_date
                                                                    .value
                                                            "
                                                            :max-date="
                                                                movementForm
                                                                    .to_date
                                                                    ?.value
                                                            "
                                                            show-now-button
                                                            now-button-label="Ahora"
                                                            auto-apply
                                                            close-on-scroll
                                                            textinput
                                                            dark
                                                            teleport-center>
                                                            <template
                                                                #dp-input="{
                                                                    value,
                                                                }">
                                                                <InputText
                                                                    label="Fecha Mínima"
                                                                    :model-value="
                                                                        value
                                                                    "
                                                                    :info-label="
                                                                        movementForm
                                                                            .from_date
                                                                            .errorMessage
                                                                    "
                                                                    :status="
                                                                        Boolean(
                                                                            movementForm
                                                                                .from_date
                                                                                .errorMessage
                                                                        )
                                                                    "
                                                                    info-status="danger" />
                                                            </template>
                                                        </Datepicker>
                                                    </div>
                                                    <div
                                                        class="col-lg-4 col-xl-3 col-sm-6">
                                                        <Datepicker
                                                            v-model="
                                                                movementForm
                                                                    .to_date
                                                                    .value
                                                            "
                                                            :min-date="
                                                                movementForm
                                                                    .from_date
                                                                    ?.value
                                                            "
                                                            show-now-button
                                                            now-button-label="Ahora"
                                                            auto-apply
                                                            close-on-scroll
                                                            textinput
                                                            dark
                                                            teleport-center>
                                                            <template
                                                                #dp-input="{
                                                                    value,
                                                                }">
                                                                <InputText
                                                                    label="Fecha Máxima"
                                                                    :model-value="
                                                                        value
                                                                    "
                                                                    :info-label="
                                                                        movementForm
                                                                            .to_date
                                                                            .errorMessage
                                                                    "
                                                                    :status="
                                                                        Boolean(
                                                                            movementForm
                                                                                .to_date
                                                                                .errorMessage
                                                                        )
                                                                    "
                                                                    info-status="danger" />
                                                            </template>
                                                        </Datepicker>
                                                    </div>
                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <b-form-checkbox
                                                            class="tw-text-xl form-check-input"
                                                            v-model="
                                                                movementForm.entrada
                                                            "
                                                            name="checkbox-3"
                                                            switch>
                                                            Buscar Entradas a
                                                            Bodega
                                                        </b-form-checkbox>
                                                    </div>
                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <b-form-checkbox
                                                            class="tw-text-xl form-check-input"
                                                            v-model="
                                                                movementForm.salida
                                                            "
                                                            name="checkbox-4"
                                                            switch>
                                                            Buscar Salidas de
                                                            Bodega
                                                        </b-form-checkbox>
                                                    </div>
                                                    <div
                                                        class="col-sm-3 col-lg-4 col-xl-2">
                                                        <InputText
                                                            label="Estado"
                                                            v-model="
                                                                movementForm
                                                                    .status
                                                                    .value
                                                            "
                                                            :info-label="
                                                                movementForm
                                                                    .status
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    movementForm
                                                                        .status
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div
                                                        class="col-lg-6 col-xl-3 col-sm-12 mt-auto">
                                                        <InputText
                                                            label="Notas"
                                                            v-model="
                                                                movementForm
                                                                    .notes.value
                                                            "
                                                            :info-label="
                                                                movementForm
                                                                    .notes
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    movementForm
                                                                        .notes
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>
                                                    <div
                                                        class="col-lg-6 col-xl-3 col-sm-12 mt-auto">
                                                        <InputText
                                                            label="Nombre de Bodega Relacionada"
                                                            v-model="
                                                                movementForm
                                                                    .warehouse_name
                                                                    .value
                                                            "
                                                            :info-label="
                                                                movementForm
                                                                    .warehouse_name
                                                                    .errorMessage
                                                            "
                                                            :status="
                                                                Boolean(
                                                                    movementForm
                                                                        .warehouse_name
                                                                        .errorMessage
                                                                )
                                                            "
                                                            info-status="danger" />
                                                    </div>
                                                    <div
                                                        class="col-2 mt-4 text-center">
                                                        <EButton class="">
                                                            Confirmar Búsqueda
                                                        </EButton>
                                                    </div>

                                                    <div
                                                        class="col-2 col-md-3 col-sm-4 mt-4">
                                                        <e-button
                                                            @click.left="
                                                                () => {
                                                                    onReset(
                                                                        movementTabController,
                                                                        'movements'
                                                                    )
                                                                    handleReset()
                                                                }
                                                            "
                                                            type="button"
                                                            variant="primary">
                                                            Limpiar Búsqueda
                                                        </e-button>
                                                    </div>
                                                </div>
                                            </ValidationForm>
                                        </ECard>
                                    </b-collapse>
                                </div>
                            </div>

                            <BTable
                                outline
                                :fields="movementsFields"
                                :items="activeWhInformation.movements">
                                <template #cell(#)="{ index }">
                                    {{
                                        index +
                                        1 +
                                        (movementTabController.currentPage -
                                            1) *
                                            whInformationPerPage
                                    }}
                                </template>

                                <template #cell(Creada)="{ item }">
                                    {{ truncate(item.created_at, 10, '') }}
                                </template>
                                <template #cell(RealizadaPor)="{ item }">
                                    {{
                                        item.created_by.name +
                                        ' ' +
                                        item.created_by.lastname
                                    }}
                                </template>
                                <template #cell(BodegaRelacionada)="{ item }">
                                    {{
                                        item.warehouse_destiny.id ==
                                        activeWhInformation.bodega.id
                                            ? item.warehouse_origin.name
                                            : item.warehouse_destiny.name
                                    }}
                                </template>
                                <template #cell(TipoDeMovimiento)="{ item }">
                                    {{
                                        item.warehouse_destiny.id ==
                                        activeWhInformation.bodega.id
                                            ? 'Salida'
                                            : 'Entrada'
                                    }}
                                </template>
                                <template #cell(Notas)="{ item }">
                                    {{ truncate(item.notes, 10, '...') }}
                                </template>
                                <template #cell(Acciones)="{}">
                                    <e-button
                                        left-icon="fa-eye"
                                        type="button"
                                        variant="primary"
                                        >Ver detalles
                                    </e-button>
                                </template>
                            </BTable>

                            <b-pagination
                                v-model="movementTabController.currentPage"
                                :total-rows="movementTabController.totalRows"
                                :per-page="whInformationPerPage"
                                aria-controls="whpurchase-table"
                                align="center"
                                :limit="10"
                                hide-goto-end-buttons
                                class="paginator"></b-pagination>
                        </b-tab>
                    </b-tabs>
                </div>
            </div>
        </ECard>
    </WaitOverlay>
</template>
<style lang="scss">
    h1.title {
        @apply tw-text-2xl tw-text-black dark:tw-text-neutral-100;
    }

    .smaller-btn-group {
        --bs-list-group-border-width: 1px;
        --bs-list-group-border-radius: 0.25rem;
        --bs-list-group-item-padding-x: 0.8rem;
        --bs-list-group-item-padding-y: 0.3rem;
    }

    .dark-mode-text {
        @apply dark:tw-text-white tw-text-secondary-dark;
    }

    .table {
        > thead {
            @apply tw-bg-secondary tw-text-white tw-font-bold tw-text-sm;
        }

        > tbody {
            @apply tw-text-sm;
        }

        @media (prefers-color-scheme: dark) {
            color: white !important;
            --bs-table-striped-color: theme(colors.zinc.400);
            --bs-table-hover-color: theme('colors.primary.light');
            --bs-table-hover-bg: theme(colors.primary.light / 15%);
        }
    }
</style>
