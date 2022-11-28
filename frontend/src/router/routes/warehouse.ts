export const warehouses: Array<RouteConfig> = [
    {
        path: '/bodegas/nueva-orden',
        name: 'warehouse-new-order',
        component: () => import('@/views/warehouse/NewOrderView.vue'),
        meta: {
            pageTitle: 'Nueva orden',
            breadcrumb: [
                {
                    text: 'Bodegas',
                    href: '/bodegas',
                },
                {
                    text: 'Nuevo pedido',
                    active: true,
                },
            ],
        },
    },
    {
        path: '/bodegas/tomas-fisicas',
        component: () => import('@views/warehouse/GestionTomasFisicas.vue'),
        name: 'tomas-fisica-view',
        meta: {
            pageTitle: 'Tomas Fisicas',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'inicio' }, { text: 'dashboard' }],
        },
    },

    {
        path: '/bodegas/movimiento-inventario',
        name: 'movimiento-inventario-view',
        component: () => import('@views/warehouse/MovimientosInventario.vue'),
        meta: {
            pageTitle: 'Movimiento Inventario',
        },
    },

    {
        path: '/bodegas/proveedores',
        name: 'proveedores-view',
        component: () => import('@views/warehouse/ProveedoresView.vue'),
        meta: {
            pageTitle: 'Proveedores',
        },
    },

    {
        path: '/bodegas/pedidos',
        name: 'pedidos-view',
        component: () => import('@views/warehouse/GestionPedidos.vue'),
        meta: {
            pageTitle: 'Gestion Pedidos',
        },
    },
    {
        path: '/bodegas/stock/crear/codigo-barra',
        name: 'warehouse-create-stock-barcodes',
        component: () =>
            import('@views/warehouse/barcodes/BarcodeManagementView.vue'),
        meta: {
            permission: 'can_create_barcodes',
            pageTitle: 'Creación de Códigos de Barras',
            breadcrumb: [
                { text: 'Bodega' },
                {
                    text: 'Códigos barras',
                    href: '/bodegas/stock/lectura/codigo-barras',
                },
                { text: 'Crear' },
            ],
        },
    },
    {
        path: '/bodegas/stock/lectura/codigo-barras',
        name: 'warehouse-stock-barcodes',
        component: () => import('@views/warehouse/barcodes/BarcodeViewer.vue'),
        meta: {
            permission: 'can_view_barcodes',
            pageTitle: 'Gestión Código de Barras',
            breadcrumb: [
                { text: 'Bodega' },
                { text: 'Códigos barras', active: true },
            ],
        },
    },
]
