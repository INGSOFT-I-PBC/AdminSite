export const menus: MenuItem[] = [
    {
        label: 'Principal',
        path: '/home',
        icon: 'home',
        routeName: 'home-view',
        forceRender: true,
    },
    {
        label: 'Dashboard',
        path: '/dashboard',
        icon: 'bar-chart-2',
        routeName: 'dashboard-view',
        forceRender: true,
    },
    {
        label: 'Usuarios',
        icon: 'users',
        children: [
            {
                label: 'Empleados',
                path: '/usuarios/empleados',
                routeName: 'employee-management-panel',
            },
            {
                label: 'Clientes',
                path: '/usuarios/clientes',
                routeName: 'client-management-panel',
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
                        routeName: 'components-testing',
                    },
                ],
            },
            {
                label: 'Roles',
                path: '/admin/roles',
                routeName: 'role-panel',
            },
        ],
    },
    {
        label: 'Bodegas',
        icon: 'package',
        children: [
            {
                label: 'Gestión pedidos',
                path: '/bodegas/pedidos',
                routeName: 'pedidos-view',
            },
            {
                label: 'Solcitar Pedido',
                path: '/bodegas/nueva-orden',
                routeName: 'warehouse-new-order',
            },
            {
                label: 'Tomas físicas',
                path: '/bodegas/tomas-fisicas',
                routeName: 'tomas-fisica-view',
            },
            {
                label: 'Visualizar Movimientos',
                path: '/bodegas/movimiento-inventario',
                routeName: 'movimiento-inventario-view',
            },
            {
                label: 'Proveedores',
                path: '/bodegas/proveedores',
                routeName: 'proveedores-view',
            },
        ],
    },
    {
        label: 'Inventario',
        icon: 'archive',
        children: [
            {
                label: 'Administración',
                path: '/inventario',
                routeName: 'inventory-panel',
            },
        ],
    },
    {
        label: 'Compras',
        icon: 'shopping-bag',
        children: [],
    },
    {
        label: 'Facturación',
        icon: 'clipboard',
        children: [],
        path: '/facturacion',
    },
    {
        id: 'logout',
        label: 'Cerrar Sesión',
        forceRender: true,
        icon: 'log-out',
    },
   
]
