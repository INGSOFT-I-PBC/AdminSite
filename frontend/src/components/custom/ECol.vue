<script setup lang="ts">
    import { computed } from 'vue'

    const props = defineProps({
        cols: {
            type: [Number, String],
            default: 'auto',
        },
        sm: {
            type: [Number, String],
            default: null,
        },
        md: {
            type: [Number, String],
            default: null,
        },
        lg: {
            type: [Number, String],
            default: null,
        },
        xl: {
            type: [Number, String],
            default: null,
        },
        xxl: {
            type: [Number, String],
            default: null,
        },
    })

    interface NormalizedBreakpointValue {
        [breakpoint: string]: number
    }

    function normalize(value: number, original: string | number) {
        if (original?.toString().toLowerCase().trim() === 'auto') return '-auto'
        if (value >= 1 && value <= 12) return `-${value}`
        return ''
    }

    const widthClass = computed(() => {
        const { cols, sm: rxs, md: rmd, lg: rlg, xl: rxl, xxl: rxxl } = props
        const normalized: Partial<NormalizedBreakpointValue> = {
            sm: Number(rxs),
            md: Number(rmd),
            lg: Number(rlg),
            xl: Number(rxl),
            xxl: Number(rxxl),
        }
        const numCols = Number(cols)
        const classes = [`col${normalize(numCols, cols)}`]
        Object.getOwnPropertyNames(normalized).forEach(breakpoint => {
            const suffix = normalize(
                normalized[breakpoint] as number,
                (props as NormalizedBreakpointValue)[breakpoint]
            )
            if (suffix) classes.push(`col-${breakpoint}${suffix}`)
        })
        return classes
    })
</script>

<template>
    <Transition>
        <!-- class="tw-flex-grow-0 tw-flex-shrink-0 tw-basis-auto tw-justify-items-stretch tw-flex-col" -->
        <div :class="widthClass" c-type="column">
            <slot />
        </div>
    </Transition>
</template>
