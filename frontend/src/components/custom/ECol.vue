<script setup lang="ts">
    import { computed } from 'vue'

    const props = defineProps({
        cols: {
            type: [Number, String],
            default: 'auto',
        },
    })

    const widthClass = computed(() => {
        const { cols } = props
        const numCols = Number(cols)
        return {
            'tw-w-auto':
                cols === 'auto' ||
                numCols < 1 ||
                numCols > 12,
            'tw-w-1/12': numCols === 1,
            'tw-w-1/6': numCols === 2,
            'tw-w-1/4': numCols === 3,
            'tw-w-1/3': numCols === 4,
            'tw-w-5/12': numCols === 5,
            'tw-w-1/2': numCols === 6,
            'tw-w-7/12': numCols === 7,
            'tw-w-2/3': numCols === 8,
            'tw-w-3/4': numCols === 9,
            'tw-w-5/6': numCols === 10,
            'tw-w-11/12': numCols === 11,
            'tw-w-full': numCols === 12,
        }
    })
</script>

<template>
    <Transition>
        <div
            class="tw-justify-self-stretch tw-grid"
            :class="widthClass">
            <slot />
        </div>
    </Transition>
</template>
