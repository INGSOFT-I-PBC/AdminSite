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
        path: '/bodegas/tomas-fisicas',
        component: () => import('@views/warehouse/GestionTomasFisicas.vue'),
        name: 'tomas-fisica-view',
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
]
