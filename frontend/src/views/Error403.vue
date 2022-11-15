<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
    import { useRoute, useRouter } from 'vue-router'

    import EButton from '../components/custom/EButton.vue'

    const router = useRouter()

    function redirectHome() {
        const origin = useRoute()?.redirectedFrom
        let redirectPath = origin?.path || '/'
        if (origin?.path === '/error-403' || origin?.path === '/error-404') {
            redirectPath = '/'
        }
        router.push({ path: redirectPath })
    }
</script>

<template>
    <div
        class="tw-h-screen tw-w-screen tw-flex tw-flex-col tw-justify-center tw-justify-items-center tw-text-center tw-items-center">
        <h1
            class="tw-text-9xl tw-font-bold tw-p-1 dark:tw-text-pink-700 dark:tw-hover:text-pink-500 tw-text-amber-600 tw-italic tw-drop-shadow-md hover:tw-transform-gpu tw-transition-all tw-ease-in-out hover:tw-scale-110 tw-font-mono tw-max-w-fit tw-max-h-fit">
            <FontAwesomeIcon class="tw-text-7xl" icon="fa-lock" />
            403
        </h1>
        <h3
            class="tw-text-3xl tw-font-bold tw-p-3 tw-text-amber-700 dark:tw-text-amber-500">
            Sin autorización
        </h3>
        <span
            class="lg:tw-w-1/2 tw-mx-10 dark:tw-font-bold dark:tw-text-gray-400">
            Lo sentimos, no está autorizado a visualizar el recurso
            solicitado.<br />
            Pero puedes seguir hacia la página principal.
        </span>
        <div class="tw-p-5">
            <EButton
                class="dark:tw-bg-teal-800 dark:tw-text-white dark:tw-font-bold dark:hover:tw-bg-teal-600 hover:tw-scale-105 hover:tw-shadow-inner"
                @click="redirectHome"
                >Volver al Inicio</EButton
            >
        </div>
    </div>
</template>
