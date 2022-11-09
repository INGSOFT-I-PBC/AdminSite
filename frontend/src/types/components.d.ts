import type { Component, DefineComponent } from 'vue'

export type OlMap = DefineComponent<{
    a: string
}>

declare module '*.vue' {
    import { type DefineComponent } from 'vue'

    import { type Router } from 'vue-router'

    /**
     * The Item type for the ListBox component
     */
    export type ListboxItem = {
        label: string
        value: string
    }
    const router: Router
    /**
     * The component definition for the ListBox component
     */
    export const ListBox: DefineComponent<
        {
            modelValue: unknown
            /** The `model` property used to show the object on UI */
            label: string
            options: Array<ListboxItem | string | MapObj<unknown>>
        },
        Record<string, unknown>,
        Component
    >
}

export default {}
