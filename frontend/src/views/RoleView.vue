<script setup lang="ts">
    import EButton from '@components/custom/EButton.vue'
    //
   const array = ["Cajero", "Vendedor", "Bodeguero"];

</script>

<template>
    <div
        class="tw-flex tw-flex-rows tw-justify-items-stretch tw-min-h-screen tw-w-full tw-justify-between tw-bg-neutral-100 dark:tw-bg-neutral-900 tw-overflow-x-hidden"
        id="_root">
        <aside
            class="tw-h-full tw-min-w-fit tw-bg-slate-600 tw-rounded-r-xl tw-overflow-hidden">
            <div 
                id="__left-drawer"
                class="tw-h-full tw-flex tw-flex-col tw-justify-self-stretch tw-justify-items-stretch lg:tw-min-w-fit tw-resize-x">
                <div
                    id="__left-logo-container"
                    class="tw-p-10 tw-px-24 tw-bg-gray-300 tw-ring-slate-600 dark:tw-bg-slate-800">
                    <EButton type="secondary">+ Agregar rol </EButton>
                </div>
                <div 
                    id="__left-menu-container"
                    class="tw-w-full tw-flex-1 tw-overflow-y-auto tw-bg-gray-200">
                    <DrawerMenu ref="menuContainer">
                    <form class="d-flex" role="search">
                            <input
                                class="form-control me-2"
                                type="search"
                                placeholder="Buscar rol"
                                aria-label="Search" />
                            <button class="btn btn-outline-black" type="submit">
                                Search
                            </button>
                        </form>
                        <TransitionGroup style="display:flex;align-items: center;" enter-active-class="tw-transition-all tw-duration-400"
                          enter-from-class="tw-opacity-0 -tw-translate-x-50 tw-scale-60"
                          enter-to-class="tw-opacity-100 tw-scale-100"
                          leave-active-class="tw-transition-all tw-duration-900"
                          leave-from-class="tw-scale-105"
                          leave-to-class="tw-scale-10 tw-opacity-20 -tw-translate-x-full">

                          <div v-for="item in array">

                             <RouterLink  style="display:flex;align-items;margin-top:10px" class="hover:tw-text-primary hover:tw-font-bold" to="/">{{ item }}</RouterLink>


                          </div>

                        </TransitionGroup>
                       
                    </DrawerMenu>
                </div>
            </div>
        </aside>
        <!-- Resize bar -->
        <div
            class="resize-handle--x tw-cursor-ew-resize tw-justify-center hover:tw-bg-primary-light tw-w-1 hover:tw-animate-pulse hover:tw-transition tw-ease-in-out tw-duration-700 tw-bg-transparent"
            data-target="aside" />
        <!-- Right view -->
        <main
            class="tw-px-4 tw-py-2 tw-justify-items-stretch tw-w-full tw-gap-3 tw-flex-1 tw-flex tw-flex-col"
            id="right-panel">
            <header
                class="tw-flex tw-flex-row tw-gap-3 tw-justify-between tw-justify-items-stretch">
                <UserCard />
                <div
                    id="_page-title-container"
                    class="tw-bg-secondary tw-px-5 tw-rounded-md dark:tw-bg-slate-800 tw-grid tw-content-center tw-justify-items-center tw-justify-center tw-align-middle tw-flex-1">

                </div>
            </header>
            <!-- End of header -->
            <div
                id="_page-breadcrumb_row"
                class="tw-flex tw-my-2 tw-transform-gpu tw-transition-all tw-duration-200 tw-ease-linear">
                <div
                    id="_breadcrumb-container"
                    class="tw-py-1 tw-px-3 tw-rounded-md tw-grid tw-grid-flow-col tw-gap-2 tw-items-center tw-bg-slate-600 tw-text-gray-50">
                    <TransitionGroup
                        enter-active-class="tw-transition-all tw-duration-400"
                        enter-from-class="tw-opacity-0 -tw-translate-x-50 tw-scale-60"
                        enter-to-class="tw-opacity-100 tw-scale-100"
                        leave-active-class="tw-transition-all tw-duration-900"
                        leave-from-class="tw-scale-105"
                        leave-to-class="tw-scale-10 tw-opacity-20 -tw-translate-x-full">
                        
                      
                            
                    </TransitionGroup>
                </div>
            </div>
            <!-- End of Breadcrumb -->
            <div class="row tw-grid tw-z-10">
                <Transition
                    enter-active-class="tw-transition-all tw-duration-350 tw-ease-in"
                    enter-from-class="tw-opacity-10 tw-translate-x-full tw-scale-40"
                    enter-to-class="tw-opacity-100 tw-scale-100"
                    leave-active-class="tw-transition-all tw-duration-400 tw-ease-in"
                    leave-from-class="tw-opacity-100 tw-scale-110"
                    leave-to-class="tw-opacity-0 tw-translate-x-64 tw-scale-60">
                    <slot> Información de roles

                    </slot>
                </Transition>
            </div>

           
        </main>
    </div>
</template>
