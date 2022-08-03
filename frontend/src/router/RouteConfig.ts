/**
 * This type contains the configuration of a route with the needed data
 * and other additions
 */
type RouteConfig = {
    path: string
    name?: string
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    component: any
    meta: RouteMetaData
}

/**
 * This is the metadata of the route, contains information that would
 * be injected while rendering
 */
type RouteMetaData = {
    permission?: string
    pageTitle: string
    breadcrumb?: Array<RouteBreadcrumb>
}

/**
 * This is the route breadcrumb only used for decoration on the main view
 */
type RouteBreadcrumb = {
    text: string
    active?: boolean
}

export default RouteConfig
