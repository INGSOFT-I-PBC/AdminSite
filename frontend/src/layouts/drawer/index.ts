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
                label: 'Usuarios',
                routeName: 'admin-user-management',
                path: '/admin/usuarios',
            },
            {
                label: 'Permisos',
                routeName: 'admin-permission-manager',
                path: '/admin/permisos',
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
                label: 'Pedidos',
                children: [
                    {
                        label: 'Gestión pedidos',
                        path: '/bodegas/pedidos',
                        routeName: 'pedidos-view',
                    },
                    {
                        label: 'Solicitar Pedido',
                        path: '/bodegas/nueva-orden',
                        routeName: 'warehouse-new-order',
                    },
                ],
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
        children: [
            {
                label: 'Proveedores',
                children: [
                    {
                        label: 'Nuevo Proveedor',
                        path: '/compras/nuevo-proveedor',
                        routeName: 'purchases-add-provider',
                    },
                    {
                        // TODO: make this view
                        label: 'Gestionar',
                        path: '/compras/proveedores',
                        routeName: 'purchases-manage-providers',
                    },
                ],
            },
        ],
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
