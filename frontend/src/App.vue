<script setup lang="ts">
    import { computed, defineAsyncComponent, provide } from 'vue'
    import { useRoute, RouterView } from 'vue-router'
    const FullLayout = defineAsyncComponent(() => import('./layouts/FullLayout.vue'))
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
    /**
     * The breadcrumb of the current route
     */
    const breadcrumb = computed(
        (): Array<RouteBreadcrumb> => (route.meta as RouteMetaData).breadcrumb || []
    )
</script>

<template>
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

<style scoped>
    .logo {
        display: block;
        margin: 0 auto 2rem;
    }

    nav {
        width: 100%;
        font-size: 12px;
        text-align: center;
        margin-top: 2rem;
    }

    nav a.router-link-exact-active {
        color: var(--color-text);
    }

    nav a.router-link-exact-active:hover {
        background-color: transparent;
    }

    nav a {
        display: inline-block;
        padding: 0 1rem;
        border-left: 1px solid var(--color-border);
    }

    nav a:first-of-type {
        border: 0;
    }

    @media (min-width: 1024px) {
        header {
            display: flex;
            place-items: center;
            padding-right: calc(var(--section-gap) / 2);
        }

        .logo {
            margin: 0 2rem 0 0;
        }

        header .wrapper {
            display: flex;
            place-items: flex-start;
            flex-wrap: wrap;
        }

        nav {
            text-align: left;
            margin-left: -1rem;
            font-size: 1rem;

            padding: 1rem 0;
            margin-top: 1rem;
        }
    }
</style>
