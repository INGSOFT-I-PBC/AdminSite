import axios from 'axios'
import { defineStore} from 'pinia'
import type { Group, Groups, PaginatedGroups } from './types/common.model'

export const useCommonStore = defineStore('common-store', () => {
    const groups = ref<Groups>([])
    const paginatedGroups = ref<PaginatedGroups | null>(null)
    const group = ref<Group | null>(null)

    async function fetchAllGroups() {
        const response = (
            await axios.get<Groups>('/api/v1/list/groups/all')
            ).data
        groups.value = response
        return response
    }

    async function fetchGroups(params?: PaginationOptions) {
        const response = (await axios.get<PaginatedGroups>('/api/v1/list/groups', {params})).data
        paginatedGroups.value = response
        return response
    }


    return {
        groups, paginatedGroups, group,
        fetchAllGroups, fetchGroups
    }
})
