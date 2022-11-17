<script setup lang="ts">
    import type {
        ColorTheme,
        Orientation,
        TextColorMode,
    } from '@components-types'

    import type { PropType } from 'vue'

    const props = defineProps({
        modelValue: {
            type: String,
            default: '',
        },
        modelModifiers: {
            type: Object as PropType<{
                capitalize?: boolean
                trim?: boolean
                upper?: boolean
                lower?: boolean
                number?: boolean
                alpha?: boolean
            }>,
            default: () => ({} as Record<string, string>),
        },
        theme: {
            type: String as PropType<ColorTheme>,
            default: 'auto',
        },
        color: {
            type: String as PropType<TextColorMode>,
            default: 'auto',
        },
        resize: {
            type: String as PropType<Orientation | 'both' | 'none'>,
            default: 'both',
        },
        placeholder: {
            type: String,
            default: '',
        },
        cols: {
            type: [Number, String],
            default: 20,
        },
    })

    const emit = defineEmits(['update:modelValue'])
    function emitValue(e: Event) {
        let value = (e.target as HTMLTextAreaElement).value
        if (props.modelModifiers?.capitalize) {
            value = value.charAt(0).toUpperCase() + value.slice(1)
        }
        if (props.modelModifiers?.trim) {
            value = value.trim()
        }
        if (props.modelModifiers?.upper) {
            value = value.toUpperCase()
        }
        if (props.modelModifiers?.lower) {
            value = value.toLowerCase()
        }
        if (props.modelModifiers?.number) {
            value = value.replace(/[^0-9]/g, '')
        }
        if (props.modelModifiers?.alpha) {
            value = value.replace(/[0-9]/g, '')
        }
        emit('update:modelValue', value)
    }
</script>

<template>
    <textarea
        class="t-text-area"
        :placeholder="placeholder"
        :cols="cols"
        :class="[
            textMode[color] ?? textMode.auto,
            resizeMode[resize] ?? resizeMode.both,
            colorscheme[theme] ?? colorscheme.outline,
        ]"
        :value="modelValue"
        @input="emitValue" />
</template>

<style module="colorscheme" lang="scss">
    .auto {
        @apply tw-bg-black/10 dark:tw-bg-gray-50/30;
    }
    .daynight {
        @apply tw-bg-gray-200 dark:tw-bg-slate-800;
    }
    .light {
        .light-auto {
        }
    }
    .dark {
        .dark-auto {
        }
    }
    .outline {
        background-color: transparent !important;
    }
</style>

<style module="textMode" lang="scss">
    .auto {
        @apply tw-text-slate-900 dark:tw-text-slate-300;
    }
    .light {
        @apply tw-text-slate-300;
    }
    .dark {
        @apply tw-text-black;
    }
    .night {
        @apply tw-text-slate-800;
    }
    .danger {
        @apply tw-text-red-500;
    }
    .success {
        @apply tw-text-emerald-800;
    }
</style>
<style module="resizeMode">
    .horizontal {
        @apply tw-resize-x;
    }
    .vertical {
        @apply tw-resize-y;
    }
    .none {
        @apply tw-resize-none;
    }
    .both {
        @apply tw-resize;
    }
</style>

<style lang="scss">
    .t-text-area {
        @apply tw-rounded tw-bg-neutral-500/5 dark:tw-bg-slate-900
        dark:tw-ring-neutral-500 tw-ring-1 tw-ring-neutral-300 tw-shadow-md tw-px-2 tw-py-1.5 tw-max-w-full;
    }
</style>
