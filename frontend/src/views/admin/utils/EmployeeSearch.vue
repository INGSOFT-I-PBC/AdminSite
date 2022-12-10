<template>
    <div class="container gy-3">
        <div class="row align-items-end gx-2 gy-3 mb-3">
            <div class="col col-8">
                <InputText
                    label="Búsqueda de empleado"
                    v-model="employeeName" />
            </div>
            <div class="col col-2 gy-3 mb-3 text-center">
                <EButton class="py-2" @click.left="makeOneSearch"
                    >Buscar</EButton
                >
            </div>
            <div class="col col-2 gy-3 mb-3">
                <EButton class="py-2" @click.left="reSearch">Limpiar</EButton>
            </div>
        </div>
        <WaitOverlay :show="isLoading">
            <div class="row gy-3 align-items-stretch">
                <div v-if="!isEmployeeSearch">
                    <div
                        class="col-12 col-md-6 col-lg-4 col-xxl-2"
                        v-for="employee in employees"
                        :key="employee.cid">
                        <EmployeeCardItem
                            :model="employee"
                            @item-click="
                                employee => $emit('itemSelect', employee)
                            " />
                    </div>
                </div>
                <div v-if="isEmployeeSearch">
                    <div
                        class="col-12 col-md-6 col-lg-4 col-xxl-2"
                        v-for="employee in employeesSearch"
                        :key="employee.cid">
                        <EmployeeCardItem
                            :model="employee"
                            @item-click="
                                employee => $emit('itemSelect', employee)
                            " />
                    </div>
                </div>
                <div class="col col-12">
                    <BPagination align="center" />
                </div>
            </div>
        </WaitOverlay>
    </div>
</template>

<script setup lang="ts">
    import WaitOverlay from '@components/custom/WaitOverlay.vue'
    import EmployeeCardItem from '@components/models/EmployeeCardItem.vue'
    import { type EmployeeSearchParams, useEmployeeStore } from '@store'
    import type { Employee } from '@store/types'
    import { BPagination } from 'bootstrap-vue-3'

    import { onMounted } from 'vue'

    import EButton from '../../../components/custom/EButton.vue'
    import InputText from '../../../components/custom/InputText.vue'

    const isEmployeeSearch = ref(false)
    const employeeRepository = useEmployeeStore()
    const employeeName = ref('')
    const searchOptions = ref<EmployeeSearchParams & PaginationOptions>({
        page: 1,
        per_page: 15,
    })
    const isLoading = ref(false)

    function onSubmit() {
        makeSearch()
    }

    onMounted(() => {
        return makeSearch()
    })

    const employees = ref<Employee[]>([])
    function makeSearch() {
        isLoading.value = true
        employeeRepository
            .fetchEmployees(searchOptions.value)
            .then(response => {
                employees.value = response.data
            })
            .finally(() => {
                isLoading.value = false
            })
    }

    const employeesSearch = ref<Employee[]>([])

    function makeOneSearch() {
        isLoading.value = true
        employeeRepository
            .fetchEmployees({ name: employeeName.value, page: 1, per_page: 10 })
            .then(response => {
                employeesSearch.value = response.data
            })
            .finally(() => {
                isLoading.value = false
                isEmployeeSearch.value = true
            })
    }

    function reSearch() {
        isEmployeeSearch.value = false
        console.log(isEmployeeSearch.value)
        employeeName.value = ''
    }

    makeSearch()
    defineEmits(['itemSelect', 'pageChanged'])
</script>
