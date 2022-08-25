<script setup lang="ts">
    import { computed } from 'vue'

    const props = defineProps({
        alignV: {
            type: String,
            default: 'end',
        },
        alignH: {
            type: String,
            default: 'start',
        },
    })

    const alignClass = computed(() => {
        const alignV = props.alignV?.toLowerCase().trim()
        return {
            'tw-items-start': alignV === 'start',
            'tw-items-end': alignV === 'end',
            'tw-items-baseline': alignV === 'baseline',
            'tw-items-stretch': alignV === 'stretch',
            'tw-items-center': alignV === 'center' || !alignV, // fallback
            // 'tw-content-'
        }
    })
</script>
<template>
    <!-- class="tw-flex tw-flex-row tw-flex-grow-0 tw-flex-shrink-0 tw-basis-auto tw-flex-wrap tw-gap-2 tw-max-w-full" -->
    <div c-type="row" class="row" :class="alignClass">
        <slot></slot>
    </div>
</template>
