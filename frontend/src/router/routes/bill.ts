export const bill: Array<RouteConfig> = [
    {
        path: '/facturacion',
        name: 'bill-management-panel',
        component: () => import('@views/invoice/BillView.vue'),
        meta: {
            pageTitle: 'Facturas',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Facturación' }],
        },
    },
    {
        path: '/facturacion/agregar',
        name: 'addbill-panel',
        component: () => import('@views/invoice/AddBillView.vue'),
        meta: {
            pageTitle: 'Facturas',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Facturacion', href: '/facturacion' }],
        },
    },
    {
        path: '/facturacion/notascredito',
        name: 'viewnotescredit-panel',
        component: () => import('@views/creditnote/CreditNotes.vue'),
        meta: {
            pageTitle: 'Notas de crédito',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Facturacion', href: '/facturacion' }],
        },
    },
    {
        path: '/facturacion/editar/:id',
        name: 'editbill-panel',
        component: () => import('@views/invoice/EditBillView.vue'),
        meta: {
            pageTitle: 'Facturas',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Facturacion', href: '/facturacion' }],
        },
    },
    {
        path: '/facturacion/cancel/:id',
        name: 'cancelbill-panel',
        component: () => import('@views/creditnote/CancelBillView.vue'),
        meta: {
            pageTitle: 'Facturas',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Facturacion', href: '/facturacion' }],
        },
    },
]
