<script setup lang="ts">
    import BaseIcon from '@/components/charts/BaseIcon.vue'
    import CardBox from '@/components/charts/CardBox.vue'
    import NumberDynamic from '@/components/charts/NumberDynamic.vue'
    import PillTagTrend from '@/components/charts/PillTagTrend.vue'

    defineProps({
        number: {
            type: Number,
            default: 0,
        },
        icon: {
            type: String,
            default: null,
        },
        prefix: {
            type: String,
            default: null,
        },
        suffix: {
            type: String,
            default: null,
        },
        label: {
            type: String,
            default: null,
        },
        color: {
            type: String,
            default: null,
        },
        trend: {
            type: String,
            default: null,
        },
        trendType: {
            type: String,
            default: null,
        },
    })
</script>

<template>
    <CardBox>
        <PillTagTrend :trend="trend" :trend-type="trendType" small />

        <div>
            <h3 class="text-lg leading-tight text-gray-500 dark:text-slate-400">
                {{ label }}
            </h3>
            <h1 class="text-3xl leading-tight font-semibold">
                <NumberDynamic
                    :value="number"
                    :prefix="prefix"
                    :suffix="suffix" />
            </h1>
        </div>
        <BaseIcon
            v-if="icon"
            :path="icon"
            size="48"
            w=""
            h="h-16"
            :class="color" />
    </CardBox>
</template>
