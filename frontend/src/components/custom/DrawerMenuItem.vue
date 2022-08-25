<script setup lang="ts">
    import { computed, inject } from 'vue'
    import { TransitionRoot, TransitionChild } from '@headlessui/vue'
    import DrawerMenu from './DrawerMenu.vue'
    import { useRouter, type RouteLocationNormalized, type Router } from 'vue-router'
    // <{
    //     data: MenuItem
    //     child?: boolean
    //     level?: number
    // }>
    const props = defineProps({
        data: {
            type: Object,
            required: true,
        },
        child: {
            type: Boolean,
            default: false,
        },
        level: {
            type: Number,
            default: null,
        },
    })
    const emit = defineEmits(['update:level'])

    const router = useRouter()
    const currentRoute = inject('route') as RouteLocationNormalized

    const active = ref(false)
    const toggleChild = ref(false)
    const hasChilds = computed(() => !!props.data.children?.length)
    const classes = computed(() => ({
        'tw-bg-slate-800': active.value,
        'hover:tw-bg-slate-700': !active.value,
    }))
    function menuSelected() {
        toggleChild.value = !toggleChild.value
        if (props.data.path) router.push({ path: props.data.path })
        active.value = !active.value
    }
</script>

<template>
    <li class="tw-transform-gpu">
        <!-- <TransitionRoot
            :show="true"
            enter-active-class="tw-duration-200"
            enter-from="tw-scale-x-0"
            enter-to="tw-scale-x-100"
            :appear="true"
            as="template"> -->
        <div>
            <div
                class="tw-px-3 tw-py-2 tw-text-neutral-300 tw-ring-slate-500 tw-mx-2 tw-flex tw-flex-row gap-2 tw-rounded tw-my-2 tw-justify-center tw-justify-items-center tw-items-center tw-content-center tw-select-none tw-transition-all tw-duration-250 tw-ease-in"
                :class="classes"
                @click="menuSelected">
                <VueFeather v-if="data.icon" :type="data.icon" size="20" />
                <span class="tw-flex-grow sm:tw-text-medium md:tw-text-lg">
                    {{ data.label }}
                </span>
                <template v-if="data.children?.length">
                    <VueFeather
                        class="tw-transition-all tw-duration-500 tw-transform-gpu"
                        :class="active ? 'tw-rotate-180' : 'tw-rotate-0'"
                        type="chevron-up" />
                </template>
            </div>
            <Transition
                enter-active-class="tw-transition-all tw-duration-500 tw-transform-gpu"
                enter-from-class="tw-max-h-0 tw-opacity-0"
                enter-to-class="tw-opacity-100"
                leave-active-class="tw-transition-all tw-duration-500 tw-ease-in-out tw-overflow-hidden"
                leave-from-class="tw-opacity-100"
                leave-to-class="tw-max-h-0 tw-opacity-0">
                <DrawerMenu
                    class="tw-ml-5 tw-mt-2"
                    v-if="hasChilds && toggleChild"
                    ref="sub_item">
                    <template v-for="(childItem, idx) of data.children" :key="idx">
                        <DrawerMenuItem
                            :data="childItem"
                            :child="hasChilds"
                            :level="(props.level || 0) + 1" />
                    </template>
                </DrawerMenu>
            </Transition>
        </div>
        <!-- </TransitionRoot> -->
    </li>
</template>
