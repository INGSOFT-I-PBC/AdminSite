<template>
    <button
        type="button"
        @click="buttonClick"
        @mouseenter="buttonHover"
        :class="style">
        <slot>Button</slot>
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
                ].includes(value)
            },
        },
    })

    const style = computed(() => {
        let classes =
            'hover:transition ease-in-out py-1 px-3 rounded-md hover:shadow-lg shadow-md '
        switch (props.type) {
            case 'primary':
                classes +=
                    'bg-primary hover:bg-primary-dark text-on-primary dark:bg-primary-night dark:hover:bg-primary-night-dark'
                break
            default:
                classes +=
                    'bg-secondary hover:bg-secondary-light text-on-secondary dark:bg-secondary-night dark:hover:bg-secondary-night-dark dark:hover:ring-1 dark:hover:ring-slate-700'
        }
        return classes
        // return `bg-${props.type} text-on-${props.type} px-4 py-1 rounded hover:bg-gray-500 bg-primary`
    })

    function buttonClick() {
        emit('click')
    }
    function buttonHover() {
        emit('hover')
    }
</script>
