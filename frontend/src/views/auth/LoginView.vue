<script setup lang="ts">
    import ECard from '@components/custom/ECard.vue'
    import EButton from '@components/custom/EButton.vue'
    import { useAuthStore } from '@store'
    import { useRouter } from 'vue-router'
    import InputText from '../../components/custom/InputText.vue'
    import { ref } from 'vue'

    useAuthStore().refreshToken()
    const router = useRouter()
    const toggle = ref(false)
    const password = ref('')

    function switchVisibility() {
        toggle.value = !toggle.value
    }

    function inactive(e: Event) {
        e.preventDefault()
    }

    function access() {
        router.push({ path: '/' })
    }
</script>

<template>
    <div
        class="tw-h-screen tw-w-screen tw-flex tw-flex-col tw-justify-center tw-justify-items-center tw-text-center tw-items-center tw-bg-gray-200 dark:tw-bg-gray-900">
        <ECard class="tw-bg-gray-900">
            <img
                src="../../assets/img/nova.png"
                class="tw-max-w-full tw-h-auto tw-rounded-lg"
                alt="NovaGym" />
            <form @onsubmit="inactive">
                <div class="mt-4">
                    <div>
                        <InputText placeholder="Usuario"></InputText>
                        <!--<span class="text-xs tracking-wide text-red-600">Email field is required </span>-->
                    </div>
                    <div class="mt-4">
                        <InputText
                            placeholder="Contraseña"
                            v-model="password"
                            :type="toggle ? 'text' : 'password'"
                            id="password"
                            :right-icon="toggle ? 'eye-off' : 'eye'"
                            @right-icon-click="switchVisibility">
                        </InputText>
                        <!--rightIcon="eye"-->
                    </div>
                    <div class="mt-4">
                        <EButton type="primary" @click="access">Acceder </EButton>
                    </div>
                    <div class="flex items-baseline justify-between mt-4">
                        <a href="#" class="text-sm text-blue-600 hover:underline"
                            >¿Olvidó su contraseña?</a
                        >
                    </div>
                </div>
            </form>
        </ECard>
    </div>
</template>
