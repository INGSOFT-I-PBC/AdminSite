<script setup lang="ts">
    import { identity } from '@/components/types/checkers'
    import type { ColorTheme } from '@components-types'
    import type { InputType } from 'bootstrap-vue-3'

    import { type PropType, computed } from 'vue'

    const props = defineProps({
        modelValue: {
            type: String,
            default: '',
        },
        modelModifiers: {
            type: Object as PropType<Record<string, boolean>>,
            default: () => ({} as Record<string, boolean>),
        },
        type: {
            type: String as PropType<InputType>,
            default: 'text',
        },
        label: {
            type: String,
            default: null,
        },
        placeholder: {
            type: String,
            default: '',
        },
        labelStyle: {
            type: String,
            default: 'form-label',
        },
        infoLabel: {
            type: String,
            default: null,
        },
        noInfoLabel: {
            type: Boolean,
            default: false,
        },
        infoStyle: {
            type: [String, Array],
            default: () => ['tw-italic', 'tw-text-tiny'],
        },
        status: {
            type: Boolean as PropType<boolean | null>,
            default: null,
        },
        infoStatus: {
            type: String as PropType<
                'info' | 'warning' | 'success' | 'normal' | '' | 'danger'
            >,
            default: 'normal',
        },
        disabled: {
            type: Boolean,
            default: false,
        },
        leftIcon: {
            type: String,
            default: null,
        },
        rightIcon: {
            type: String,
            default: null,
        },
        theme: {
            type: String as PropType<ColorTheme>,
            default: () => 'auto',
        },
        readonly: {
            type: Boolean,
            default: () => false,
        },
        formatter: {
            type: Function as PropType<Mapper<string>>,
            default: identity,
        },
    })
    const emit = defineEmits([
        'update:modelValue',
        'rightIconClick',
        'leftIconClick',
        'keydown',
        'keyup',
        'change',
    ])
    const infoClass = computed(() => {
        const styles = Array.isArray(props.infoStyle)
            ? [...props.infoStyle]
            : props.infoStyle?.split(' ')
        // let styles = `${props.infoStyle || ''} `
        switch (props.infoStatus) {
            case 'danger':
                styles.push('tw-text-red-700', 'dark:tw-text-red-500')
                break
            case 'warning':
                styles.push('tw-text-amber-800', 'dark:tw-text-yellow-500')
                break
            case 'success':
                styles.push('tw-text-green-600', 'dark:tw-text-emerald-500')
                break
            default: // No apply styles
        }
        return styles
    })
    const inputDivClass = computed(() => {
        if (props.disabled) {
            return 'tw-bg-gray-200 tw-text-gray-400 dark:tw-bg-slate-900 dark:tw-text-slate-500 hover:tw-cursor-not-allowed tw-ring-neutral-300'
        }
        let classes = 'tw-bg-neutral-100 dark:tw-bg-slate-800 '
        if (props.status === true) {
            classes += 'tw-ring-teal-400 dark:tw-ring-emerald-600'
        } else if (props.status === false) {
            classes +=
                'focus:tw-outline-rose-600 tw-ring-red-600 dark:tw-ring-red-700 focus:tw-outline-1 tw-text-red-500 dark:tw-text-400'
        } else {
            classes +=
                'focus:tw-ring-cyan-600 tw-ring-neutral-300 dark:focus:tw-ring-sky-600 tw-text-black dark:tw-text-neutral-300'
        }
        return classes
    })
    const inputClass = computed(() => {
        if (props.disabled) {
            return 't-disabled'
        }
        let classes = '-tw-bg-neutral-50 dark:tw-bg-slate-800'
        if (props.status === true) {
            classes += 'tw-text-green-700 dark:tw-text-green-300'
        } else if (props.status === false) {
            // classes += 'tw-text-red-500 dark:tw-text-400'
            classes += 't-danger'
        } else {
            classes += 'tw-text-black dark:tw-text-neutral-300'
        }
        return classes
    })
    function interactionStart(event: Event) {
        emit('keydown')
        const target = event.target as HTMLButtonElement
        if (props.disabled) {
            event.preventDefault()
            target.blur()
        }
    }
    function emitValue(e: Event) {
        let value = (e.target as HTMLInputElement).value
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
        if (props.modelModifiers?.number || props.type === 'number') {
            value = value.replace(/\D/g, '')
        }
        if (props.modelModifiers?.alpha) {
            value = value.replace(/[0-9]/g, '')
        }
        if (
            (props.formatter ?? undefined) != undefined &&
            typeof props.formatter == 'function'
        ) {
            value = props.formatter(value)
        }
        emit('update:modelValue', value)
        e.preventDefault()
        const input = e.target as HTMLInputElement
        input.value = value
    }
</script>

<template>
    <div class="tw-flex tw-flex-col">
        <label v-if="label" :class="labelStyle">
            {{ label }}
        </label>
        <div
            class="t-input-text"
            :class="[colorscheme[theme]]"
            :classa="[inputDivClass, colorscheme[theme]]">
            <button
                type="button"
                class="tw-text-center tw-ml-1 tw-grid tw-content-center focus:tw-outline-none"
                :class="disabled ? 'hover:tw-cursor-not-allowed' : ''"
                v-if="leftIcon"
                @click="!disabled ? $emit('leftIconClick') : () => {}">
                <slot name="leftIcon">
                    <vue-feather :type="leftIcon" />
                </slot>
            </button>
            <input
                @mousedown="interactionStart"
                @keydown="interactionStart"
                @keyup="$emit('keyup')"
                @change="$emit('change')"
                :value="modelValue"
                @input="emitValue"
                :placeholder="placeholder"
                class="t-input tw-py-1.5 lg:tw-py-2 xl:tw-py-2.5' tw-px-1 tw-bg-transparent tw-outline-none min-w-full tw-flex-1"
                :class="inputClass"
                :readonly="readonly"
                :type="type" />
            <button
                type="button"
                class="tw-text-center tw-p-0.5 tw-content-center tw-grid focus:tw-outline-none"
                v-if="rightIcon"
                :class="disabled ? 'hover:tw-cursor-not-allowed' : ''"
                @click="!disabled ? $emit('rightIconClick') : () => {}">
                <slot name="rightIcon">
                    <vue-feather v-if="rightIcon" :type="rightIcon" />
                </slot>
            </button>
        </div>
        <slot v-if="!noInfoLabel" name="info-label">
            <small :class="infoClass"> {{ infoLabel }}&ZeroWidthSpace; </small>
        </slot>
    </div>
</template>

<style lang="scss">
    .form-label {
        @apply tw-font-bold tw-text-md lg:tw-text-base tw-text-left;
    }
    .t-input-text {
        @apply tw-overflow-hidden tw-rounded-md focus:tw-outline-none tw-ring-1 dark:tw-ring-neutral-600 tw-shadow-md tw-flex tw-flex-row tw-justify-between tw-justify-items-stretch tw-content-center tw-gap-1 tw-px-1 tw-place-content-stretch tw-ring-neutral-300;
    }
    .t-input-text.t-disabled {
        @apply tw-bg-gray-200 tw-text-gray-400 dark:tw-bg-slate-900 dark:tw-text-slate-500 hover:tw-cursor-not-allowed tw-ring-neutral-300;
    }
    .t-input-root {
        @apply tw-bg-neutral-600/10 dark:tw-bg-slate-800;
    }
    .t-input-text.t-success {
    }
    .t-input-text.danger {
        @apply tw-text-red-500 dark:tw-text-red-400;
    }
    .t-input.t-danger {
    }
    .t-input.t-success {
    }
    .t-input.t-disabled {
    }
</style>

<style lang="scss" module="colorscheme">
    .auto {
        @apply tw-bg-neutral-500/5 dark:tw-bg-slate-900;
    }
    .outline {
    }
    .daynight {
        @apply tw-bg-neutral-500/5 dark:tw-bg-slate-900 tw-text-black dark:tw-text-white;
    }
    .light {
        @apply tw-bg-neutral-500/5 tw-text-black;
        .light-auto {
            @apply dark:tw-bg-neutral-500/75;
        }
    }
    .dark,
    .dark-auto {
        @apply tw-bg-slate-800 tw-text-white dark:tw-bg-slate-900;
    }
</style>
