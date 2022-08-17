<script setup lang="ts">
    import { inject, ref } from 'vue'
    import UserCard from '../components/UserCard.vue'
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
    /* Inject flags to children */
    const isDebug = ref(import.meta.env.DEV)
    inject<boolean>('isDebug', isDebug.value)
</script>

<template>
    <div
        class="tw-flex tw-flex-rows tw-justify-items-stretch tw-min-h-screen tw-w-screen tw-justify-between tw-bg-neutral-100 dark:tw-bg-neutral-900"
        id="_root">
        <aside
            class="tw-h-full tw-min-w-fit tw-bg-slate-600">
            <div
                id="__left-drawer"
                class="tw-h-full tw-flex tw-flex-col tw-justify-self-stretch tw-justify-items-stretch lg:tw-min-w-fit tw-resize-x tw-rounded">
                <div
                    id="__left-logo-container"
                    class="tw-p-10 tw-px-24 tw-bg-gray-300 tw-ring-slate-600">
                    logo
                </div>
                <div
                    id="__left-menu-container"
                    class="tw-w-full tw-flex-1 tw-overflow-y-auto" />
            </div>
        </aside>
        <!-- Resize bar -->
        <div
            class="resize-handle--x tw-cursor-ew-resize tw-justify-center hover:tw-bg-primary-light tw-w-1 hover:tw-animate-pulse hover:tw-transition tw-ease-in-out tw-duration-700 tw-bg-transparent"
            data-target="aside" />
        <!-- Right view -->
        <div
            class="tw-mx-4 tw-py-2 tw-justify-items-stretch tw-w-full tw-gap-3 flex tw-flex-col"
            id="right-panel">
            <header
                class="tw-flex tw-flex-row tw-gap-3 tw-justify-between tw-justify-items-stretch">
                <UserCard />
                <!--
                <div
                    id="_user-profile-card"
                    class="tw-justify-self-start tw-grid tw-grid-cols-2 tw-gap-3 tw-bg-primary tw-px-3 tw-text-on-primary dark:tw-bg-slate-600 tw-rounded-md tw-w-1/3 md:tw-w-1/4 lg:tw-w-1/12 tw-py-2 dark:tw-text-on-secondary-hard tw-min-w-fit tw-drop-shadow-lg">
                    <div
                        class="tw-content-center">
                        <img src="" alt="" />
                        <FontAwesomeIcon
                            class="tw-align-middle tw-h-10 tw-p-1"
                            icon="fa-solid fa-circle-user" />
                    </div>
                    <div
                        class="tw-grid tw-content-center">
                        <span
                            class="tw-text-md tw-font-bold">
                            User
                        </span>
                        <small
                            class="tw-text-xs tw-italic">
                            Role
                        </small>
                    </div>
                </div>
                -->
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
                class="tw-flex tw-my-2">
                <div
                    id="_breadcrumb-container"
                    class="tw-py-1 tw-px-3 tw-rounded-md tw-grid tw-grid-flow-col tw-gap-2 tw-items-center tw-bg-slate-600 tw-text-gray-50">
                    <FontAwesomeIcon
                        class="tw-h-4 tw-text-center tw-content-center tw-align-middle"
                        icon="fa-solid fa-house-chimney" />
                    <RouterLink
                        class="breadcrumb_link"
                        to="/"
                        >Principal</RouterLink
                    >
                    <div
                        v-for="(
                            item, index
                        ) of breadcrumb"
                        :key="index">
                        <FontAwesomeIcon
                            class="tw-h-4 tw-mr-2"
                            :icon="`fa-solid ${
                                index > 0
                                    ? 'fa-chevron-right'
                                    : 'fa-circle-chevron-right'
                            }`" />
                        <span
                            v-if="
                                !item.href ||
                                item.active
                            "
                            >{{ item.text }}</span
                        >
                        <RouterLink
                            v-else
                            class="hover:tw-text-primary hover:tw-font-bold"
                            :to="item.href || '/'"
                            >{{
                                item.text
                            }}</RouterLink
                        >
                    </div>
                </div>
            </div>
            <!-- End of Breadcrumb -->
            <main class="row">
                <slot
                    >No element is defined
                    here</slot
                >
            </main>

            <!-- FOOTER -->
            <footer
                class="tw-sticky tw-top-full tw-bottom-0">
                <span
                    class="tw-text-neutral-500 dark:tw-text-neutral-400"
                    >Realizado en
                    <FontAwesomeIcon
                        icon="fa-brands fa-vuejs" />
                    VueJS
                    <FontAwesomeIcon
                        icon="fa-brands fa-node-js" />
                    NodeJS &
                    <FontAwesomeIcon
                        icon="fa-brands fa-python" />
                    Python
                </span>
            </footer>
        </div>
    </div>
</template>

<style lang="postcss"></style>
