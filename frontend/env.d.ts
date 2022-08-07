/// <reference types="vite/client" />

declare module '*.vue' {
    import type { DefineComponent } from 'vue'
    // eslint-disable-next-line @typescript-eslint/ban-types, @typescript-eslint/no-explicit-any
    const component: DefineComponent<{}, {}, any>
    export default component
}

declare module '@custom-components' {
    import index from 'src/components/custom/index'
    export default { ...index }
}
