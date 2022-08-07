<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
    import { ref } from 'vue'

    const message = ref('TODO: Make this view')
</script>

<template>
    <div>
        <h1>{{ message }}</h1>
        <h2>
            El recurso solicitado no se ha
            encontrado
        </h2>
    </div>
</template>
