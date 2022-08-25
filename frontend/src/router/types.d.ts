import type {
    NavigationGuard,
    NavigationGuardNext,
    RouteLocationNormalized,
    Router,
} from 'vue-router'

export type RouterContext = {
    to: RouteLocationNormalized
    from: RouteLocationNormalized
    next: NavigationGuardNext
    router: Router
}

export type Middleware = (
    context: RouterContext
) => NavigationGuardNext | NavigationGuard

export function defineMiddleware(setup: (context: RouterContext) => void) {
    return setup
}
