<script setup lang="ts">
    import ECard from '@components/custom/ECard.vue'
    import EButton from '@components/custom/EButton.vue'
    import { useAuthStore } from '@store'
    import { useRouter } from 'vue-router'
    import InputText from '../../components/custom/InputText.vue'
    import { ref } from 'vue'
    const router = useRouter()
    const toggle = ref(false)
    const username = ref('')
    const toggleUsername = ref(false)
    const password = ref('')
    const togglePassword = ref(false)
    const error = ref(false)
    const errorMessage = 'El usuario y/o contraseña no coinciden'
    function switchVisibility() {
        toggle.value = !toggle.value
    }
    function inactive(e: Event) {
        e.preventDefault()
    }
    const authStore = useAuthStore()
    function access() {
        error.value = false
        toggleUsername.value = username.value === '' ? true : false
        togglePassword.value = password.value === '' ? true : false
        if (toggleUsername.value === false && togglePassword.value === false) {
            console.log(import.meta.env.VITE_BACKEND_URL)
            authStore
                .login({
                    username: username.value,
                    password: password.value,
                })
                .then(it => authStore.fetchUserData())
                .then(it => {
                    router.push({ path: '/' })
                })
                .catch(it => {
                    error.value = true
                })
        }
    }
</script>

<template>
    <div
        class="tw-h-screen tw-w-screen tw-flex tw-flex-col tw-justify-center tw-justify-items-center tw-items-center tw-bg-gray-200 dark:tw-bg-gray-900">
        <ECard class="tw-bg-gray-900">
            <img
                src="../../assets/img/nova.png"
                class="tw-max-w-full tw-h-auto tw-rounded-lg"
                alt="NovaGym" />
            <form @onsubmit="inactive">
                <InputText
                    label="Usuario"
                    :info-label="toggleUsername ? 'campo requerido' : ''"
                    placeholder="usuario"
                    v-model="username"
                    info-status="danger"></InputText>
                <!--<span class="text-xs tracking-wide text-red-600">Email field is required </span>-->
                <div class="mt-4">
                    <InputText
                        label="Contraseña"
                        :info-label="togglePassword ? 'campo requerido' : ''"
                        placeholder="contraseña"
                        v-model="password"
                        :type="toggle ? 'text' : 'password'"
                        id="password"
                        :right-icon="toggle ? 'eye-off' : 'eye'"
                        @right-icon-click="switchVisibility"
                        info-status="danger">
                    </InputText>
                    <!--rightIcon="eye"-->
                </div>
                <div class="tw-text-center">
                    <div class="mt-4" v-if="error">
                        <p class="tw-text-red-700">{{ errorMessage }}</p>
                    </div>
                    <div class="mt-4">
                        <EButton type="primary" @click="access">Acceder </EButton>
                    </div>
                    <div class="flex items-baseline justify-between mt-4">
                        <a class="text-sm text-blue-600 hover:underline"
                            >¿Olvidó su contraseña?</a
                        >
                    </div>
                </div>
            </form>
        </ECard>
    </div>
</template>
