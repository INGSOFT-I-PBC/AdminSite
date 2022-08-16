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
    role: string
    permissions: string[]
}
