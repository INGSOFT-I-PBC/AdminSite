export const menus: MenuItem[] = [

    {
        label: 'Principal',
        path: '/home',
        icon: 'home',
        forceRender: true,
    },
    {
        label: 'Dashboard',
        path: '/dashboard',
        icon: 'bar-chart-2',
        forceRender: true,
    },
    {
        label: 'Usuarios',
        icon: 'users',
        children: [
            {
                label: 'Empleados',
                path: '/employee',

            },
            {
                label: 'Clientes',
                path: '/',

            },

        ],
    },
    {
        label: 'Administración',
        icon: 'terminal',
        children: [
            {
                label: 'Frontend',
                children: [
                    {
                        label: 'Components',
                        path: '/admin/testing-components',
                    },
                ],
            },
        ],
    },
    {
        label: 'Bodegas',
        icon: 'package',
        children: [
            {
                label: 'Gestión',
                path: '/',
            },
            {
                label: 'Solcitar Pedido',
                path: '/bodegas/nueva-orden',
            },
            {
                label: 'Visualizar Movimientos',
                path: '',
            },
        ],
    },
    {
        label: 'Inventario',
        icon: 'archive',
        children: [],
    },
    {
        label: 'Compras',
        icon: 'shopping-bag',
        children: [],
    },
]
