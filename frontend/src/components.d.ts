import type {
    FontAwesomeIconProps,
    FontAwesomeLayersProps,
} from '@fortawesome/vue-fontawesome'
import '@vue/runtime-core'

declare module '@vue/runtime-core' {
    export interface GlobalComponents {
        EasyDataTable: DefineComponent<Vue3EasyDataTable>
        VueFeather: typeof import('vue-feather').default
        FontAwesomeIcon: DefineComponent<
            Partial<FontAwesomeIconProps> & {
                icon: object | Array<string> | string | IconDefinition
            }
        >
        FontAwesomeLayers: DefineComponent<Partial<FontAwesomeLayersProps>>
        FontAwesomeLayersText: DefineComponent<Partial<FontAwesomeLayersProps>>
        VeeForm: typeof import('vee-validate')['Form']
        VeeField: typeof import('vee-validate')['Field']
        VeeFieldArray: typeof import('vee-validate')['FieldArray']
    }
}
export {}
