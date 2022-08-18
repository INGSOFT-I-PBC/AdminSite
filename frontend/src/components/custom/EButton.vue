<template>
    <button
        type="button"
        @click="buttonClick"
        @mouseenter="buttonHover"
        class="hover:tw-transition-all focus:tw-shadow-sm tw-font-bold tw-ease-in-out tw-py-1.5 tw-px-4 focus:tw-outline-none tw-rounded-md hover:tw-shadow-lg tw-shadow-md"
        :class="style"
        @mouseup="mouseStopInteraction"
        @mouseleave="mouseStopInteraction">
        <FontAwesomeIcon
            v-if="leftIcon"
            :icon="leftIcon" />
        <slot>Button</slot>
        <FontAwesomeIcon
            v-if="rightIcon"
            :icon="rightIcon" />
    </button>
</template>

<script setup lang="ts">
    import { computed } from 'vue'
    const emit = defineEmits(['click', 'hover'])
    const props = defineProps({
        type: {
            type: String,
            default: 'primary',
            validator(value: string) {
                return [
                    'primary',
                    'secondary',
                    'outline',
                    'cancel',
                    'success',
                    'blank',
                ].includes(value)
            },
        },
        leftIcon: {
            type: String,
            default: null,
        },
        rightIcon: {
            type: String,
            default: null,
        },
        disabled: {
            type: Boolean,
            default: false,
        },
    })

    const style = computed(() => {
        let classes = ''
        const { disabled } = props
        switch (props.type) {
            case 'primary':
                classes +=
                    'tw-bg-primary hover:tw-bg-primary-dark focus:tw-bg-primary-dark tw-text-on-primary dark:tw-bg-primary-night dark:hover:tw-bg-primary-night-dark dark:focus:tw-bg-primary-night-dark'
                break
            case 'outline':
                classes =
                    'tw-bg-transparent focus:tw-bg-transparent tw-ring-2 tw-ring-secondary focus:tw-bg-neutral-200'
                break
            case 'success':
                classes =
                    'tw-bg-green-500 dark:tw-bg-emerald-700 hover:tw-bg-green-600 focus:tw-bg-green-600'
                break
            case 'cancel':
                classes =
                    'tw-bg-rose-600 dark:tw-bg-red-800 focus:tw-bg-rose-700 hover:tw-bg-rose-700 tw-text-white'
                break
            case 'blank':
                break
            default:
                classes +=
                    'tw-bg-secondary hover:tw-bg-secondary-light focus:tw-bg-secondary-light tw-text-on-secondary dark:tw-bg-secondary-night dark:hover:tw-bg-secondary-night-dark dark:focus:tw-bg-secondary-night-dark dark:hover:tw-ring-1 dark:hover:tw-ring-slate-700'
        }
        if (disabled)
            classes =
                'tw-bg-neutral-300 dark:tw-bg-neutral-500 hover:tw-drop hover:tw-shadow-md hover:tw-cursor-not-allowed tw-text-neutral-500 dark:tw-text-neutral-800'
        return classes
        // return `bg-${props.type} text-on-${props.type} px-4 py-1 rounded hover:bg-gray-500 bg-primary`
    })

    function buttonClick() {
        if (!props.disabled) emit('click')
    }
    function buttonHover() {
        emit('hover')
    }
    function mouseStopInteraction(
        event: MouseEvent
    ) {
        const element =
            event.target as HTMLButtonElement
        element.blur()
    }
</script>
