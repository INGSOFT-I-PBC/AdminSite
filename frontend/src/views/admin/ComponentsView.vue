<script setup lang="ts">
    import ECard from '../../components/custom/ECard.vue'
    import EButton from '../../components/custom/EButton.vue'
    import ERow from '../../components/custom/ERow.vue'
    import Title from '../../components/custom/Title.vue'
    import InputText from '../../components/custom/InputText.vue'
    import { ref } from 'vue'

    const normalValue = ref('')
    const toggle = ref(true)

    function iconClick() {
        toggle.value = !toggle.value
    }
</script>

<template>
    <div class="tw-flex tw-gap-3">
        <ECard>
            <div>
                <Title>Botones</Title>
                <ERow>
                    <EButton>Primary</EButton>
                    <EButton type="secondary"
                        >Secondary</EButton
                    >
                    <EButton type="outline"
                        >Outlined</EButton
                    >
                    <EButton disabled>
                        disabled
                    </EButton>
                </ERow>
            </div>
        </ECard>
        <ECard>
            <Title size="2xl">Input Texts</Title>
            <InputText
                v-model="normalValue"
                label="Normal"
                placeholder="normal"
                info-label="normal info label" />
            <span
                >Content normal InputText:
                {{ normalValue }}</span
            >
            <InputText
                label="Danger"
                info-label="danger info label"
                placeholder="danger"
                right-icon="alert-triangle"
                :status="false"
                info-status="danger" />
            <InputText
                label="Warning"
                :info-label="
                    'warning info label :: ' +
                    (toggle ? 'on' : 'off')
                "
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
        <ECard>
            <Title size="2xl">Modal</Title>
        </ECard>
        <ECard>
            <Title size="2xl"
                >Combo Box & lists</Title
            >
        </ECard>
        <ECard>
            <h3></h3>
        </ECard>
    </div>
</template>
