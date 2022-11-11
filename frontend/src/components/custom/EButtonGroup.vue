<template>
    <div class="t-button-group">
        <slot></slot>
    </div>
</template>

<style lang="scss">
    .t-button-group {
        display: flex;
        border-radius: theme('borderRadius.md');
        overflow: hidden;
        width: fit-content;
        max-width: fit-content;

        > .t-button {
            border-radius: 0 !important;
            margin: 0 !important;
        }
    }
</style>
