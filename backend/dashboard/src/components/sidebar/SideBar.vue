<template>
    <section class="w-full">
        <nav class="lg:hidden py-6 px-6 border-b">
            <div class="flex items-center justify-between">
                <a class="text-2xl font-semibold" href="#">
                    <img class="h-10 w-auto" src="../../assets/artemis-assets/logos/artemis-logo-light.svg" alt="">
                </a>
                <button class="navbar-burger flex items-center rounded focus:outline-none">
                    <svg class="text-white bg-indigo-500 hover:bg-indigo-600 block h-8 w-8 p-2 rounded"
                         viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" fill="currentColor">
                        <title>Mobile menu</title>
                        <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"></path>
                    </svg>
                </button>
            </div>
        </nav>
        <div class="hidden lg:block navbar-menu relative z-50">
            <div class="navbar-backdrop fixed lg:hidden inset-0 bg-gray-800 opacity-10">
            </div>
            <nav v-if="!sideBarOpen"
                 class="fixed top-0 left-0 bottom-0 flex flex-col w-1/4 lg:w-14 sm:max-w-xs bg-white border-r overflow-y-auto scrollbar-hide">
                <div
                    class="sticky top-0 z-40 flex w-full items-center justify-center px-2 py-3 lg:border-b border-blue-50 bg-white">
                    <router-link
                        :to="{ name: 'home' }" class="text-xl font-semibold w-full flex items-center justify-center">
                        <img class="h-8 w-auto" src="../../assets/artemis-assets/logos/artemis-sign.svg" alt="">
                    </router-link>
                </div>
                <div :class="sideBarOpen ? 'px-4 pb-6' : 'px-0 pb-6'">
                    <side-bar-tree/>
                </div>
                <toggle-button/>
            </nav>
            <nav v-else
                 class="fixed top-0 left-0 bottom-0 flex flex-col w-3/4 lg:w-80 sm:max-w-xs pt-6 pb-8 bg-white border-r overflow-y-auto">
                <div class="flex w-full items-center px-6 pb-6 mb-6 lg:border-b border-blue-50">
                    <a class="text-xl font-semibold" href="#">
                        <img class="h-8 w-auto" src="../../assets/artemis-assets/logos/artemis-logo-light.svg" alt="">
                    </a>
                </div>
                <div class="px-4 pb-6">
                    <side-bar-tree/>
                </div>
                <toggle-button/>
            </nav>

        </div>
    </section>
</template>

<script setup>
import ToggleButton from '@/components/sidebar/toggleButton.vue';
import SideBarTree from "@/components/sidebar/sideBarTree.vue";
import {storeToRefs} from 'pinia';
import {useSessionStore} from '@/stores/session'
// Access the Pinia store
const sessionStore = useSessionStore();
const {sideBarOpen} = storeToRefs(sessionStore);
</script>
<style>
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.scrollbar-hide {
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
}
</style>