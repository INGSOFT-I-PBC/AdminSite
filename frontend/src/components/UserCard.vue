<script setup lang="ts">
    defineProps({
        username: {
            type: String,
            required: true,
            default: 'Unknown',
        },
        role: {
            type: String,
            required: true,
            default: 'Unknown Role',
        },
        userImage: {
            type: String,
            default: '',
        },
    })
</script>

<template>
    <div
        id="_user-profile-card"
        class="tw-justify-self-start md:tw-grid tw-grid-cols-2 tw-gap-3 tw-bg-primary tw-px-3 tw-text-on-primary dark:tw-bg-slate-600 tw-rounded-md tw-w-1/3 md:tw-w-1/4 lg:tw-w-1/12 tw-py-2 dark:tw-text-on-secondary-hard tw-min-w-fit tw-drop-shadow-lg tw-hidden lg:tw-h-auto">
        <div class="tw-content-center">
            <img v-if="userImage" :src="userImage" alt="User image" />
            <FontAwesomeIcon
                v-else
                class="tw-align-middle tw-h-10 tw-p-1"
                icon="fa-solid fa-circle-user" />
        </div>
        <div class="tw-grid tw-content-center">
            <span class="tw-text-md tw-font-bold">
                {{ username }}
            </span>
            <small class="tw-text-xs tw-italic">
                {{ role }}
            </small>
        </div>
    </div>
</template>
