<script lang="ts" setup>
    import ECard from '../../../components/custom/ECard.vue'
    import InputText from '../../../components/custom/InputText.vue'
    import ERow from '../../../components/custom/ERow.vue'
    import ECol from '../../../components/custom/ECol.vue'
    import ETab from '../../../components/holders/ETab.vue'
    import EButton from '@components/custom/EButton.vue'

    const user = ref({
        username: '',
        name: '',
        lastname: '',
        email: '',
        password: '',
        confirmPassword: '',
        role: null,
    })
    const vertical = ref(false)
</script>

<template>
    <ECard>
        <ETab
            :vertical-tabs="vertical"
            :tabs="['Mantenimiento usuarios', 'Crear usuario']">
        </ETab>
        <EButton @click="vertical = !vertical">ClickMe</EButton>
        <ERow>
            <ECol>
                <InputText label="Nombre de usuario" />
            </ECol>
        </ERow>
    </ECard>
</template>
