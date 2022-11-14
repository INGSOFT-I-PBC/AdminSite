<script lang="ts" setup>
    import type { BorderRadius } from '@components-types'

    import type { PropType } from 'vue'

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
    <EOverlay :rounded="rounded" :show="show">
        <template #content>
            <div
                class="tw-flex tw-flex-row fit tw-items-center tw-relative tw-top-1/2 tw-left-1/2 tw-right-1/2 tw-content-center tw-self-center tw-z-10">
                <FontAwesomeLayers fixed-width>
                    <FontAwesomeIcon
                        class="tw-fill-white"
                        icon="spinner"
                        inverse
                        pull="left"
                        size="5x"
                        spin />
                    <!--                    class="fa-4x"-->
                    <FontAwesomeLayersText
                        :style="{
                            color: 'white',
                            marginTop: '3rem',
                            align: 'center',
                        }"
                        :value="message"
                        transform="down-10 grow-6" />
                </FontAwesomeLayers>
            </div>
        </template>
        <template #default>
            <slot />
        </template>
    </EOverlay>
</template>
