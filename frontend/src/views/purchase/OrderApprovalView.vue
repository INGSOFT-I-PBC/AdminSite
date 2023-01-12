<template>
    <ECard>
        <ModalDialog
            v-model:show="modalState.showConfirmDelete"
            title="¿Desea desaprobar el pedido?">
            El pedido #{{ targetOrder?.id }} se va a desaprobar y no se podrá
            revertir este cambio, ¿desea continuar?
            <template #dialog-buttons>
                <EButton
                    variant="cancel"
                    @click="
                        () => {
                            if (targetOrder) {
                                orderRepository
                                    .denyOrderRequest(targetOrder.id)
                                    .then(() => {
                                        searchOptions.page = 1
                                        makeSearch()
                                        modalState.showConfirmDelete = false
                                    })
                                    .catch(checkRespose)
                            }
                        }
                    ">
                    Desaprobar
                </EButton>
                <EButton @click="modalState.showConfirmDelete = false">
                    Cancelar
                </EButton>
            </template>
        </ModalDialog>
        <ModalDialog
            v-model:show="modalState.showConfirmApprove"
            title="¿Desea aprobar el pedido?"
            button-type="ok-cancel"
            ok-text="Aprobar"
            @ok="
                () => {
                    if (targetOrder) {
                        orderRepository
                            .approveOrderRequest(targetOrder.id)
                            .then(() => {
                                toast.success('Orden aprobada exitosamente')
                                searchOptions.page = 1
                                makeSearch()
                            })
                            .catch(checkRespose)
                    }
                }
            ">
            El pedido #{{ targetOrder?.id }} se va a aprobar y no se podrá
            revertir este cambio, ¿desea continuar?
        </ModalDialog>

        <ModalDialog
            v-model:show="modalState.showPreview"
            :title="`Vista previa de orden ${targetOrder?.id}`"
            size="3xl"
            ok-text="Cerrar">
            <OrderRequestPreview :order-model="targetOrder" />
        </ModalDialog>
        <Title size="3xl">Aprobación de Órdenes de compra</Title>
        <div class="tw-my-3">
            <Title
                class="tw-absolute tw-left-3 -tw-top-3 tw-z-[5] tw-bg-slate-50 dark:tw-bg-slate-800"
                size="lg">
                Cuadro de búsqueda
            </Title>
            <div
                class="tw-border-solid tw-border-gray-800 tw-py-5 tw-px-3 tw-rounded-md tw-border-2">
                <VeeForm @submit="makeSearch">
                    <div
                        class="row justify-items-center align-content-center align-items-center">
                        <div class="col">
                            <InputText
                                label="Motivo o Descripción"
                                v-model="searchOptions.comment" />
                        </div>
                        <div class="col col-auto">
                            <EButton class="tw-w-full">Buscar</EButton>
                        </div>
                        <div class="col col-auto">
                            <EButton
                                class="tw-w-full"
                                @click="
                                    () => {
                                        searchOptions.comment = undefined
                                    }
                                ">
                                Limpiar
                            </EButton>
                        </div>
                    </div>
                    <div></div>
                </VeeForm>
            </div>
        </div>
        <BTable
            :fields="fields"
            :busy="isLoading"
            :items="orderRepository.orderRequests?.data">
            <template #cell(#)="{ index }">
                {{
                    index +
                    1 +
                    (searchOptions.page - 1) * (searchOptions.per_page ?? 1)
                }}
            </template>
            <template #cell(requested_at)="{ value }">
                {{ moment(value).fromNow() }}
            </template>
            <template #cell(requested_by)="{ value }">
                {{ `${value.name} ${value.lastname}` }}
            </template>
            <template #cell(status)="{ value }">
                <BBadge
                    :variant="determinePillVariant(value as OrderRequestStatus)">
                    {{ evalStatus(value) }}
                </BBadge>
            </template>
            <template #cell(items)="{ value }">
                {{ value.length }}
            </template>
            <template #cell(Acciones)="{ item }">
                <EButtonGroup>
                    <EButton
                        :disabled="item.status == 'AP' || item.status == 'NG'"
                        variant="success"
                        left-icon="check"
                        @click="
                            () => {
                                targetOrder = item
                                modalState.showConfirmApprove = true
                            }
                        ">
                        Aprobar</EButton
                    >
                    <EButton
                        :disabled="item.status == 'AP' || item.status == 'NG'"
                        variant="cancel"
                        left-icon="trash"
                        @click="
                            () => {
                                targetOrder = item
                                modalState.showConfirmDelete = true
                            }
                        "
                        >Desaprobar</EButton
                    >
                    <EButton
                        variant="secondary"
                        left-icon="eye"
                        @click="
                            () => {
                                targetOrder = item
                                modalState.showPreview = true
                            }
                        "
                        >Ver</EButton
                    >
                </EButtonGroup>
            </template>
        </BTable>
        <BPagination
            align="center"
            :total-rows="orderRepository.orderRequests?.total ?? 1"
            :per-page="searchOptions.per_page ?? 10"
            next-text="Siguiente"
            prev-text="Anterior"
            @page-click="onPaginationClick" />
    </ECard>
</template>

<script lang="ts" setup>
    import type { ColorVariant } from '@components/types/bootstrap'
    import { useOrderStore } from '@store'
    import type {
        OrderRequest,
        OrderRequestStatus,
        RawOrderRequest,
    } from '@store/types/orders.model'
    import type {
        BadValidationResponse,
        ErrorResponse,
    } from '@store/types/requests'
    import { isErrorResponse } from '@store/types/typesafe'
    import OrderRequestPreview from '@views/warehouse/OrderRequestPreview.vue'
    import axios from 'axios'
    import { BPagination, BTable, BvEvent } from 'bootstrap-vue-3'
    import moment from 'moment'

    import { useToast } from 'vue-toastification'

    import {
        EButton,
        EButtonGroup,
        ECard,
        InputText,
        ModalDialog,
        Title,
    } from '@custom-components'

    /*
     * Store definition
     */
    const orderRepository = useOrderStore()

    /**
     * View related variables
     */
    const toast = useToast()
    const modalState = ref({
        showConfirmDelete: false,
        showConfirmApprove: false,
        showPreview: false,
    })
    const isLoading = ref(false)
    const searchOptions = ref<PaginationOptions & Partial<RawOrderRequest>>({
        comment: undefined,
        page: 1,
        per_page: 10,
    })
    const targetOrder = ref<OrderRequest>()

    /*
     * Table related variables
     */
    const fields = [
        '#',
        { label: 'No. orden', key: 'id' },
        { label: 'Estado', key: 'status' },
        { label: 'Solicitado por', key: 'requested_by' },
        { label: 'Solicitado en', key: 'requested_at' },
        { label: 'Cantidad Items', key: 'items' },
        'Acciones',
    ]

    function makeSearch() {
        isLoading.value = true
        orderRepository
            .fetchOrderRequests(searchOptions.value)
            .catch(err => {
                if (
                    axios.isAxiosError(err) &&
                    defined(err.response) &&
                    err.response.status < 500
                ) {
                    const queryError = err.response
                        .data as BadValidationResponse
                    toast.error('No se pudo realizar la busqueda')
                } else {
                    toast.error('Error desconocido')
                }
                //               console.log('Error while searching: ', err)
                //                toast.error('No se pudo realizar a búsqueda')
            })
            .finally(() => {
                isLoading.value = false
            })
    }
    function determinePillVariant(value: OrderRequestStatus): ColorVariant {
        switch (value) {
            case 'AP':
                return 'success'
            case 'PA':
                return 'warning'
            case 'NG':
                return 'danger'
            default:
                return 'dark'
        }
    }
    function evalStatus(value: OrderRequestStatus) {
        switch (value) {
            case 'PA':
                return 'Pendiente Aprobacion'
            case 'AP':
                return 'Aprobada'
            case 'NG':
                return 'Denegada'
            default:
                return 'Desconocido'
        }
    }

    function checkRespose(err: Error | ErrorResponse) {
        if (isErrorResponse(err)) {
            switch (err.response?.data.code) {
                case 'ERR_REVISED':
                    toast.error('La orden ya ha sido revisada')
                    break
                default:
                    toast.error('Error desconocido')
            }
        } else {
            toast.error('Error desconocido, por favor intente más tarde')
        }
    }
    function onPaginationClick(event: BvEvent, page: number) {
        searchOptions.value.page = page
        makeSearch()
    }
    makeSearch()
</script>
