import type ListBoxVue from '@/components/custom/ListBox.vue'
import type { Component, Ref } from 'vue'

declare module '*.vue' {
    import { type DefineComponent } from 'vue'

    import { type Router } from 'vue-router'

    export type Testingaaaa = {
        a: string
    }
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
            modelValue: any
            /** The `model` property used to show the object on UI */
            label: string
            options: Array<ListboxItem | string | any>
        },
        {},
        Component
    >
}

declare module '@vue/runtime-core' {
    export interface GlobalComponents {
        RouterLink: typeof import('vue-router')['RouterLink']
        RouterView: typeof import('vue-router')['RouterView']
        VueFeather: typeof import('vue-feather')['default']
        FontAwesomeIcon: typeof import('@fortawesome/vue-fontawesome')['FontAwesomeIcon']
        ECard: typeof import('@components/custom/ECard.vue')['default']
        Table: typeof import('@components/holders/Table.vue')['default']
    }
}

export {}
