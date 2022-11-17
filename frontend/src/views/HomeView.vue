<script setup lang="ts">
    import { useAuthStore } from '@/store/auth'

    import ECard from '../components/custom/ECard.vue'

    const authStore = useAuthStore()
</script>

<template>
    <main>
        <ECard theme="secondary" card-elevation="xl">
            <h1
                class="tw-align-center tw-text-center tw-text-xl lg:tw-text-2xl tw-font-bold tw-text-primary-dark">
                Bienvenido
            </h1>
            <h2
                class="tw-align-center tw-text-center tw-text-white tw-text-2xl lg:tw-text-3xl tw-font-bold">
                {{ authStore.userData?.name }}
            </h2>
            <p
                class="tw-text-primary-light tw-justify-center tw-text-center tw-text-md lg:tw-text-lg">
                Para comenzar a utilizar la plataforma, selecciona alguna opción
                del menú al lado izquierdo.
            </p>
        </ECard>
    </main>
</template>
