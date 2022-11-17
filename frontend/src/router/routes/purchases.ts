export const purchases: Array<RouteConfig> = [
    {
        name: 'purchase-add-provider',
        path: '/compras/nuevo-proveedor',
        component: () => import('@/views/purchase/AddNewProvider.vue'),
        meta: {
            breadcrumb: [{ text: 'compras' }, { text: 'nuevo proveedor' }],
            pageTitle: 'Crear nuevo proveedor',
        },
    },
    {
        name: 'purchase-manage-providers',
        path: '/compras/proveedores',
        component: () => import('@/views/purchase/ManageProviders.vue'),
        meta: {
            breadcrumb: [{ text: 'Compras' }, { text: 'Proveedores' }],
            pageTitle: 'Proveedores',
        },
    },
    {
        name: 'purchase-approval-orders',
        path: '/compras/aprobacion-ordenes-compra',
        component: () => import('@views/purchase/OrderApprovalView.vue'),
        meta: {
            breadcrumb: [
                { text: 'Compras' },
                { text: 'ordenes de compras' },
                { text: 'aprobación' },
            ],
            pageTitle: 'Aprobación de Órdenes de compra',
        },
    },
]
