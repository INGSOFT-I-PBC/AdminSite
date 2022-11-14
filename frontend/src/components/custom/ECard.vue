<script setup lang="ts">
    import type { CardStyle, Elevation } from '@components-types'

    import type { PropType } from 'vue'

    defineProps({
        theme: {
            type: String as PropType<CardStyle>,
            default: 'daynigth',
        },
        cardElevation: {
            type: String as PropType<Elevation>,
            default: 'md',
        },
        cardTheme: {
            type: String,
            default: 'tw-bg-slate-50 dark:tw-bg-gray-800',
        },
        clickable: {
            type: Boolean,
            default: false,
        },
    })
</script>

<template>
    <div class="t-card" :class="[card[theme], elevation[cardElevation]]">
        <slot />
    </div>
</template>

<style lang="scss" module="elevation">
    .md {
        @apply tw-shadow-md;
    }
    .sm {
        @apply tw-shadow-sm;
    }
    .lg {
        @apply tw-shadow-lg;
    }
    .xl {
        @apply tw-shadow-xl;
    }
    .xxl {
        @apply tw-shadow-2xl;
    }
    .default {
        @apply tw-shadow;
    }
</style>

<style lang="scss" module="card">
    .daynigth {
        @apply tw-bg-slate-50 dark:tw-bg-gray-800 dark:tw-text-gray-100;
    }
    .day {
        @apply tw-bg-slate-50;
    }
    .nigth {
        @apply tw-bg-gray-900;
    }
    .primary {
        @apply tw-bg-primary;
    }
    .primary-dark {
        @apply tw-bg-primary-dark;
    }
    .primary-light {
        @apply tw-bg-primary-light;
    }
    .secondary {
        @apply tw-bg-secondary dark:tw-bg-secondary-night tw-text-white;
    }
    .secondary-light {
        @apply tw-bg-secondary-light dark:tw-bg-secondary-night-light;
    }
    .secondary-dark {
        @apply tw-bg-secondary-dark dark:tw-bg-secondary-night-dark;
    }
    .secondary,
    .secondary-dark,
    .secondary-light {
        > h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            @apply tw-text-white;
        }
        > p,
        span,
        small {
            color: white;
        }
    }
    .outline {
        @apply tw-bg-transparent;
    }
</style>

<style lang="scss">
    .t-card {
        @apply sm:tw-rounded-lg tw-ring-1 tw-ring-slate-300 tw-p-4 dark:tw-ring-0 dark:tw-ring-slate-700 tw-text-black dark:tw-text-slate-200 tw-flex tw-flex-col tw-gap-2;
    }
    .t-card > .t-card {
        @apply dark:tw-bg-black/10 dark:tw-ring-1 dark:tw-ring-slate-900;
    }
</style>
