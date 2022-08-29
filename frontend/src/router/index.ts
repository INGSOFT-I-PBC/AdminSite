// vim: set tw=4:sw=4
import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router'
import LoginView from '../views/auth/LoginView.vue'
import Error404 from '../views/Error404.vue'
import Error403 from '../views/Error403.vue'
import { admin } from './routes/admin'
import { common } from './routes/common'
import { inventory } from './routes/inventory'
import { purchases } from './routes/purchases'
import { warehouses } from './routes/warehouse'
import { employee } from './routes/employee'
import { role } from './routes/role'

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        redirect: '/home',
        children: [
            ...common,
            ...admin,
            ...inventory,
            ...purchases,
            ...warehouses,
            ...employee,
            ...role,
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
    routes: routes,
})

/**
router.beforeEach(async (to, from, next) => {
    const auth = useAuthStore()
    const loggedIn = await auth.isAuthenticated()
    if (!loggedIn) return next({ path: '/login' })
    if (to.path === '/login') {
        if (loggedIn) return next({ path: '/' })
        return next(from)
    }
    const targetMeta = from.meta as RouteMetaData
    return next()
})*/

export default router
