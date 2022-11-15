<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
    import { type PropType, computed } from 'vue'

    const props = defineProps({
        size: {
            type: String as PropType<
                | 'sm'
                | 'md'
                | 'lg'
                | 'xl'
                | '2xl'
                | '3xl'
                | '4xl'
                | '5xl'
                | '6xl'
                | '7xl'
                | '8xl'
                | '9xl'
                | '10xl'
                | '11xl'
            >,
            default: 'xl',
            validate: (option: string) =>
                [
                    'sm',
                    'md',
                    'lg',
                    'xl',
                    ...Array.from(Array(9).keys()).map(
                        sizeIdx => `${sizeIdx + 2}xl`
                    ),
                ].includes(option),
        },
        weight: {
            type: String,
            default: 'bold',
            validate: (weight: string) =>
                [
                    'normal',
                    'bold',
                    'italic',
                    'bold-italic',
                    'semibold',
                ].includes(weight),
        },
        textColorClass: {
            type: String,
            default: 'tw-text-slate-700 dark:tw-text-slate-300',
        },
    })

    const fontSize = computed(() => {
        switch (props.size) {
            case 'sm':
                return 'tw-text-sm'
            case 'md':
                return 'tw-text-md'
            case 'lg':
                return 'tw-text-lg'
            case '2xl':
                return 'tw-text-2xl'
            case '3xl':
                return 'tw-text-3xl'
            case '4xl':
                return 'tw-text-4xl'
            case '5xl':
                return 'tw-text-5xl'
            case '6xl':
                return 'tw-text-6xl'
            case '7xl':
                return 'tw-text-7xl'
            case '8xl':
                return 'tw-text-8xl'
            case '9xl':
                return 'tw-text-9xl'
            default:
                return 'tw-text-xl'
        }
    })
    const fontWeight = computed(() => {
        switch (props.weight) {
            case 'normal':
                return 'tw-font-normal'
            case 'semibold':
                return 'tw-font-semibold'
            case 'bold-italic':
                return 'tw-font-bold tw-italic'
            case 'italic':
                return 'tw-italic'
            default:
                return 'tw-font-bold'
        }
    })

    const joinedClasses = computed(
        () => `${fontSize.value} ${fontWeight.value} ${props.textColorClass}`
    )
</script>

<template>
    <h2 class="" :class="joinedClasses">
        <slot />
    </h2>
</template>
