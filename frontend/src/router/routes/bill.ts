export const bill: Array<RouteConfig> = [
    {
        path: '/facturacion',
        name: 'bill-management-panel',
        component: () => import('@views/billing/BillView.vue'),
        meta: {
            pageTitle: 'Facturas',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Facturación' }],
        },
    },
    {
        path: '/facturacion/agregar',
        name: 'addbill-panel',
        component: () => import('@views/billing/AddBillView.vue'),
        meta: {
            pageTitle: 'Facturas',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Facturacion', href: '/facturacion' }],
        },
    },
]
