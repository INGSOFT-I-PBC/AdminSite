import type { RouteRecordRaw } from 'vue-router'

/* eslint no-var: 0 */
declare global {
    type Optional<T> = T | undefined | null

    /**
     * A item used by default or base on the component
     * `ListBox`
     * @see Listbox
     */
    interface _ListboxItem {
        label: string
        value: string
    }

    type ListboxItem = _ListboxItem | MapObj

    var ref: typeof import('vue')['ref']
    /// eslint-disable no-var
    var router: typeof import('@store')

    export interface MenuItem {
        readonly id?: string
        readonly label: string
        readonly path?: string
        readonly icon?: Optional<string>
        readonly children?: Optional<MenuItem[]>
        readonly forceRender?: boolean
        readonly routeName?: string
    }

    type MapObj<T> = { [key: string]: T }

    /********************************
     *  Store Types or model types  *
     ********************************/
    export interface JWTAccessToken {
        accessToken: string
    }
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

    type RouteMetaData = {
        permission?: string
        pageTitle: string
        layout?: string
        breadcrumb?: RouteBreadcrumb[]
    }

    type _RouteMeta = {
        meta: RouteMetaData
    }
    /**
     * This type contains the configuration of a route with the needed data
     * and other additions
     */
    type RouteConfig = _RouteMeta & Omit<RouteRecordRaw, 'meta'>

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
