export const employee: Array<RouteConfig> = [
    {
        path: '/usuarios/empleados',
        name: 'employee-management-panel',
        component: () => import('@views/employee/EmployeeView.vue'),
        meta: {
            pageTitle: 'Gestión de Empleados',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Usuarios' }, { text: 'Empleados' }],
        },
    },
    {
        path: '/usuarios/empleado/agregar',
        name: 'addemployee-panel',
        component: () => import('@views/employee/AddEmployeeView.vue'),
        meta: {
            pageTitle: 'Gestión de Empleados',
            permission: 'view_dashboard',
            breadcrumb: [
                { text: 'Usuarios' },
                { text: 'Empleados', href: '/usuarios/empleados' },
            ],
        },
    },
    {
        path: '/usuarios/empleado/editar/:id',
        name: 'editemployee-panel',
        component: () => import('@views/employee/EditEmployeeView.vue'),
        meta: {
            pageTitle: 'Gestión de Empleados',
            permission: 'view_dashboard',
            breadcrumb: [
                { text: 'Usuarios' },
                { text: 'Empleados', href: '/usuarios/empleados' },
            ],
        },
    },
]
