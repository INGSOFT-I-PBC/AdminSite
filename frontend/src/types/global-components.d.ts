// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import type { DefineComponent } from 'vue'
import Vue3EasyDataTable from 'vue3-easy-data-table'
import type { OlMap } from './components'

declare module '@vue/runtime-core' {
    export interface GlobalComponents {
        EasyDataTable: typeof Vue3EasyDataTable
        FontAwesomeIcon: DefineComponent<FontAwesomeIconProps>
        FontAwesomeLayers: DefineComponent<FontAwesomeLayersProps>
        FontAwesomeLayersText: DefineComponent<FontAwesomeLayersTextProps>
    }
}

export {}
