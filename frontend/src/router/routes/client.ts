export const client: Array<RouteConfig> = [
    {
        path: '/usuarios/clientes',
        name: 'client-management-panel',
        component: () => import('@views/ClientView.vue'),
        meta: {
            pageTitle: 'Gestión de Clientes',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Usuarios' }, { text: 'Clientes' }],
        },
    },
    {
        path: '/usuarios/cliente/agregar',
        name: 'addclient-panel',
        component: () => import('@views/AddClientView.vue'),
        meta: {
            pageTitle: 'Gestión de Clientes',
            permission: 'view_dashboard',
            breadcrumb: [
                { text: 'Usuarios' },
                { text: 'Clientes', href: '/usuarios/clientes' },
            ],
        },
    },
]
