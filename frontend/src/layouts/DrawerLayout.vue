<script setup lang="ts">
    import { menus as menuItems } from '@/layouts/drawer'
    import DrawerMenu from '@components/custom/DrawerMenu.vue'
    import { useAuthStore } from '@store'

    import { computed, inject, ref } from 'vue'
    import { useRouter } from 'vue-router'

    import UserCard from '../components/UserCard.vue'
    import DrawerMenuItem from '../components/custom/DrawerMenuItem.vue'
    import Title from '../components/custom/Title.vue'

    defineProps({
        title: {
            type: String,
            default: 'NO TITLE',
        },
        breadcrumb: {
            type: Array<{
                text: string
                active: boolean
                href: string
            }>,
            default: () => [],
        },
    })
    const authStore = useAuthStore()
    const router = useRouter()
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const routeMap: MapObj<any> = {} as MapObj<any>
    useRouter()
        .getRoutes()
        .forEach(route => {
            routeMap[
                (route as unknown as RouteConfig).name?.toString() || 'unknown'
            ] = route.meta?.permission
        })
    // .map(it => ({
    //     name: it.name,
    //     meta: it.meta
    // }))
    /* Inject flags to children */
    const isDebug = ref(import.meta.env.DEV)
    inject<boolean>('isDebug', isDebug.value)
    type FilteredMenuItem = MenuItem & { showable: boolean }
    // TODO: Make this work
    /* eslint-disable @typescript-eslint/no-unused-vars */
    const availableMenus = computed(() => {
        const flatten: FilteredMenuItem[] = []
        const stack = [...menuItems]
        while (stack.length) {
            const currentNode = stack.pop() as MenuItem
            if (currentNode.forceRender) {
                const node = { ...currentNode, showable: true }
                node.children = [] // reset to filter childs
                flatten.push()
            }
        }
        return menuItems.filter(menu => {
            console.log('Verifing for: ', menu.routeName)
            return (
                menu.forceRender ||
                authStore.hasPermission(
                    routeMap[menu.routeName || 'unknown'] || 'bypass'
                )
            )
        })
    })
    function logout() {
        authStore
            .logout()
            .then((it: unknown) => {
                router.push({ path: '/login' })
            })
            .catch((it: unknown) => {
                console.error(it)
            })
    }
</script>

<template>
    <div
        class="tw-flex tw-flex-rows tw-justify-items-stretch tw-min-h-screen tw-w-full tw-justify-between tw-bg-neutral-100 dark:tw-bg-neutral-900 tw-overflow-x-hidden"
        id="_root">
        <aside
            class="tw-h-full tw-min-w-fit tw-bg-slate-600 tw-rounded-r-xl tw-overflow-hidden tw-resize-x">
            <div
                id="__left-drawer"
                class="tw-h-full tw-flex tw-flex-col tw-justify-self-stretch tw-justify-items-stretch lg:tw-min-w-fit tw-resize-x">
                <div
                    id="__left-logo-container"
                    class="tw-p-10 tw-px-24 tw-bg-gray-300 tw-ring-slate-600 dark:tw-bg-slate-800">
                    <Title>LOGO</Title>
                </div>
                <div
                    id="__left-menu-container"
                    class="tw-w-full tw-flex-1 tw-overflow-y-auto">
                    <DrawerMenu ref="menuContainer">
                        <template
                            v-for="(menuItemData, idx) of menuItems"
                            :key="idx">
                            <DrawerMenuItem
                                v-if="menuItemData.id != 'logout'"
                                :data="menuItemData" />
                            <DrawerMenuItem
                                v-else
                                @click="logout"
                                :data="menuItemData" />
                        </template>
                    </DrawerMenu>
                </div>
            </div>
        </aside>
        <!-- Resize bar -->
        <div
            class="resize-handle--x tw-cursor-ew-resize tw-justify-center tw-resize-x hover:tw-bg-primary-light tw-w-1 hover:tw-animate-pulse hover:tw-transition tw-ease-in-out tw-duration-700 tw-bg-transparent"
            data-target="aside" />
        <!-- Right view -->
        <main class="main-section" id="right-panel">
            <header
                class="tw-flex tw-flex-row tw-gap-3 tw-justify-between tw-justify-items-stretch">
                <UserCard
                    :username="authStore.userData?.username"
                    :role="authStore.userData?.role" />
                <div
                    id="_page-title-container"
                    class="tw-bg-secondary tw-px-5 tw-rounded-md dark:tw-bg-slate-800 tw-grid tw-content-center tw-justify-items-center tw-justify-center tw-align-middle tw-flex-1">
                    <h1
                        class="tw-font-bold tw-text-on-secondary dark:tw-text-on-secondary-hard tw-text-2xl">
                        {{ title }}
                    </h1>
                </div>
            </header>
            <!-- End of header -->
            <div
                id="_page-breadcrumb_row"
                class="tw-flex tw-my-2 tw-transform-gpu tw-transition-all tw-duration-200 tw-ease-linear">
                <div
                    id="_breadcrumb-container"
                    class="tw-py-1 tw-px-3 tw-rounded-md tw-grid tw-grid-flow-col tw-gap-2 tw-items-center tw-bg-slate-600 tw-text-gray-50">
                    <FontAwesomeIcon
                        class="tw-h-4 tw-text-center tw-content-center tw-align-middle"
                        icon="fa-solid fa-house-chimney" />
                    <RouterLink class="breadcrumb_link" to="/"
                        >Principal</RouterLink
                    >
                    <TransitionGroup
                        enter-active-class="tw-transition-all tw-duration-400"
                        enter-from-class="tw-opacity-0 -tw-translate-x-50 tw-scale-60"
                        enter-to-class="tw-opacity-100 tw-scale-100"
                        leave-active-class="tw-transition-all tw-duration-900"
                        leave-from-class="tw-scale-105"
                        leave-to-class="tw-scale-10 tw-opacity-20 -tw-translate-x-full">
                        <div v-for="(item, index) of breadcrumb" :key="index">
                            <FontAwesomeIcon
                                class="tw-h-4 tw-mr-2"
                                :icon="`fa-solid ${
                                    index > 0
                                        ? 'fa-chevron-right'
                                        : 'fa-circle-chevron-right'
                                }`" />
                            <span v-if="!item.href || item.active">{{
                                item.text
                            }}</span>
                            <RouterLink
                                v-else
                                class="hover:tw-text-primary hover:tw-font-bold"
                                :to="item.href || '/'">
                                {{ item.text }}</RouterLink
                            >
                        </div>
                    </TransitionGroup>
                </div>
            </div>
            <!-- End of Breadcrumb -->
            <!--            <div class="row tw-grid tw-z-10">-->
            <!-- <Transition
                enter-active-class="tw-transition-all tw-duration-350 tw-ease-in"
                enter-from-class="tw-opacity-10 tw-translate-x-full tw-scale-40"
                enter-to-class="tw-opacity-100 tw-scale-100"
                leave-active-class="tw-transition-all tw-duration-400 tw-ease-in"
                leave-from-class="tw-opacity-100 tw-scale-110"
                leave-to-class="tw-opacity-0 tw-translate-x-64 tw-scale-60"> -->
            <slot>No element is defined here</slot>
            <!-- </Transition> -->
            <!--            </div>-->

            <!-- FOOTER -->
            <footer
                class="tw-sticky tw-top-full tw-bottom-0 tw-pb-1 tw-pt-5 tw-z-0">
                <span class="tw-text-neutral-500 dark:tw-text-neutral-400"
                    >Realizado en
                    <FontAwesomeIcon icon="fa-brands fa-vuejs" />
                    VueJS
                    <FontAwesomeIcon icon="fa-brands fa-node-js" />
                    NodeJS &
                    <FontAwesomeIcon icon="fa-brands fa-python" />
                    Python
                </span>
            </footer>
        </main>
    </div>
</template>

<style lang="scss">
    .main-section {
        @apply tw-px-4 tw-py-2 tw-justify-items-stretch tw-overflow-x-hidden tw-w-full tw-gap-3 tw-flex-1 tw-flex tw-flex-col tw-overflow-y-auto;
    }
    .drawer-left-view {
    }
</style>
