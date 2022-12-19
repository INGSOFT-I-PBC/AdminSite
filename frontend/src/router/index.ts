// vim: set tw=4:sw=4
import { useAuthStore } from '@/store/auth'

import {
    type RouteRecordRaw,
    createRouter,
    createWebHashHistory,
} from 'vue-router'

import Error403 from '../views/Error403.vue'
import Error404 from '../views/Error404.vue'
import LoginView from '../views/auth/LoginView.vue'
import { admin } from './routes/admin'
import { bill } from './routes/bill'
import { client } from './routes/client'
import { closebox } from './routes/closebox'
import { common } from './routes/common'
import { employee } from './routes/employee'
import { inventory } from './routes/inventory'
import { purchases } from './routes/purchases'
import { role } from './routes/role'
import { warehouses } from './routes/warehouse'

const routes = [
    {
        path: '/',
        meta: {
            isAuthenticated: true,
        },
        redirect: '/home',
        children: [
            ...common,
            ...admin,
            ...inventory,
            ...purchases,
            ...warehouses,
            ...employee,
            ...role,
            ...client,
            ...bill,
            ...closebox,
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
        path: '/error-403',
        name: 'error-403',
        component: Error403,
        meta: { layout: 'full' },
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/error-404',
    },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes: routes as RouteRecordRaw[],
})

router.beforeEach(async (to, from, next) => {
    if (to.meta.isAuthenticated) {
        const authStore = useAuthStore()
        authStore.refreshToken().catch(err => {
            console.error(err)
            router.push({ path: '/login' })
        })
    }
    next()
})

export default router
