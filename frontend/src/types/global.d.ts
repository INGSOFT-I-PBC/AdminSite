import type { Employee } from '@store/types'

import type { RouteRecordRaw } from 'vue-router'

/* eslint no-var: 0 */
declare global {
    type Optional<T> = T | null
    type Nullable<T> = Optional<T>
    type Nullish = null | undefined
    type Maybe<T> = T | undefined

    type TypeChecker<T> = (arg0: T) => arg0 is T

    //type Functor<I, O> = (I) => O

    type Mapper<T> = (T) => T

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
    var computed: typeof import('vue')['computed']

    /**
     * Checks if the given value is defined.
     *
     * @param value The value to check
     */
    function undef(value?: any): value is undefined

    function defined<T = any>(value?: T): value is T

    /// eslint-disable no-var
    var router: typeof import('@store')

    export interface MenuItem {
        readonly id?: string
        readonly label: string
        readonly path?: string
        readonly icon?: Optional<string>
        children?: Optional<MenuItem[]>
        readonly forceRender?: boolean
        readonly routeName?: string
    }

    type MapObj<T> = { [key: string]: T }

    /********************************
     *  Store Types or model types  *
     ********************************/
    export interface JWTAccessToken {
        access: string
    }

    /**
     * The definition of response type for:
     * JWT authentication
     */
    export interface JWTToken {
        access: string
        refresh: string
    }

    /**
     * This is the type of a user that is returned from the Backend
     */
    export interface UserInfo {
        employee: number | Employee
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
    export interface Auth {
        token: string | null
        isAuthenticated: boolean | null
    }

    export type PaginationOptions = {
        per_page?: number
        page: number
        buscar?: string
    }
}

export {}
