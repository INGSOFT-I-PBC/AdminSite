export const role: Array<RouteConfig> = [
    {
        path: '/admin/roles',
        name: 'role-panel',
        component: () => import('@views/employee/RoleView.vue'),
        meta: {
            pageTitle: 'Roles',
            permission: 'view_dashboard',
            breadcrumb: [
                { text: 'Usuarios' },
                { text: 'Empleados', href: '/usuarios/empleados' },
                { text: 'Roles' },
            ],
        },
    },
]
