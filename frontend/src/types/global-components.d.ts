// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import Vue3EasyDataTable from 'vue3-easy-data-table'

declare module '@vue/runtime-core' {
    export interface GlobalComponents {
        EasyDataTable: typeof Vue3EasyDataTable
    }
}

export {}
