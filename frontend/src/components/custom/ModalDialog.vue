<script lang="ts" setup>
    import type { ComponentSize } from '@components-types'
    import {
        Dialog,
        DialogPanel,
        DialogTitle,
        TransitionChild,
        TransitionRoot,
    } from '@headlessui/vue'

    import { type PropType, computed } from 'vue'

    import EButton from './EButton.vue'

    const props = defineProps({
        show: {
            type: Boolean,
            default: false,
        },
        title: {
            type: String,
            default: 'Modal Title',
        },
        hideTitle: {
            type: Boolean,
            default: false,
        },
        hideButtons: {
            type: Boolean,
            default: true,
        },
        okText: {
            type: String,
            default: 'Ok',
        },
        cancelText: {
            type: String,
            default: 'Cancel',
        },
        buttonType: {
            type: String as PropType<
                'ok-only' | 'ok-cancel' | 'cancel-only' | 'none'
            >,
            default: 'ok-only',
            validate: (it: string) =>
                ['ok-only', 'ok-cancel', 'cancel-only'].includes(it),
        },
        size: {
            type: String as PropType<ComponentSize>,
            default: () => 'md',
        },
    })
    const emit = defineEmits(['update:show', 'close', 'cancel', 'ok'])

    function onCloseHandler() {
        emit('update:show', false)
        emit('close')
    }

    function okClicked() {
        emit('ok')
        emit('update:show', false)
    }

    function cancelClicked() {
        emit('cancel')
        emit('update:show', false)
    }

    const classes = computed(() => [
        't-dialog',
        'tw-relative',
        'tw-z-50',
        'tw-ease-in-out',
        'tw-transition-opacity',
    ])
    const sizeClasses = computed(() => [
        {
            'tw-max-w-sm': props.size == 'sm',
            'tw-max-w-md': props.size == 'md',
            'tw-max-w-lg': props.size == 'lg',
            'tw-max-w-xl': props.size == 'xl',
            'tw-max-w-2xl': props.size == '2xl',
            'tw-max-w-3xl': props.size == '3xl',
            'tw-max-w-4xl': props.size == '4xl',
            'tw-max-w-[95%]': props.size == 'full',
        },
    ])
</script>

<template>
    <TransitionRoot :show="show" appear as="template">
        <Dialog :class="classes" :open="show" as="div" @close="onCloseHandler">
            <!-- Dialog drop shadow -->
            <TransitionChild
                as="template"
                enter="tw-duration-300 tw-ease-out"
                enter-from="tw-opacity-0"
                enter-to="tw-opacity-100"
                leave="tw-duration-300 tw-ease-in"
                leave-from="tw-opacity-100"
                leave-to="tw-opacity-0">
                <div
                    aria-hidden="true"
                    class="tw-fixed tw-inset-0 tw-bg-black/30 tw-backdrop-blur-sm" />
            </TransitionChild>
            <!-- Dialog Content Below -->
            <TransitionChild
                as="template"
                enter="tw-duration-300 tw-ease-in-out"
                enter-from="tw-opacity-0 tw-scale-0"
                enter-to="tw-opacity-100 tw-scale-100"
                leave="tw-duration-300 tw-ease-in"
                leave-from="tw-opacity-100 tw-scale-100"
                leave-to="tw-opacity-0 tw-scale-50">
                <div
                    class="tw-fixed tw-inset-0 tw-transform-gpu tw-flex tw-items-center tw-justify-center">
                    <DialogPanel
                        :class="sizeClasses"
                        class="tw-w-full tw-flex tw-flex-col tw-max-h-screen md:tw-max-h-[95%] tw-rounded tw-bg-gray-100 dark:tw-bg-slate-700">
                        <DialogTitle v-if="!hideTitle">
                            <div class="tw-px-4 tw-py-4 tw-text-xl">
                                <slot name="dialog-title">
                                    <h1>
                                        {{ title }}
                                    </h1>
                                </slot>
                            </div>
                            <div
                                class="tw-w-full tw-h-0.5 tw-bg-slate-600 dark:tw-bg-slate-400" />
                        </DialogTitle>
                        <div class="e-modal-content">
                            <slot>Hello Modal</slot>
                        </div>
                        <div
                            class="tw-px-2 tw-py-3 tw-flex tw-flex-row-reverse tw-gap-2 tw-z-0">
                            <slot name="dialog-buttons">
                                <EButton
                                    v-if="
                                        ['ok-only', 'ok-cancel'].includes(
                                            buttonType
                                        )
                                    "
                                    @click="okClicked">
                                    {{ okText }}
                                </EButton>
                                <EButton
                                    v-if="
                                        ['cancel-only', 'ok-cancel'].includes(
                                            buttonType
                                        )
                                    "
                                    variant="cancel"
                                    @click="cancelClicked">
                                    {{ cancelText }}
                                </EButton>
                            </slot>
                        </div>
                    </DialogPanel>
                </div>
            </TransitionChild>
        </Dialog>
    </TransitionRoot>
</template>

<style lang="scss">
    .e-modal-content {
        // tw-overflow-y-auto tw-max-h-full
        @apply tw-px-5 tw-py-3 tw-z-50 tw-max-h-full tw-overflow-y-auto;
    }
</style>
