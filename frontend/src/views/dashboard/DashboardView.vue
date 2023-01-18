<script setup lang="ts">
    import CardBoxWidget from '@/components/charts/CardBoxWidget.vue'
    import * as chartConfig from '@/components/charts/chart.config'

    import { computed, onMounted, ref } from 'vue'

    const chartData: any = ref(null)

    const fillChartData = () => {
        chartData.value = chartConfig.sampleChartData()
    }

    onMounted(() => {
        fillChartData()
    })
</script>

<template>
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-3 mb-6">
        <CardBoxWidget
            trend="12%"
            trend-type="down"
            color="text-blue-500"
            :number="7770"
            prefix="$"
            label="Sales" />
    </div>
</template>
