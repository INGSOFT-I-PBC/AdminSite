<script setup lang="ts">
    import type { text } from '@fortawesome/fontawesome-svg-core'
    import { computed } from 'vue'

    const props = defineProps({
        modelValue: {
            type: String,
            default: '',
        },
        modelModifiers: {
            default: () => ({} as any),
        },
        type: {
            type: String,
            default: 'text',
        },
        label: {
            type: String,
        },
        placeholder: {
            type: String,
            default: '',
        },
        labelStyle: {
            type: String,
            default: 'tw-font-bold tw-text-smd',
        },
        infoLabel: {
            type: String,
        },
        infoStyle: {
            type: String,
            default: 'tw-italic tw-text-tiny',
        },
        status: {
            type: Boolean || null,
            default: null,
        },
        infoStatus: {
            type: String,
            default: 'normal',
        },
        disabled: {
            type: Boolean,
            default: false,
        },
    })

    const emit = defineEmits([
        'update:modelValue',
    ])

    const infoClass = computed(() => {
        let styles = `${props.infoStyle || ''} `
        switch (props.infoStatus) {
            case 'danger':
                styles +=
                    'tw-text-red-700 dark:tw-text-red-500'
                break
            case 'warning':
                styles +=
                    'tw-text-amber-800 dark:tw-text-yellow-500'
                break
            case 'success':
                styles +=
                    'tw-text-green-600 dark:tw-text-emerald-500'
                break
            default: // No apply styles
        }
        return styles
    })

    const inputClass = computed(() => {
        if (props.disabled) {
            return 'tw-bg-gray-200 tw-text-gray-400 dark:tw-bg-slate-900 dark:tw-text-slate-500 hover:tw-cursor-not-allowed tw-ring-neutral-300'
        }
        let classes =
            'tw-bg-neutral-100 dark:tw-bg-slate-800 '
        if (props.status === true) {
            classes +=
                'focus:tw-outline-teal-500 tw-ring-teal-400 dark:tw-ring-emerald-600 focus:tw-outline-1 tw-text-green-700 dark:tw-text-green-300'
        } else if (props.status === false) {
            classes +=
                'focus:tw-outline-rose-600 tw-ring-red-600 dark:tw-ring-red-700 focus:tw-outline-1 tw-text-red-500 dark:tw-text-400'
        } else {
            classes +=
                'focus:tw-outline-cyan-600 tw-ring-neutral-300 dark:focus:tw-outline-sky-600 tw-text-black dark:tw-text-neutral-300'
        }
        return classes
    })

    function interactionStart(event: Event) {
        const target =
            event.target as HTMLButtonElement
        if (props.disabled) {
            event.preventDefault()
            target.blur()
        }
    }

    function emitValue(e: Event) {
        let value = (e.target as HTMLInputElement)
            .value
        if (props.modelModifiers?.capitalize) {
            value =
                value.charAt(0).toUpperCase() +
                value.slice(1)
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
        emit('update:modelValue', value)
    }
</script>

<template>
    <div class="tw-flex tw-flex-col">
        <label v-if="label" :class="labelStyle">
            {{ label }}
        </label>
        <input
            @mousedown="interactionStart"
            @keydown="interactionStart"
            :value="modelValue"
            @input="emitValue"
            :placeholder="placeholder"
            class="tw-py-1 lg:tw-py-1.5 tw-px-2 tw-overflow-hidden tw-rounded-md focus:tw-outline-none tw-ring-2 dark:tw-ring-neutral-600 tw-shadow-md"
            :class="inputClass"
            :type="type" />
        <slot name="info-label">
            <small :class="infoClass">
                {{ infoLabel }}
            </small>
        </slot>
    </div>
</template>
