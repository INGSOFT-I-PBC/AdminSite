<script setup lang="ts">
    defineProps({
        theme: {
            type: String,
            default:
                'tw-bg-slate-50 dark:tw-bg-gray-800',
        },
        cardTheme: {
            type: String,
            default:
                'tw-bg-slate-50 dark:tw-bg-gray-800',
        },
    })
</script>

<template>
    <div
        :class="theme"
        class="tw-rounded-lg tw-ring-1 tw-ring-slate-300 tw-p-4 tw-shadow-md dark:tw-ring-0 dark:tw-ring-slate-700 tw-text-black dark:tw-text-slate-200 tw-flex tw-flex-col tw-gap-2">
        <slot />
    </div>
</template>
