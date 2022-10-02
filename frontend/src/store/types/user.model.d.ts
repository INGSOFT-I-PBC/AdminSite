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

export interface User {
    id: string
    username: string
    email: string
    employee: Maybe<Employee>
    created_at: string
}

export interface Employee {
    name: string
    lastname: string
    cid: string
    role: Maybe<Role>
}

export default {}
