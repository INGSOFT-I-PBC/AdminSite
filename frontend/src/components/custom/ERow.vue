<script setup lang="ts">
    import type {
        HorizontalAlignment,
        VerticalAlignment,
    } from '@components-types'

    import { type PropType, computed } from 'vue'

    const props = defineProps({
        alignV: {
            type: String as PropType<VerticalAlignment>,
            default: 'end',
        },
        alignH: {
            type: String as PropType<HorizontalAlignment>,
            default: 'start',
        },
    })

    const alignClass = computed(() => {
        const alignV = props.alignV?.toLowerCase().trim()
        const alignH = props.alignH?.toLocaleLowerCase().trim()
        return {
            'tw-items-start': alignV === 'start',
            'tw-items-end': alignV === 'end',
            'tw-items-baseline': alignV === 'baseline',
            'tw-items-stretch': alignV === 'stretch',
            'tw-items-center': alignV === 'middle' || !alignV,
            'tw-content-start': alignH === 'start',
            'tw-content-end': alignH === 'end',
            'tw-content-center': alignH === 'center',
            'tw-content-between': alignH === 'between',
            'tw-content-around': alignH === 'around',
            'tw-content-none': alignH === 'none',
            // fallback
            // 'tw-content-'
        }
    })
</script>
<template>
    <!-- class="tw-flex tw-flex-row tw-flex-grow-0 tw-flex-shrink-0 tw-basis-auto tw-flex-wrap tw-gap-2 tw-max-w-full" -->
    <div c-type="row" class="row gy-2" :class="alignClass">
        <slot></slot>
    </div>
</template>
