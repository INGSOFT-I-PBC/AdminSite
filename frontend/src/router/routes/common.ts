import type RouteConfig from '../RouteConfig'

export const common: Array<RouteConfig> = [
    {
        path: '/home',
        name: 'home-view',
        component: () =>
            import('@views/HomeView.vue'),
        meta: {
            pageTitle: 'Inicio',
        },
    },
    {
        path: '/dashboard',
        component: () =>
            import('@views/DashboardView.vue'),
        name: 'dashboard-view',
        meta: {
            pageTitle: 'Dashboard General',
            permission: 'view_dashboard',
            breadcrumb: [
                { text: 'inicio' },
                { text: 'dashboard' },
            ],
        },
    },
]
