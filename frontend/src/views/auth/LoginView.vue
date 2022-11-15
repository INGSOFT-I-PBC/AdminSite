<script setup lang="ts">
    import EButton from '@components/custom/EButton.vue'
    import ECard from '@components/custom/ECard.vue'
    import { useAuthStore } from '@store'

    import { ref } from 'vue'
    import { useRouter } from 'vue-router'

    import InputText from '../../components/custom/InputText.vue'
    import LoadingBar from '../../components/custom/LoadingBar.vue'

    const router = useRouter()
    const toggle = ref(false)
    const username = ref('')
    const isLoading = ref(false)
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
        toggleUsername.value = (username.value ?? '') === ''
        togglePassword.value = (password.value ?? '') === ''
        if (toggleUsername.value === false && togglePassword.value === false) {
            isLoading.value = true
            authStore
                .login({
                    username: username.value,
                    password: password.value,
                })
                .then(() => authStore.fetchUserData())
                .then(() => {
                    router.push({ path: '/' })
                })
                .catch(() => {
                    error.value = true
                })
                .finally(() => {
                    isLoading.value = false
                })
        }
    }
</script>

<template>
    <div class="login-view">
        <ECard id="login-card">
            <img
                src="../../assets/img/nova.png"
                class="tw-max-w-full tw-h-auto tw-rounded-lg"
                alt="NovaGym" />
            <form @submit.prevent="inactive">
                <InputText
                    label="Usuario"
                    :disabled="isLoading"
                    :info-label="toggleUsername ? 'campo requerido' : ''"
                    placeholder="usuario"
                    v-model="username"
                    info-status="danger"></InputText>
                <!--<span class="text-xs tracking-wide text-red-600">Email field is required </span>-->
                <div class="mt-4">
                    <InputText
                        :disabled="isLoading"
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

                <LoadingBar v-show="isLoading" class="tw-mt-5" />

                <div class="tw-text-center">
                    <div class="mt-4" v-if="error">
                        <p class="tw-text-red-700">{{ errorMessage }}</p>
                    </div>
                    <div class="mt-4">
                        <EButton @click="access">Acceder </EButton>
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

<style lang="scss">
    .login-view {
        @apply tw-min-h-full tw-py-0 md:tw-py-5 tw-w-screen tw-flex tw-flex-col tw-justify-center tw-justify-items-center tw-items-center tw-bg-gray-200 dark:tw-bg-gray-900;
    }
    .login-view > #login-card {
        @apply tw-h-full tw-min-h-full;
    }
</style>
