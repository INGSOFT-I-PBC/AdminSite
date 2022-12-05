export const closebox: Array<RouteConfig> = [
    {
        path: '/close-box',
        name: 'close-box',
        component: () => import('@views/invoice/CloseBox.vue'),
        meta: {
            pageTitle: 'Cierre de caja',
            permission: 'view_dashboard',
            breadcrumb: [{ text: 'Cierre de caja' }],
        },
    },
]
