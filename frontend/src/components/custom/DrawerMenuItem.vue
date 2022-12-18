<script setup lang="ts">
    import { computed, inject } from 'vue'
    import { type RouteLocationNormalized, useRouter } from 'vue-router'

    import DrawerMenu from './DrawerMenu.vue'

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
    const emit = defineEmits(['update:level', 'click'])

    const router = useRouter()
    const instance = ref()
    const currentRoute = inject('route') as RouteLocationNormalized

    const active = ref(false)
    const toggleChild = ref(false)
    const hasChilds = computed(() => !!props.data.children?.length)
    const isShown = computed(() => {
        const name = currentRoute.name
        return name === props.data.routeName
    })
    const activePage = computed(() => isShown.value && !hasChilds.value)

    const classes = computed(() => ({
        'tw-bg-slate-800': activePage.value,
        'hover:tw-bg-slate-700': !activePage.value,
    }))
    function menuSelected() {
        if (activePage.value) return

        toggleChild.value = !toggleChild.value
        if (props.data.path) router.push({ path: props.data.path })
        active.value = !active.value
        emit('click', { menuConfig: props.data, from: instance })
    }
    defineExpose({
        instance,
    })
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
                ref="instance"
                :class="classes"
                @click="menuSelected">
                <VueFeather
                    v-if="data.icon"
                    :type="data.icon"
                    size="20"
                    class="tw-pointer-events-none" />
                <span
                    class="tw-flex-grow sm:tw-text-medium md:tw-text-lg tw-pointer-events-none">
                    {{ data.label }}
                </span>
                <template v-if="data.children?.length">
                    <VueFeather
                        class="tw-transition-all tw-duration-500 tw-transform-gpu tw-pointer-events-none"
                        :class="active ? 'tw-rotate-0' : 'tw-rotate-180'"
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
                    v-show="hasChilds && toggleChild"
                    ref="sub_item">
                    <template
                        v-for="(childItem, idx) of data.children"
                        :key="idx">
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
