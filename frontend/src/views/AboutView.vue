<script setup lang="ts">
    import { ref } from 'vue'

    const counter = ref(0)

    function clickButton() {
        counter.value += 1
    }
</script>
<template>
    <div class="about">
        <h1>This is an about page</h1>
        <span>Counter: {{ counter }}</span>
        <button @click="clickButton">Button</button>
    </div>
</template>

<style>
    @media (min-width: 1024px) {
        .about {
            min-height: 100vh;
            display: flex;
            align-items: center;
        }
    }
</style>
