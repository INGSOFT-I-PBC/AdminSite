<script setup lang="ts">
    import ECard from '../components/custom/ECard.vue'
    import EButton from '../components/custom/EButton.vue'
    import { useAuthStore } from '@store'
    import { inject } from 'vue'
    import type { Router } from 'vue-router'

    useAuthStore().refreshToken()
    const router = inject('router') as Router
    function goToAdmin() {
        router.push('/dashboard')
        console.log('asdf')
    }
</script>

<template>
    <main>
        <ECard class="tw-bg-gray-900">
            <h1
                class="tw-align-center tw-text-center tw-text-xl lg:tw-text-2xl tw-font-bold tw-text-primary-dark">
                Bienvenido
            </h1>
            <h2
                class="tw-align-center tw-text-center tw-text-white tw-text-2xl lg:tw-text-3xl tw-font-bold">
                User name
            </h2>
            <p
                class="tw-text-primary-light tw-justify-center tw-text-center tw-text-md lg:tw-text-lg">
                Para comenzar a utilizar la
                plataforma, selecciona alguna
                opción del menú al lado izquierdo.
            </p>
        </ECard>
    </main>
</template>
