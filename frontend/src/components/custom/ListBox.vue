<script lang="ts" setup>
    import {
        Listbox,
        ListboxButton,
        ListboxOption,
        ListboxOptions,
    } from '@headlessui/vue'

    import { type PropType, computed } from 'vue'
    import VueFeather from 'vue-feather'

    type ValidListboxItem = ListboxItem & Record<string | number, unknown>
    const props = defineProps({
        modelValue: {
            type: Object as PropType<ValidListboxItem>,
            default: null,
        },
        topLabel: {
            type: String,
            default: null,
        },
        label: {
            type: String,
            default: 'label',
        },
        options: {
            type: Array as PropType<ValidListboxItem[]>,
            default: () => [],
            validator: (value: Optional<unknown>) =>
                (value ?? null) !== null && Array.isArray(value),
        },
        placeholder: {
            type: String,
            default: '',
        },
    })
    const emit = defineEmits(['update:modelValue', 'change'])
    const selectedItem = computed({
        get() {
            return props.modelValue
        },
        set(value) {
            emit('update:modelValue', value)
            emit('change', value)
        },
    })
</script>

<template>
    <Listbox v-model="selectedItem">
        <div class="tw-relative">
            <label
                v-if="topLabel"
                class-asdf="tw-pl-0.5 tw-font-bold tw-text-md lg:tw-text-base"
                class="form-label">
                {{ topLabel }}
            </label>
            <ListboxButton class="t-listbox-button">
                <span
                    v-if="modelValue && modelValue[label]"
                    class="tw-block tw-truncate tw-max-h-fit">
                    <slot :data="modelValue[label]" name="content-label">
                        {{ modelValue ? modelValue[label] : '' }}
                        &ZeroWidthSpace;
                    </slot>
                </span>
                <span
                    v-else
                    class="tw-block tw-truncate tw-max-h-fit tw-text-black/50 dark:tw-text-white/60">
                    <slot name="placeholder">
                        {{ placeholder }} &ZeroWidthSpace;
                    </slot>
                </span>
                <span
                    class="tw-pointer-events-none tw-absolute tw-inset-y-0 tw-right-0 tw-flex tw-items-center tw-pr-2">
                    <VueFeather type="chevron-down" />
                </span>
            </ListboxButton>

            <Transition
                class=""
                enter-active-class="tw-transition-all tw-duration-150 tw-ease-in-out"
                enter-from-class="tw-h-0 tw-opacity-0"
                enter-to-class="tw-opacity-100 tw-h-0 tw-h-96"
                leave-active-class="tw-transition tw-duration-150 tw-ease-in"
                leave-from-class="tw-opacity-100 "
                leave-to-class="tw-opacity-0 tw-translate-y-0">
                <ListboxOptions class="t-listbox-options">
                    <span
                        v-if="props.options?.length === 0"
                        class="tw-py-6 tw-px-3 tw-text-md tw-text-slate-600 dark:tw-text-zinc-300">
                        No item available
                    </span>
                    <!-- :class="[
                                active
                                    ? 'tw-bg-amber-100 tw-text-amber-900 dark:tw-bg-slate-900/40 dark:tw-text-amber-200/70'
                                    : 'tw-text-gray-900 dark:tw-text-gray-300',
                            ]" -->
                    <ListboxOption
                        v-for="(item, idx) in options"
                        :key="idx"
                        v-slot="{ active, selected }"
                        :value="item"
                        as="template">
                        <li
                            :class="{
                                't-item-active': active,
                            }"
                            class="t-listbox-item">
                            <span
                                :class="[
                                    selected
                                        ? 'tw-font-medium'
                                        : 'tw-font-normal',
                                ]"
                                class="t-listbox-show"
                                >{{ `${item[props.label] || ''}` }}</span
                            >
                            <span v-if="selected" class="t-listbox-check">
                                <VueFeather
                                    aria-hidden="true"
                                    class="tw-h-5 tw-w-5"
                                    type="check" />
                            </span>
                        </li>
                    </ListboxOption>
                </ListboxOptions>
            </Transition>
        </div>
    </Listbox>
</template>

<style lang="scss">
    .t-listbox-options {
        @apply tw-absolute tw-mt-2 tw-transform-gpu tw-z-10 tw-backdrop-blur tw-bg-white/30 dark:tw-bg-slate-700/30 tw-w-full tw-overflow-auto tw-rounded-md tw-py-1.5 tw-text-base tw-max-h-60 focus:tw-outline-none sm:tw-text-sm tw-ring-1 tw-ring-black tw-ring-opacity-20 tw-shadow-xl;
    }

    .t-listbox-button {
        @apply tw-relative tw-w-full tw-cursor-default tw-rounded-lg tw-bg-neutral-500/5 dark:tw-bg-slate-900 tw-py-2 tw-pl-3 tw-pr-10 tw-text-left tw-shadow-md focus:tw-outline-none focus-visible:tw-border-indigo-500 focus-visible:tw-ring-2 focus-visible:tw-ring-white focus-visible:tw-ring-opacity-75 focus-visible:tw-ring-offset-2 focus-visible:tw-ring-offset-orange-300 sm:tw-text-md tw-text-md lg:tw-text-base tw-ring-1 tw-ring-zinc-300 dark:tw-ring-neutral-600;
    }

    .t-listbox-item {
        @apply tw-relative tw-cursor-default tw-select-none tw-py-2 tw-pl-10 tw-pr-4 tw-text-gray-900 dark:tw-text-gray-300;
    }

    .t-listbox-item.t-item-active {
        @apply tw-bg-amber-100 tw-text-amber-900 dark:tw-bg-slate-900/40 dark:tw-text-amber-200/70;
    }

    .t-listbox-show {
        @apply tw-block tw-truncate;
    }

    .t-listbox-check {
        @apply tw-absolute tw-inset-y-0 tw-left-0 tw-flex tw-items-center tw-pl-3 tw-text-amber-600;
    }
</style>
