export const employee: Array<RouteConfig> = [
    {
        path: '/usuarios/empleados',
        name: 'employee-management-panel',
        component: () => import('@views/EmployeeView.vue'),
        meta: {
            pageTitle: 'Gestión de Empleados',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Usuarios' }, { text: 'Empleados' }],
        },
    },
    {
        path: '/usuarios/empleado/agregar',
        name: 'addemployee-panel',
        component: () => import('@views/AddEmployeeView.vue'),
        meta: {
            pageTitle: 'Gestión de Empleados',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Usuarios' }, { text: 'Empleados' }],
        },
    },
]
