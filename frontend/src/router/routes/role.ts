import type RouteConfig from '../RouteConfig'

export const role: Array<RouteConfig> = [
    {
        path: '/role',
        name: 'role-panel',
        component: () =>
            import('@views/RoleView.vue'),
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
