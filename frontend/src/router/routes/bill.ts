export const bill: Array<RouteConfig> = [
    {
        path: '/facturacion',
        name: 'bill-management-panel',
        component: () => import('@views/BillView.vue'),
        meta: {
            pageTitle: 'Facturas',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Facturación' }],
        },
    },
    {
        path: '/facturacion/agregar',
        name: 'addbill-panel',
        component: () => import('@views/AddBillView.vue'),
        meta: {
            pageTitle: 'Facturas',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Facturacion', href: '/facturacion' }],
        },
    },
]
