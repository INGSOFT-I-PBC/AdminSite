<script setup lang="ts">
    defineProps({
        title: {
            type: String,
            default: 'NO TITLE',
        },
    })
</script>

<template>
    <div
        class="flex flex-rows justify-items-stretch h-full w-screen justify-between"
        id="_root">
        <aside
            class="h-full min-w-fit bg-slate-600">
            <div
                id="__left-drawer"
                class="h-full flex flex-col justify-self-stretch justify-items-stretch lg:min-w-fit resize-x rounded">
                <div
                    id="__left-logo-container"
                    class="p-10 px-24 bg-gray-300 ring-slate-600">
                    logo
                </div>
                <div
                    id="__left-menu-container"
                    class="w-full flex-1 overflow-y-auto" />
            </div>
        </aside>
        <!-- Resize bar -->
        <div
            class="resize-handle--x hover:bg-primary-light w-1 hover:animate-pulse hover:transition ease-in-out duration-700 bg-transparent"
            data-target="aside"></div>
        <!-- Right view -->
        <div
            class="mx-4 py-2 justify-items-stretch w-full gap-3"
            id="right-panel">
            <div
                class="flex flex-row gap-3 justify-between justify-items-stretch">
                <div
                    id="_user-profile-card"
                    class="justify-self-start grid grid-cols-2 gap-3 bg-primary px-3 text-on-primary dark:bg-slate-600 rounded-md w-1/3 md:w-1/4 lg:w-1/12 py-2 dark:text-on-secondary-hard min-w-fit drop-shadow-lg">
                    <div class="content-center">
                        <img src="" alt="" />
                        <FontAwesomeIcon
                            class="align-middle h-10 p-1"
                            icon="fa-solid fa-circle-user" />
                    </div>
                    <div
                        class="grid content-center">
                        <span
                            class="text-md font-bold">
                            User
                        </span>
                        <small
                            class="text-xs italic">
                            Role
                        </small>
                    </div>
                </div>
                <div
                    id="_page-title-container"
                    class="bg-secondary px-5 rounded-md dark:bg-slate-800 grid content-center justify-items-center justify-center align-middle flex-1">
                    <h1
                        class="font-bold text-on-secondary dark:text-on-secondary-hard text-2xl">
                        {{ title }}
                    </h1>
                </div>
            </div>
            <!-- End of header -->
            <div
                id="_page-breadcrumb_row"
                class="flex my-2">
                <div
                    id="_breadcrumb-container"
                    class="py-1 px-3 rounded-md grid grid-flow-col gap-2 items-center bg-slate-600 text-gray-50">
                    <FontAwesomeIcon
                        class="h-4 text-center content-center align-middle"
                        icon="fa-solid fa-house-chimney" />
                    <h2>Home</h2>
                </div>
            </div>
            <!-- End of Breadcrumb -->
            <div class="row">
                <slot
                    >No element is defined
                    here</slot
                >
            </div>
        </div>
    </div>
</template>

<style lang="postcss"></style>
