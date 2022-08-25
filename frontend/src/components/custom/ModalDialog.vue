<script setup lang="ts">
    import {
        Dialog,
        DialogPanel,
        DialogTitle,
        TransitionRoot,
        TransitionChild,
    } from '@headlessui/vue'
    import EButton from './EButton.vue'

    defineProps({
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
            default: false,
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
            type: String,
            default: 'ok-only',
            validate: (it: string) =>
                ['ok-only', 'ok-cancel', 'cancel-only'].includes(it),
        },
    })
    const emit = defineEmits(['update:show', 'close', 'cancel', 'ok'])
    function onCloseHandler() {
        emit('update:show', false)
        emit('close')
    }
    function okClicked(_e: Event) {
        emit('ok')
        emit('update:show', false)
    }
    function cancelClicked(_e: Event) {
        emit('cancel')
        emit('update:show', false)
    }
</script>

<template>
    <TransitionRoot appear :show="show" as="template">
        <Dialog
            as="div"
            :open="show"
            @close="onCloseHandler"
            class="tw-relative tw-z-50 tw-ease-in-out tw-transition-opacity">
            <!-- Dialog drop shadow -->
            <TransitionChild
                as="template"
                enter="tw-duration-300 tw-ease-out"
                enter-from="tw-opacity-0"
                enter-to="tw-opacity-100"
                leave="tw-duration-200 tw-ease-in"
                leave-from="tw-opacity-100"
                leave-to="tw-opacity-0">
                <div
                    class="tw-fixed tw-inset-0 tw-bg-black/30 tw-backdrop-blur-sm"
                    aria-hidden="true" />
            </TransitionChild>
            <!-- Dialog Content Below -->
            <TransitionChild
                as="template"
                enter="tw-duration-300 tw-ease-in-out"
                enter-from="tw-opacity-0 tw-scale-0"
                enter-to="tw-opacity-100 tw-scale-100"
                leave="tw-duration-300 tw-ease-in"
                leave-from="tw-opacity-100 tw-scale-100"
                leave-to="tw-opacity-0 tw-scale-0">
                <div
                    class="tw-fixed tw-inset-0 tw-transform-gpu tw-flex tw-items-center tw-justify-center">
                    <DialogPanel
                        class="tw-w-full tw-max-w-sm tw-rounded tw-bg-gray-100 dark:tw-bg-slate-700">
                        <DialogTitle v-if="!hideTitle">
                            <div class="tw-px-3 tw-py-2">
                                <slot name="dialog-title">
                                    <h1>
                                        {{ title }}
                                    </h1>
                                </slot>
                            </div>
                            <div
                                class="tw-w-full tw-h-0.5 tw-bg-slate-600 dark:tw-bg-slate-400" />
                        </DialogTitle>
                        <div class="e-modal-content tw-px-5 tw-py-3">
                            <slot>Hello Modal</slot>
                        </div>
                        <div
                            class="tw-px-2 tw-py-3 tw-flex tw-flex-row-reverse tw-gap-2">
                            <slot name="dialog-buttons">
                                <EButton
                                    v-if="
                                        ['ok-only', 'ok-cancel'].includes(buttonType)
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
                                    @click="cancelClicked"
                                    type="cancel">
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
