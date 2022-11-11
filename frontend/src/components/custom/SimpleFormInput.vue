<template>
    <VeeField :name="name" v-slot="{ field, errorMessage, handleChange }">
        <InputText
            :label="label"
            :model-value="field.value as string"
            :info-label="errorMessage"
            info-status="danger"
            @update:model-value="handleChange" />
    </VeeField>
</template>

<script lang="ts" setup>
    import InputText from './InputText.vue'

    defineProps({
        name: {
            type: String,
            required: true,
        },
        label: {
            type: String,
            required: true,
        },
    })
</script>
