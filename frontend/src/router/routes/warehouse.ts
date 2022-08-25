import type RouteConfig from '../RouteConfig'

export const warehouses: Array<RouteConfig> = [
    {
        path: '/bodegas/nueva-orden',
        name: 'warehouse-new-order',
        component: () =>
            import(
                '@/views/warehouse/NewOrderView.vue'
            ),
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
]
