<template>
    <div class="container gy-3">
        <div class="row align-items-end gx-2 gy-3 mb-3">
            <div class="col col-9">
                <InputText label="Búsqueda de empleado" />
            </div>
            <div class="col col-3">
                <EButton>Buscar</EButton>
            </div>
        </div>
        <WaitOverlay :show="isLoading">
            <div class="row gy-3 align-items-stretch">
                <div
                    class="col-12 col-md-6 col-lg-4 col-xxl-2"
                    v-for="employee in employeeRepository.paginatedEmployees
                        ?.data"
                    :key="employee.cid">
                    <EmployeeCardItem
                        :model="employee"
                        @item-click="
                            employee => $emit('itemSelect', employee)
                        " />
                </div>
                <div class="col col-12">
                    <BPagination align="center" />
                </div>
            </div>
        </WaitOverlay>
    </div>
</template>

<script setup lang="ts">
    import InputText from '../../../components/custom/InputText.vue'
    import EButton from '../../../components/custom/EButton.vue'
    import { BPagination } from 'bootstrap-vue-3'
    import { useEmployeeStore, type EmployeeSearchParams } from '@store'
    import WaitOverlay from '@components/custom/WaitOverlay.vue'
    import EmployeeCardItem from '@components/models/EmployeeCardItem.vue'
    const employeeRepository = useEmployeeStore()
    const searchOptions = ref<EmployeeSearchParams & PaginationOptions>({
        page: 1,
        per_page: 15,
    })
    const isLoading = ref(false)

    function makeSearch() {
        isLoading.value = true
        employeeRepository.fetchEmployees(searchOptions.value).finally(() => {
            isLoading.value = false
        })
    }
    makeSearch()
    defineEmits(['itemSelect', 'pageChanged'])
</script>
