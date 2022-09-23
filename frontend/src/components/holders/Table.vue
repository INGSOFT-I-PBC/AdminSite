<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
    import { TableHeaderSettings } from './definitions/table'

    defineProps({
        header: {
            type: TableHeaderSettings,
            require: true,
            default: () => ({} as TableHeaderSettings),
        },
        rows: {
            type: Array<unknown>,

            default: [],
        },
        columns: {
            type: Array<unknown>,
            default: [],
        },
    })
</script>

<template>
    <div class="tw-overflow-x-auto">
        <table class="tw-min-w-full">
            <thead class="tw-overflow-hidden tw-bg-zinc-300 tw-border-b">
                <tr>
                    <template v-for="(cfg, idx) of header?.headers" :key="idx">
                        <th :class="cfg.style ? cfg.style : 'tw-px-2 tw-py-3'">
                            <slot name="head-cell">
                                <span class="tw-text-center">{{ cfg.label }}</span>
                            </slot>
                        </th>
                    </template>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(data, idx) of header?.rows" :key="idx">
                    <td
                        class="tw-px-2 tw-py-3"
                        v-for="(column, cidx) of header?.headers"
                        :key="cidx">
                        <slot
                            name="body-cell"
                            :cell-data="
                                column?.morphFunc ? column.morphFunc(data) : data
                            "
                            :column-data="column"
                            :row-idx="idx"
                            :col-idx="cidx">
                            <span>
                                {{
                                    `${
                                        (column?.morphFunc
                                            ? column.morphFunc(data)
                                            : (data as any))[
                                            column.attribute || ''
                                        ] || ''
                                    }`
                                }}
                            </span>
                        </slot>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
