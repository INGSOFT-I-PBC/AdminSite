<script setup lang="ts">
    import { ref } from 'vue'
    import EButton from '@components/custom/EButton.vue'

    const message = ref('TODO: Make this view')
</script>

<template>
    <div>
        <h1>{{ message }}</h1>
        <h2>Esto es un ejemplo derole</h2>
        <EButton type="secondary">
            New Role +
        </EButton>
    </div>
</template>
