<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div>
        <h1>Error403</h1>
        <p>
            No esta autorizado para visualizar el
            recurso solicitado
        </p>
        <EButton @click="goToHome">Regresar al inicio</EButton>
    </div>
</template>

<script setup lang="ts">
    import EButton from '@components/custom/EButton.vue'
    import { useRouter } from 'vue-router'
    const router = useRouter()
    function goToHome() {
      router.push({ path: '/' })
    }
</script>

<style scoped>

</style>
