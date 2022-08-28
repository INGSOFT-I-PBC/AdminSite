import type RouteConfig from '../RouteConfig'

export const role: Array<RouteConfig> = [
    {
        path: '/role',
        name: 'role-panel',
        component: () => import('@views/RoleView.vue'),
        meta: {
            pageTitle: 'Roles',
            permission: 'view_dashboard',
            breadcrumb: [
                { text: 'Usuarios'},
                { text: 'Empleados' , href: '/empleado',},
                { text: 'Roles',  },
            ],
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
]
