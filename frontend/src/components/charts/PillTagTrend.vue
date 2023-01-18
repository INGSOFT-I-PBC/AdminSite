<script setup lang="ts">
    import PillTag from '@/components/charts/PillTag.vue'

    import { computed } from 'vue'

    const props = defineProps({
        trend: {
            type: String,
            required: true,
        },
        trendType: {
            type: String,
            default: null,
        },
        small: Boolean,
    })

    const trendStyle = computed(() => {
        if (props.trendType === 'up') {
            return {
                style: 'success',
            }
        }

        if (props.trendType === 'down') {
            return {
                style: 'danger',
            }
        }

        if (props.trendType === 'alert') {
            return {
                style: 'warning',
            }
        }

        return {
            style: 'info',
        }
    })
</script>

<template>
    <PillTag :label="trend" :color="trendStyle.style" :small="small" />
</template>
