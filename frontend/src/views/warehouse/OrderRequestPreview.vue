<template>
    <ECard>
        <Title size="3xl">Información General</Title>
        <div class="tw-h-0.5 tw-w-full tw-relative -tw-top-3 tw-bg-slate-900" />
        <div class="row">
            <div class="col">
                <InputText
                    :model-value="orderModel?.id.toString()"
                    label="Número de orden"
                    read-only />
            </div>
            <div class="col">
                <InputText
                    :model-value="
                        moment(orderModel?.requested_at).format(
                            'dddd DD/MM/yyyy HH:mm:ss'
                        )
                    "
                    label="Fecha de creación"
                    read-only />
            </div>
            <div class="col">
                <InputText
                    :model-value="`${orderModel?.requested_by.name} ${orderModel?.requested_by.lastname}`"
                    label="Solicitado por"
                    read-only />
            </div>
            <div class="col">
                <label> Estado de la órden</label><br />
                <Title size="2xl">
                    <BBadge :variant="statusColor(orderModel?.status)">
                        {{ parseStatus(orderModel?.status) }}
                    </BBadge>
                </Title>
            </div>
            <div class="col">
                <label class="form-label">Comentarios de la orden</label>
                <TextArea :model-value="orderModel?.comment" readonly />
            </div>
            <div class="col">
                <InputText
                    label="Revisado por"
                    :model-value="
                        orderModel?.revised_at
                            ? `${orderModel?.revised_by?.name} ${orderModel?.revised_by?.lastname}`
                            : '----'
                    "
                    read-only></InputText>
            </div>
        </div>

        <Title size="3xl">Contenido de la orden</Title>
        <div class="tw-h-0.5 tw-w-full tw-relative -tw-top-3 tw-bg-slate-900" />
        <div class="container">
            <div class="row">
                <div class="col">
                    <BTable :fields="tableFields" :items="orderModel?.items">
                        <template #cell(#)="{ index }">
                            {{ index + 1 }}
                        </template>
                    </BTable>
                </div>
            </div>
        </div>
    </ECard>
</template>
<script lang="ts" setup>
    import type {
        OrderRequest,
        OrderRequestStatus,
    } from '@store/types/orders.model'
    import { BBadge, BTable, type ColorVariant } from 'bootstrap-vue-3'
    import moment from 'moment'

    import type { PropType } from 'vue'

    import { ECard, InputText, TextArea, Title } from '@custom-components'

    /**
     * Component props
     */
    defineProps({
        orderModel: {
            type: Object as PropType<OrderRequest>,
            default: undefined,
        },
    })

    /**
     * View related variables
     */
    const tableFields = [
        '#',
        { label: 'Nombre ítem', key: 'item_name' },
        { label: 'Marca ítem', key: 'item_brand' },
        // { label: 'Categoría', key: 'item_category' },
        { label: 'Cantidad', key: 'quantity' },
    ]

    function statusColor(status?: OrderRequestStatus): ColorVariant {
        switch (status) {
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
    function parseStatus(status?: OrderRequestStatus): string {
        switch (status) {
            case 'AP':
                return 'Aprobado'
            case 'PA':
                return 'Pendiente aprobación'
            case 'CR':
                return 'Necesita Corrección'
            case 'NG':
                return 'Desaprobado'
            default:
                return 'Desconocido'
        }
    }
</script>

<!--documentation>
 # OrderRequestPreview

 This view/component is an implementation of a read-only pre visualization
 of the data that an Order Request must have.

 There is 2 parts that involves this component, the first part (at the top of the view)
 is the header information, and data about the employee that requested this.

 The second part is the visualization of the content that includes all the items that this
 order request has and information about the item.
</documentation-->
