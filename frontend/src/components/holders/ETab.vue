<script setup lang="ts">
    import { Tab, TabGroup, TabList, TabPanels } from '@headlessui/vue'

    const props = defineProps({
        verticalTabs: {
            type: Boolean,
            default: false,
        },
        defaultIndex: {
            type: Number,
            default: 0,
        },
        tabs: {
            type: Array<string>,
            default: ['Tab1'],
        },
        selectedTab: {
            type: Number,
            default: 0,
        },
    })
    const emits = defineEmits(['change', 'update:selectedTab'])

    function tabChange(tabIndex: number) {
        emits('update:selectedTab', tabIndex)
    }
</script>

<template>
    <TabGroup
        :vertical="verticalTabs"
        :default-index="props.defaultIndex"
        @change="tabChange">
        <TabList class="tw-tablist">
            <Tab
                class="tw-tab"
                v-for="(tabTitle, index) in tabs"
                :key="index"
                as="template"
                v-slot="{ selected }">
                <slot
                    name="tab"
                    :tab-title="tabTitle"
                    :tab-index="index"
                    :selected="selected">
                    <button
                        class="tw-tab-button"
                        :class="{ 'tw-tab-selected': selected }">
                        {{ tabTitle }}
                    </button>
                </slot>
            </Tab>
        </TabList>
        <TabPanels>
            <slot />
        </TabPanels>
    </TabGroup>
</template>

<style lang="scss">
    .tw-tablist {
        @apply tw-flex tw-space-x-2 tw-rounded-xl tw-bg-on-primary/5 tw-p-1;
    }
    .tw-rounded-button {
        @apply tw-rounded-md;
    }
    .tw-tab {
        @apply tw-py-1.5 tw-px-0.5;
    }
    .tw-tab-button {
        @apply hover:tw-ring-1 hover:tw-ring-primary-dark/80 tw-px-4 tw-transition-all tw-duration-150 tw-rounded-md tw-outline-none;
    }
    .tw-tab-selected {
        @apply tw-bg-primary/80 hover:tw-bg-primary tw-transition-all tw-duration-300 tw-border-transparent hover:tw-shadow-xl;
    }
</style>
