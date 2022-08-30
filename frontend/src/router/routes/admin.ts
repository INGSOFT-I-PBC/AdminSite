export const admin: Array<RouteConfig> = [
    {
        path: '/user/admin',
        name: 'user-admin-panel',
        component: () => import('@views/auth/UserAdminView.vue'),
        meta: {
            pageTitle: 'Configuración',
            permission: 'can_edit_user',
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
        path: '/admin/creacion-usuario',
        name: 'user-creation-view',
        component: () => import('@views/admin/CreacionUsuario.vue'),
        meta: {
            pageTitle: 'Creacion Cuenta Usuario',
        },
    },
]
