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
        component: () => import('@/views/Error404.vue'),
        meta: {
            breadcrumb: [{ text: 'Compras' }, { text: 'Proveedores' }],
            pageTitle: 'Proveedores',
        },
    },
]
