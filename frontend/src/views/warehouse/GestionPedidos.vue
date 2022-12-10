<script setup lang="ts">
    import { WaitOverlay } from '@custom-components'

    const showWaitOverlay = ref(true)
</script>

<template>
    <WaitOverlay :show="showWaitOverlay"> </WaitOverlay>
</template>
<style lang="scss">
    h1.title {
        @apply tw-text-2xl tw-text-black dark:tw-text-neutral-100;
    }

    .smaller-btn-group {
        --bs-list-group-border-width: 1px;
        --bs-list-group-border-radius: 0.25rem;
        --bs-list-group-item-padding-x: 0.8rem;
        --bs-list-group-item-padding-y: 0.3rem;
    }

    .table {
        > thead {
            @apply tw-bg-secondary tw-text-white tw-font-bold tw-text-sm;
        }

        > tbody {
            @apply tw-text-sm;
        }

        @media (prefers-color-scheme: dark) {
            color: white !important;
            --bs-table-striped-color: theme(colors.zinc.400);
            --bs-table-hover-color: theme('colors.primary.light');
            --bs-table-hover-bg: theme(colors.primary.light / 15%);
        }
    }
</style>
