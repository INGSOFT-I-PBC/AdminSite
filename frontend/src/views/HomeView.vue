<script setup lang="ts">
    import TheWelcome from '@/components/TheWelcome.vue'
    import ECard from '../components/custom/ECard.vue'
    import EButton from '../components/custom/EButton.vue'
</script>

<template>
    <main>
        <ECard>
            <h1
                class="align-center text-center text-3xl font-bold">
                Bienvenido
            </h1>
            <div class="flex gap-3">
                <EButton
                    >Test primary Button</EButton
                >
                <EButton type="secondary"
                    >Test secondary
                    Button</EButton
                >
            </div>
        </ECard>
    </main>
</template>
