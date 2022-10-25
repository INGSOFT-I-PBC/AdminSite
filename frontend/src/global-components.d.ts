declare module '@vue/runtime-core' {
    export interface GlobalComponents {
        RouterLink: typeof import('vue-router')['RouterLink']
        RouterView: typeof import('vue-router')['RouterView']
        FontAwesomeIcon: DefineComponent<FontAwesomeIconProps>
        FontAwesomeLayers: DefineComponent<FontAwesomeLayersProps>
        FontAwesomeLayersText: DefineComponent<FontAwesomeLayersTextProps>
    }
}

export {}
