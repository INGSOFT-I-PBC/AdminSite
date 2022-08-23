<script setup lang="ts">
    import { ref } from 'vue'
    import EButton from '@components/custom/EButton.vue'
    import ERow from '@components/custom/ERow.vue'

    const message = ref('TODO: Make this view')
</script>

<template>
    <div>
        <h1>{{ message }}</h1>
        <h2>Esto jjes un ejemplo de empleado</h2>
        <ERow
            ><EButton type="secondary"
                >+ Add Employee
            </EButton>
            <EButton>Roles</EButton></ERow
        >
    </div>
</template>
