import type { RouteMetaData } from '@/router/RouteConfig'
import type { DefineComponent } from 'vue'
import type { RouteRecordRaw } from 'vue-router'

/* eslint no-var: 0 */
declare global {
    type Optional<T> = T | undefined | null

    /**
     * A item used by default or base on the component
     * `ListBox`
     * @see Listbox
     */
    interface ListboxItem {
        label: string
        value: string
    }

    var ref: typeof import('vue')['ref']
    /// eslint-disable no-var
    var router: typeof import('@store')

    export interface MenuItem {
        readonly label: string
        readonly path?: string
        readonly icon?: Optional<string>
        readonly children?: Optional<MenuItem[]>
        readonly forceRender?: boolean
        readonly routeName?: string
    }

    /********************************
     *  Store Types or model types  *
     ********************************/
    /**
     * The definition of response type for:
     * JWT authentication
     */
    export interface JWTToken {
        accessToken: string
        refreshToken: string
    }
    /**
     * This is the type of a user that is returned from the Backend
     */
    export interface UserInfo {
        name: string
        username: string
        role: string
        permissions: string[]
    }
    /**
     * The state of the Authorization
     */
    export interface AuthState {
        jwtData: JWTToken | null
        userData: UserInfo | null
    }

    type _RouteMeta = {
        meta: RouteMetaData
    }
    /**
     * This type contains the configuration of a route with the needed data
     * and other additions
     */
    type RouteConfig = RouteRecordRaw & _RouteMeta

    /**
     * This is the route breadcrumb only used for decoration on the main view
     */
    export type RouteBreadcrumb = {
        text: string
        active?: boolean
        href?: string
    }
}



export {}
