<script setup lang="ts">
    import ModalDialog from '@components/custom/ModalDialog.vue'

    import { ref } from 'vue'

    import EButton from '../../components/custom/EButton.vue'
    import ECard from '../../components/custom/ECard.vue'
    import ECol from '../../components/custom/ECol.vue'
    import ERow from '../../components/custom/ERow.vue'
    import InputText from '../../components/custom/InputText.vue'
    import Title from '../../components/custom/Title.vue'

    const normalValue = ref('')
    const toggle = ref(true)
    const showModal = ref(false)

    function iconClick() {
        toggle.value = !toggle.value
    }
    function showModalClick() {
        console.log('Toggling modal')
        showModal.value = !showModal.value
    }
</script>

<template>
    <ERow>
        <ModalDialog v-model:show="showModal" />
        <ECol>
            <ECard>
                <div>
                    <Title>Botones</Title>
                    <ERow>
                        <EButton>Primary</EButton>
                        <EButton variant="secondary">Secondary</EButton>
                        <EButton variant="outline">Outlined</EButton>
                    </ERow>
                    <ERow class="tw-mt-2">
                        <EButton disabled> disabled </EButton>
                        <EButton variant="cancel"> Cancel </EButton>
                        <EButton variant="success"> Success </EButton>
                        <EButton variant="blank"> Blank </EButton>
                    </ERow>
                </div>
            </ECard>
        </ECol>
        <ECol>
            <ECard>
                <Title size="2xl">Input Texts</Title>
                <InputText
                    v-model="normalValue"
                    label="Normal"
                    placeholder="normal"
                    info-label="normal info label" />
                <span>Content normal InputText: {{ normalValue }}</span>
                <InputText
                    label="Danger"
                    info-label="danger info label"
                    placeholder="danger"
                    theme="dark"
                    right-icon="alert-triangle"
                    :status="false"
                    info-status="danger" />
                <InputText
                    label="Warning"
                    :info-label="
                        'warning info label :: ' + (toggle ? 'on' : 'off')
                    "
                    theme="daynight"
                    left-icon="eye"
                    placeholder="warning"
                    @left-icon-click="iconClick"
                    info-status="warning" />
                <InputText
                    label="Success"
                    info-label="Success info label"
                    placeholder="success"
                    :status="true"
                    info-status="success" />
                <InputText
                    v-model="normalValue"
                    label="disabled"
                    placeholder="disabled"
                    right-icon="box"
                    disabled />
            </ECard>
        </ECol>
        <ECol>
            <ECard>
                <Title size="2xl">Modal</Title>
                <EButton @click="showModalClick">Show Modal</EButton>
            </ECard>
        </ECol>
        <ECol>
            <ECard>
                <Title size="2xl">Combo Box & lists</Title>
            </ECard>
        </ECol>
        <ECol cols="4">
            <ECard>
                <Title>Row & Col system</Title>
                <ERow>
                    <template v-for="(_, x) in Array(12)" :key="x">
                        <ECol :cols="x + 1">
                            <span
                                class="tw-ring-emerald-500 tw-ring-1 tw-rounded tw-text-center tw-py-2 tw-px-1">
                                Col-{{ `${x + 1}` }}
                            </span>
                        </ECol>
                    </template>
                </ERow>
            </ECard>
        </ECol>
    </ERow>
    <ECard> adfas </ECard>
</template>
