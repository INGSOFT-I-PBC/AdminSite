<template>
    <div
        class="card hover:tw-scale-105 tw-transition-all tw-duration-150 tw-ease-in-out">
        <div class="card-body" @click="$emit('itemClick', model)">
            <div class="row">
                <div class="col col-auto">
                    <div
                        @click="$emit('iconClick')"
                        class="tw-rounded-full tw-bg-primary/50 tw-p-2 tw-text-primary-light hover:tw-bg-secondary-light tw-transition-colors tw-ease-in-out tw-duration-300">
                        <BIconPerson width="3rem" height="3rem" />
                    </div>
                </div>
                <div class="col">
                    <h5 class="card-title">
                        <span class="tw-text-md tw-text-gray-500 tw-font-bold"
                            >#{{ model.cid }}</span
                        >
                    </h5>
                    <h6>{{ model.name }}&ThinSpace;{{ model.lastname }}</h6>
                </div>
            </div>
        </div>
        <div class="card-footer" v-if="editOptions">
            <div class="btn-group">
                <button
                    class="btn btn-success"
                    @click="$emit('editClick', $data)">
                    <i class="bi bi-pencil-square"></i>
                    &ThinSpace;
                    <span>Editar</span>
                </button>
                <button
                    class="btn btn-danger"
                    @click="$emit('cleanClick', $data)">
                    <i class="bi bi-trash"></i>
                    &ThinSpace;
                    <span>Borrar</span>
                </button>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
    import type { Employee } from '@store-types'
    import { BIconPerson } from 'bootstrap-icons-vue'

    defineEmits(['editClick', 'cleanClick', 'iconClick', 'itemClick'])

    withDefaults(
        defineProps<{
            model: Employee
            editOptions: boolean
        }>(),
        {
            editOptions: false,
        }
    )
</script>
