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
        path: '/admin/usuarios',
        name: 'admin-user-mangement',
        component: () => import('@views/admin/users/UserManagementView.vue'),
        meta: {
            pageTitle: 'Administrador de usuarios',
            permission: 'can_manage_user',
        },
    },
    {
        path: '/admin/permisos',
        name: 'admin-permission-manager',
        component: () => import('@views/admin/PermissionManager.vue'),
        meta: {
            pageTitle: 'Administrador de permisos',
            permission: 'can_manage_permissions',
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
