<script setup lang="ts">
    import type { BorderRadius } from '@components-types'

    import type { PropType } from 'vue'
    import { watch } from 'vue'

    const overlayContainer = ref(null)
    const overlayBg = ref()
    const props = defineProps({
        show: {
            type: Boolean,
            default: false,
        },
        rounded: {
            type: String as PropType<BorderRadius>,
            default: 'md',
        },
    })
    watch(
        () => props.show,
        async (_oldValue: unknown, newValue: unknown) => {
            if (!newValue) return
        }
    )
</script>

<template>
    <div ref="overlayContainer" class="t-overlay">
        <Transition
            class=""
            enter-active-class="tw-transition-all tw-duration-300"
            enter-from-class="tw-opacity-0"
            enter-to-class="tw-opacity-100"
            leave-active-class="tw-transition-all tw-duration-300"
            leave-from-class="tw-opacity-100"
            leave-to-class="tw-opacity-0">
            <div
                ref="overlayBg"
                class="t-overlay-content"
                v-show="show"
                :class="border[rounded]">
                <slot name="content" />
            </div>
        </Transition>
        <slot />
    </div>
</template>

<style lang="scss" module="border">
    .sm {
        @apply tw-rounded-sm;
    }
    .md {
        @apply tw-rounded-md;
    }
    .lg {
        @apply tw-rounded-lg;
    }
    .xl {
        @apply tw-rounded-xl;
    }
    .xxl {
        @apply tw-rounded-2xl;
    }
    .xxxl {
        @apply tw-rounded-3xl;
    }
    .none {
        @apply tw-rounded-none;
    }
</style>

<style lang="scss">
    .t-overlay {
    }
    .t-overlay-content {
        @apply tw-w-full tw-h-full tw-bg-black/50 tw-absolute tw-z-10;
    }
</style>
