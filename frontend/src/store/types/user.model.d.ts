import type { date } from "yup"

export interface Role {
    id: number
    name: string
    codename: string
    role_class: string
}

export interface Permission {
    name: string
    codename: string
}

/**
 * A complete user with all parsed things and with support of the
 * simple user, aka only id references
 */
export interface User {
    id?: string
    username: string
    email: string
    employee: Employee
    group: number
    created_at: string
}
/**
 * A model of an User without all the `parsed` things, only with minimal information
 * aka: id's
 */
export interface SimpleUser {
    id?: number
    username: string
    email: string
    employee: number
    group: number
    is_active?: boolean
}

export type SimpleUserForm = {
    username: string
    email: string
    employee: number
    group: number
    password: string
    password_confirm: string
}

/**
 * A user class used for forms, all values are optional, but useful
 * for sending request and type-safety
 */
export type UserForm = {
    username?: string
    email?: string
    employee?: number
    group?: number
    password?: string
    password_confirm?: string
    is_active?: boolean
}


export interface Employee {
    created_at:string
    name: string
    lastname: string
    cid: string
    role: Maybe<Role>
    is_active: boolean
}

export default {}
