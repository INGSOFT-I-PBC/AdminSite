<script lang="ts" setup>
    import { computed, type Prop, type PropType } from 'vue'
    import type { TableColumnish, NormalizedHeader } from '@components-types'
    import { isTableColumn } from '@/components/types'

    const props = defineProps({
        hover: Boolean,
        dark: Boolean,
        striped: Boolean,
        columns: {
            type: Object as PropType<TableColumnish[]>,
            default: [],
            required: true,
        },
        rows: {
            type: Object as PropType<string[]>,
            default: [],
        },
    })

    const bTableStyle = computed(() => ({
        'table-hover': props.hover,
        'table-dark': props.dark,
        'table-striped': props.striped,
    }))

    const headerNormalized = computed((): NormalizedHeader[] => {
        if (!props.columns) return []
        return props.columns.map(col => ({
            label: isTableColumn(col) ? col.label : col,
            field: isTableColumn(col) ? col.field : col,
            content: col,
        }))
    })
</script>

<template>
    <table class="table" :class="bTableStyle">
        <thead>
            <tr>
                <th v-for="column in headerNormalized" :key="column.label">
                    <slot name="header" :columnData="column">
                        {{ column.label }}
                    </slot>
                </th>
            </tr>
        </thead>
    </table>
</template>

<style></style>
