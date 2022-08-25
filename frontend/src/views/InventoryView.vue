<script setup lang="ts">
    import { ref } from 'vue'
    import EButton from '@components/custom/EButton.vue'

    const message = ref('TODO: Make this view')
</script>

<template>
    <div>
        <h1>{{ message }}</h1>
        <h2>Esto es un ejemplo de inventario</h2>
        <EButton type="secondary"> + Add Product </EButton>
    </div>
</template>
