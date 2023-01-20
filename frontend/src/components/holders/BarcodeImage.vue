<template>
    <component ref="element" :is="tag" />
</template>

<script lang="ts" setup>
    import JsBarcode from 'jsbarcode'

    import { type PropType, onMounted, watch } from 'vue'

    type SupportedBarcodes =
        | 'code128'
        | 'code128A'
        | 'code128B'
        | 'code128C'
        | 'ean-13'
        | 'ean-8'
        | 'ean-5'
        | 'ean-2'
        | 'upc-a'
        | 'upc-b'
        | 'code39'
        | 'itf'
        | 'itf-14'
        | 'msi10'
        | 'msi11'
        | 'msi1010'
        | 'msi1110'
        | 'pharmacode'
        | 'codabar'
    type Configuration = {
        code: string
        type: SupportedBarcodes
        tag: 'svg' | 'canvas' | 'img'
        lineColor: string
        width: number
        height: number
        displayValue: boolean
        options: JsBarcode.Options | null
    }
    const props = defineProps({
        code: {
            type: String,
            required: true,
        },
        type: {
            type: String as PropType<SupportedBarcodes>,
            default: '',
        },
        tag: {
            type: String as PropType<'svg' | 'canvas' | 'img'>,
            default: 'canvas',
        },
        lineColor: {
            type: String,
            default: '#000000',
        },
        width: {
            type: Number as PropType<number>,
            default: 2,
        },
        height: {
            type: Number as PropType<number>,
            default: 100,
        },
        displayValue: {
            type: Boolean,
            default: true,
        },
        options: {
            type: Object as PropType<JsBarcode.Options | null>,
            default: null,
        },
    })

    const element = ref()

    watch(
        () => props,
        (first, second) => {
            drawBarcode(second as Configuration)
        }
    )

    function drawBarcode(cfg: Configuration) {
        JsBarcode(element.value, cfg.code, {
            format: cfg.type,
            width: cfg.width,
            height: cfg.height,
            displayValue: cfg.displayValue,
            lineColor: cfg.lineColor,
            ...(cfg.options ?? {}),
        })
        console.debug('asdfs')
    }

    onMounted(() => {
        drawBarcode(props as Configuration)
    })
</script>
