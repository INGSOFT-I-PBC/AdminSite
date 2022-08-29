<script setup lang="ts">
    import { computed } from 'vue'
    const instance = ref()
    const childsMenuItems = computed(() => {

    })
</script>

<template>
    <Transition
        leave-active-class="tw-transition-all tw-duration-200 tw-ease-in"
        leave-from-class="tw-opacity-100"
        leave-to-class="tw-opacity-0">
        <ul ref="instance">
            <slot />
        </ul>
    </Transition>
</template>
