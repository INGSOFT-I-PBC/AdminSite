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
                    href: '/bodegas/gestion',
                },
                {
                    text: 'Nuevo pedido',
                    active: true,
                },
            ],
        },
    },
    {
        path: '/bodegas/tomas-fisicas/:id?',
        component: () => import('@views/warehouse/GestionTomasFisicas.vue'),
        name: 'tomas-fisica-view',
        props: true,
        meta: {
            pageTitle: 'Tomas Físicas',
            breadcrumb: [
                {
                    text: 'Bodegas',
                    href: '/bodegas/gestion',
                },
                {
                    text: 'Nueva Toma',
                    active: true,
                },
            ],
        },
    },

    {
        path: '/bodegas/movimiento-inventario',
        name: 'movimiento-inventario-view',
        component: () => import('@views/warehouse/MovimientosInventario.vue'),
        meta: {
            pageTitle: 'Movimientos de Bodega',
            breadcrumb: [
                {
                    text: 'Bodegas',
                    href: '/bodegas/gestion',
                },
                {
                    text: 'Movimientos',
                    active: true,
                },
            ],
        },
    },

    {
        path: '/bodegas/nuevo-movimiento',
        name: 'warehouse-new-movement',
        component: () => import('@views/warehouse/NewMovimiento.vue'),
        meta: {
            pageTitle: 'Nuevo Movimiento',
            breadcrumb: [
                {
                    text: 'Bodegas',
                    href: '/bodegas/gestion',
                },
                {
                    text: 'Nuevo Movimiento',
                    active: true,
                },
            ],
        },
    },

    {
        path: '/bodegas/pedidos/:id?',
        name: 'pedidos-view',
        props: true,
        component: () => import('@views/purchase/GestionPedidos.vue'),
        meta: {
            pageTitle: 'Gestión Pedidos',
        },
    },
    {
        path: '/bodegas/gestion',
        name: 'gestion-view',
        component: () => import('@views/warehouse/GestionBodegas.vue'),
        meta: {
            pageTitle: 'Gestión de Bodegas',
            breadcrumb: [
                {
                    text: 'Bodegas',
                    href: '/bodegas',
                },
            ],
        },
    },
    {
        path: '/bodegas/mantenimiento/inventario',
        name: 'warehouse-management-inventory',
        component: () => import('@views/warehouse/ManageInventoryView.vue'),
        meta: {
            pageTitle: 'Gestor de inventario por bodega',
            permission: 'can_manage_warehouse_inventory',
            breadcrumb: [
                { text: 'Bodegas' },
                { text: 'Mantenimiento' },
                { text: 'Inventario' },
            ],
        },
    },
    {
        path: '/bodegas/impresion-etiquetas',
        name: 'warehouse-tag-print',
        component: () => import('@views/warehouse/TagPrintingView.vue'),
        meta: {
            pageTitle: 'Impresión de etiquetas',
            permission: 'can_print_tags',
            breadcrumb: [
                { text: 'Bodegas' },
                { text: 'Impresión de etiquetas' },
            ],
        },
    },
]
