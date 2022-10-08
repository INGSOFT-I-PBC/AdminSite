<script setup lang="ts">
    import type { BorderRadius } from '@components-types'
    import type { PropType } from 'vue'
    import {
        FontAwesomeLayers,
        FontAwesomeLayersText,
    } from '@fortawesome/vue-fontawesome'
    import EOverlay from './EOverlay.vue'
    defineProps({
        show: {
            type: Boolean,
            default: false,
        },
        rounded: {
            type: String as PropType<BorderRadius>,
            default: 'lg',
        },
        message: {
            type: String,
            default: 'Cargando, espere...',
        },
    })
</script>
<template>
    <EOverlay :show="show" :rounded="rounded">
        <template #content>
            <div
                class="tw-flex tw-flex-row fit tw-items-center tw-relative tw-top-1/2 tw-left-1/2 tw-right-1/2 tw-content-center tw-self-center">
                <FontAwesomeLayers class="fa-4x">
                    <FontAwesomeIcon
                        class="tw-fill-white"
                        icon="spinner"
                        spin
                        inverse
                        pull="left" />
                    <FontAwesomeLayersText
                        transform="down-10 shrink-8"
                        :style="{ color: 'white', marginTop: '3rem' }"
                        :value="message" />
                </FontAwesomeLayers>
            </div>
        </template>
        <template #default>
            <slot />
        </template>
    </EOverlay>
</template>
