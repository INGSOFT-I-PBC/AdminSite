<script lang="ts" setup>
    import { computed } from 'vue'

    const props = defineProps({
        indeterminate: {
            type: Boolean,
            default: true,
        },
    })

    const classes = computed(() => [
        't-load-bar',
        {
            't-indeterminate': props.indeterminate,
        },
    ])
</script>

<template>
    <div :class="classes"></div>
</template>
<style lang="scss">
    .t-load-bar {
        width: 90%;
        margin: 0 auto;
        height: 0.33rem;
        @apply tw-bg-primary-light dark:tw-bg-slate-900/95;
        transition: all 300ms ease-in-out;
    }
    .t-load-bar:before,
    .t-load-bar:after {
        content: '';
        display: block;
        height: 100%;
        position: absolute;
        border-radius: 3px;
    }
    .t-indeterminate:before,
    .t-indeterminate:after {
        animation: motion 3s infinite ease;
    }
    .t-load-bar:before,
    .t-load-bar:after {
        @apply tw-bg-slate-700 dark:tw-bg-primary-light/75;
    }
    // .t-load-bar:before {
    //     animation-delay: 250ms;
    //     @apply tw-bg-secondary/40 dark:tw-bg-amber-300;
    // }
    .t-load-bar:after {
        animation-delay: 330ms;
    }

    @keyframes motion {
        0% {
            left: 0;
            width: 0;
        }
        20% {
            left: 20%;
            width: 60%;
        }
        40% {
            left: 30%;
            width: 20%;
        }
        60% {
            left: 60%;
            width: 10%;
        }
        80% {
            left: 70%;
            width: 30%;
        }
        100% {
            left: 100%;
            width: 0;
        }
    }
</style>
