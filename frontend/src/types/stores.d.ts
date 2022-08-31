declare module '@store/*' {
    /* Here go the definitions for model types that are received on
     * every request to the backend
     */

    declare class JWTResponse {
        accessToken: string
        refreshToken: string
    }
}

declare module '*.vue' {}

export {}
