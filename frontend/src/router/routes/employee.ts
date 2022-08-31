import type RouteConfig from '../RouteConfig'

export const employee: Array<RouteConfig> = [
    {
        path: '/empleado',
        name: 'empleado-panel',
        component: () =>
            import('@views/EmployeeView.vue'),
        meta: {
           pageTitle: 'Gestión de Empleados',
            permission: 'view_dashboard',
            breadcrumb: [
                { text: 'Usuarios' },
                { text: 'Empleados',  href: '/empleado' },
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
            breadcrumb: [
                { text: 'Inventario' },
            ],
        },
    },

     {
        path: '/empleado/agregar',
        name: 'addemployee-panel',
        component: () =>
            import('@views/AddEmployeeView.vue'),
        meta: {
           pageTitle: 'Gestión de Empleados',
            permission: 'view_dashboard',
            breadcrumb: [
                { text: 'Usuarios' },
                { text: 'Empleados',  href: '/empleado'},
            ],
        },

    },

    {
        path: '/empleado/ver',
        name: 'veremployee-panel',
        component: () =>
            import('@views/VerEmployeeView.vue'),
        meta: {
           pageTitle: 'Gestión de Empleados',
            permission: 'view_dashboard',
            breadcrumb: [
                { text: 'Usuarios' },
                { text: 'Empleados',  href: '/empleado'},
            ],
        },
    }, 
]