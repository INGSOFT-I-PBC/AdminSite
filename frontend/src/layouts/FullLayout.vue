<template>
    <div class="fullscreen-layout">
        <slot></slot>
    </div>
</template>
<style lang="scss">
    #app > div.fullscreen-layout {
        @apply tw-justify-center tw-items-center tw-overflow-y-auto tw-flex;
    }
</style>
