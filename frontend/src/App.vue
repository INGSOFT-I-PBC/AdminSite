<script setup lang="ts">
    import { computed, defineAsyncComponent, provide } from 'vue'
    import { useRoute, RouterView } from 'vue-router'
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
    <head>
        <title>
            {{ isDevMode ? '[Dev] ' : '' }}
            ERPt
            {{ currentTitle ? ` :: ${currentTitle}` : '' }}
        </title>
    </head>
    <Transition
        enter-active-class="tw-transition-all tw-duration-300"
        enter-from-class="tw-opacity-0"
        enter-to-class="tw-opacity-100">
        <component :is="layout" :title="currentTitle" :breadcrumb="breadcrumb">
            <!-- <Transition
                class=""
                enter-active-class="tw-transition-all tw-transform-gpu tw-ease-in-out tw-duration-550"
                enter-from-class="tw-opacity-0 tw-scale-10"
                enter-to-class="tw-opacity-100 tw-scale-105"
                leave-active-class="tw-transition-all tw-transform-gpu tw-ease-in tw-duration-400"
                leave-from-class="tw-opacity-100 tw-scale-105"
                leave-to-class="tw-opacity-0 tw-scale-90 tw-translate-x-full"> -->
            <RouterView v-slot="{ Component }">
                <Transition>
                    <component :is="Component" />
                </Transition>
            </RouterView>
            <!-- </Transition> -->
        </component>
    </Transition>
</template>

<style lang="scss">
    html,
    body,
    #app {
        @apply tw-min-w-full tw-flex tw-justify-between tw-items-stretch tw-h-screen;
    }
</style>
