<script setup>
import {useSessionStore} from '@/stores/session'
import {storeToRefs} from 'pinia';
// Access the Pinia store
const sessionStore = useSessionStore();

// Define the toggle function
const toggleSidebar = () => {
    sessionStore.toggleSideBarState()
};
const {sideBarOpen} = storeToRefs(sessionStore);
</script>

<template>
    <div class="absolute right-0 bottom-0 transform -translate-y-full">
        <button @click="toggleSidebar"
                class="bg-gray-200 hover:bg-main-300 text-gray-500 hover:text-main-500 font-semibold py-5 rounded-l-sm w-3">
            <svg v-if="sideBarOpen" class="h-3 w-3" width="24" height="24" viewBox="0 0 24 24" stroke-width="2"
                 stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <path stroke="none" d="M0 0h24v24H0z"/>
                <polyline points="15 6 9 12 15 18"/>
            </svg>
            <svg v-else class="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round">
                <polyline points="9 18 15 12 9 6"/>
            </svg>
        </button>
    </div>
</template>

<style scoped>

</style>
