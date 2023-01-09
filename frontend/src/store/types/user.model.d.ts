import type { Gender } from './client.model'
import type { Group } from './common.model'

export interface Role {
    id?: number | string
    name: string
    codename: string
    role_class: string
    created_at?: string
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

export interface FullUser {
    id: number
    username: string
    email: string
    group: Group
    employee: Employee
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

export interface RawUser extends SimpleUser {
    id: number
    is_active: boolean
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
    id?: number
    created_at?: string
    updated_at?: string
    deleted_at?: string
    name: string
    lastname: string
    cid: string
    is_active: boolean
    role: Maybe<Role> | undefined
    phone_number: string
    created_by: Maybe<Employee> | null
    gender: Maybe<Gender> | undefined
    address: string | null
}

export interface EmployeeForm {
    name: string
    lastname: string
    cid: string
    is_active: boolean
    role: Maybe<Role> | undefined | number
    phone_number: string
    created_by?: Maybe<Employee> | null | number
    gender: Maybe<Gender> | undefined | number
    address: string | null
}

export default {}
