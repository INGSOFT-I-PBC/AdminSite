<script setup lang="ts">
    import { inject, ref } from 'vue'
    import UserCard from '@components/UserCard.vue'
     import ECard from '@components/custom/ECard.vue'
    import ERow from  '@components/custom/ERow.vue'
    import ECol from  '@components/custom/ECol.vue'
    import ListBox from  '@components/custom/ListBox.vue'
    import InputText from  '@components/custom/InputText.vue'
    import EButton from  '@components/custom/EButton.vue'
    import ModalDialog from  '@components/custom/ModalDialog.vue'
    import Title from  '@components/custom/Title.vue'
    import Table from  '@components/holders/Table.vue'
    import { computed, reactive } from 'vue'
    

    import {
        useRoute,
        useRouter,
    } from 'vue-router'
    const router = useRouter()

   // 

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
                    class="tw-p-10 tw-px-24 tw-bg-gray-100 tw-ring-slate-600 dark:tw-bg-slate-800">
                    <EButton type="secondary" >+ Agregar rol </EButton>
                </div>
                <div
                    id="__left-menu-container"
                    class="tw-w-full tw-flex-1 tw-overflow-y-auto tw-bg-gray-200" >
                    <DrawerMenu>

                        <form
                            class="d-flex"
                            role="search">
                            <input
                                class="form-control me-2"
                                type="search"
                                placeholder="Buscar rol"
                                aria-label="Search" />
                            <button
                                class="btn btn-outline-black"
                                type="submit">
                                Search
                            </button>
                            
                          </form>


                        
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
            
            <!-- End of header -->
            <div
                id="_page-breadcrumb_row"
                class="tw-flex tw-my-2 tw-transform-gpu tw-transition-all tw-duration-200 tw-ease-linear">
                
            </div>
            <!-- End of Breadcrumb -->
            

            
        </main>
    </div>
</template>
