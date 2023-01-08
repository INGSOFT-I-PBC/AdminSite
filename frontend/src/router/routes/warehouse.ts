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
        name: 'new-movimiento-view',
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
]
