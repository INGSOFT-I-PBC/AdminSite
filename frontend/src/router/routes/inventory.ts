import type RouteConfig from '../RouteConfig'

export const inventory: Array<RouteConfig> = [
    {
        path: '/inventory',
        name: 'inventory-panel',
        component: () =>
            import('@views/InventoryView.vue'),
        meta: {
            pageTitle: 'Configuración',
            permission: 'can_edit_user',
        },
    },
    {
        path: '/user/reset-password',
        name: 'user-change-password',
        component: () =>
            import(
                '@views/auth/ResetPasswordView.vue'
            ),
        meta: {
            pageTitle: 'Configuración de usuario',
            permission: 'can_edit_password',
        },
    },
]
