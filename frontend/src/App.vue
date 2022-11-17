<script lang="ts" setup>
    import { computed, defineAsyncComponent, provide } from 'vue'
    import { RouterView, useRoute } from 'vue-router'

    const FullLayout = defineAsyncComponent(
        () => import('./layouts/FullLayout.vue')
    )
    const VerticalLayout = defineAsyncComponent(
        () => import('./layouts/DrawerLayout.vue')
    )
    /**
     * The Current route
     */
    const route = useRoute()

    provide('route', route)
    /**
     * The title of the current route
     */
    const currentTitle = computed(() => route.meta.pageTitle as string)

    /**
     * The layout that the current route require
     */
    const layout = computed(() => {
        switch (route.meta.layout) {
            case 'full':
                return FullLayout
            default:
                return VerticalLayout
        }
    })
    const isDevMode = import.meta.env.DEV
    /**
     * The breadcrumb of the current route
     */
    const breadcrumb = computed(
        (): Array<RouteBreadcrumb> =>
            (route.meta as RouteMetaData).breadcrumb || []
    )
</script>

<template>
    <Teleport to="head">
        <title>
            {{ isDevMode ? '[Dev] ' : '' }}
            ERPt
            {{ currentTitle ? ` :: ${currentTitle}` : '' }}
        </title>
    </Teleport>

    <component :is="layout" :breadcrumb="breadcrumb" :title="currentTitle">
        <RouterView v-slot="{ Component }">
            <!-- <Transition> -->
            <Transition
                enter-active-class="tw-transition-all tw-duration-350 tw-ease-in"
                enter-from-class="tw-opacity-10 tw-translate-x-full tw-scale-40"
                enter-to-class="tw-opacity-100 tw-scale-100"
                leave-active-class="tw-transition-all tw-duration-400 tw-ease-in"
                leave-from-class="tw-opacity-100 tw-scale-40"
                leave-to-class="tw-opacity-0 tw-translate-x-64 tw-scale-60">
                <component :is="Component" />
            </Transition>
        </RouterView>
    </component>
    <!-- </Transition> -->
</template>

<style lang="scss">
    html,
    body,
    #app {
        @apply tw-min-w-full tw-flex tw-justify-between tw-items-stretch tw-h-screen;
    }
</style>
