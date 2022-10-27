export const inventory: Array<RouteConfig> = [
    {
        path: '/inventario',
        name: 'inventory-panel',
        component: () => import('@/views/inventory/InventoryView.vue'),
        meta: {
            pageTitle: 'Inventario',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Inventario' }],
        },
    },
    {
        path: '/user/reset-password',
        name: 'user-change-password',
        component: () => import('@views/auth/ResetPasswordView.vue'),
        meta: {
            pageTitle: 'Configuración de usuario',
            permission: 'can_edit_password',
        },
    },
    {
        path: '/inventario/agregar',
        name: 'addinventario-panel',
        component: () => import('@/views/inventory/AddProductView.vue'),
        meta: {
            pageTitle: 'Inventario',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Inventario', href: '/inventario' }],
        },
    },
    {
        path: '/inventario/editar/:id',
        name: 'editinventario-panel',
        component: () => import('@/views/inventory/EditProductView.vue'),
        meta: {
            pageTitle: 'Inventario',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Inventario', href: '/inventario' }],
        },
    },
]
