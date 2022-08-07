// vim: set tw=4:sw=4
import {
    createRouter,
    createWebHashHistory,
} from 'vue-router'
import LoginView from '../views/auth/LoginView.vue'
import Error404 from '../views/Error404.vue'
import { admin } from './routes/admin'
import { common } from './routes/common'
import { inventory } from './routes/inventory'
import { purchases } from './routes/purchases'
import { warehouses } from './routes/wharehouse'

const routes = [
    {
        path: '/',
        redirect: '/home',

        children: [
            ...common,
            ...admin,
            ...inventory,
            ...purchases,
            ...warehouses,
        ],
    },
    {
        path: '/login',
        component: LoginView,
        meta: { layout: 'full' },
    },
    {
        path: '/error-404',
        name: 'error-404',
        component: Error404,
        meta: { layout: 'full' },
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/error-404',
    },
]

const router = createRouter({
    //   history: createWebHistory(import.meta.env.BASE_URL),
    history: createWebHashHistory(''),
    routes: routes,
})

export default router
