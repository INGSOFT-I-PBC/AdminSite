<script setup lang="ts">
    import { ref } from 'vue'
    const message = ref('TODO: Make this view')
</script>

<template>
    <div>
        <div
            class="rounded border ring-1 ring py-5 px-3 ring-offset-3 ring-gray-300 flex flex-col">
            <label for="email-input">Email:</label>
            <input type="text" id="email-input" />
            <label for="password-input">Password:</label>
            <EInput></EInput>
            <input type="password" name="password" id="password-input" />
            <div class="flex flex-row justify-center">
                <button class="px-2 py-1 ring ring-1 ring-gray-200">
                    Iniciar Sesión
                </button>
                <button class="px-2 py-1 ring ring-1 ring-gray-100">Cancelar</button>
            </div>
        </div>
        <h1>{{ message }}</h1>
    </div>
</template>
