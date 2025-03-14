<template>
    <section class="sticky top-0 flex items-center z-40 bg-white shadow h-12">
        <nav class="flex items-center justify-between w-full relative px-4">
            <div class="flex items-center">
                <router-link
                    :to="{ name: 'home' }"
                    class="flex items-center text-sm hover:text-gray-800 cursor-pointer"
                >
                  <span class="inline-block mr-2">
                    <svg fill="none" height="18" viewBox="0 0 16 18" width="16" xmlns="http://www.w3.org/2000/svg">
                      <path
                          d="M14.6667 5.66667L9.66668 1.28333C9.20833 0.87337 8.61496 0.646723 8.00002 0.646723C7.38507 0.646723 6.7917 0.87337 6.33335 1.28333L1.33335 5.66667C1.06866 5.90339 0.857435 6.1938 0.713745 6.51854C0.570054 6.84328 0.497195 7.1949 0.500018 7.55V14.8333C0.500018 15.4964 0.76341 16.1323 1.23225 16.6011C1.70109 17.0699 2.33698 17.3333 3.00002 17.3333H13C13.6631 17.3333 14.2989 17.0699 14.7678 16.6011C15.2366 16.1323 15.5 15.4964 15.5 14.8333V7.54167C15.5017 7.18797 15.4282 6.83795 15.2846 6.51473C15.1409 6.19152 14.9303 5.90246 14.6667 5.66667ZM9.66668 15.6667H6.33335V11.5C6.33335 11.279 6.42115 11.067 6.57743 10.9107C6.73371 10.7545 6.94567 10.6667 7.16668 10.6667H8.83335C9.05436 10.6667 9.26633 10.7545 9.42261 10.9107C9.57889 11.067 9.66668 11.279 9.66668 11.5V15.6667ZM13.8334 14.8333C13.8334 15.0543 13.7456 15.2663 13.5893 15.4226C13.433 15.5789 13.221 15.6667 13 15.6667H11.3334V11.5C11.3334 10.837 11.07 10.2011 10.6011 9.73223C10.1323 9.26339 9.49639 9 8.83335 9H7.16668C6.50364 9 5.86776 9.26339 5.39892 9.73223C4.93008 10.2011 4.66668 10.837 4.66668 11.5V15.6667H3.00002C2.779 15.6667 2.56704 15.5789 2.41076 15.4226C2.25448 15.2663 2.16668 15.0543 2.16668 14.8333V7.54167C2.16683 7.42334 2.19218 7.30641 2.24103 7.19865C2.28989 7.09088 2.36113 6.99476 2.45002 6.91667L7.45002 2.54167C7.60209 2.40807 7.79759 2.33439 8.00002 2.33439C8.20244 2.33439 8.39794 2.40807 8.55002 2.54167L13.55 6.91667C13.6389 6.99476 13.7101 7.09088 13.759 7.19865C13.8079 7.30641 13.8332 7.42334 13.8334 7.54167V14.8333Z"
                          fill="#382CDD"
                      ></path>
                    </svg>
                  </span>
                    <span>Inicio</span>
                </router-link>
                <span id="root-directory" class="flex items-center"></span>
            </div>
            <div class="flex items-center relative">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    height="24"
                    viewBox="0 0 24 24"
                    width="24"
                    class="fill-current mr-3 hover:text-blue-500"
                >
                    <path d="M0 0h24v24H0z" fill="none"/>
                    <path
                        d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2zm-2 1H8v-6c0-2.48 1.51-4.5 4-4.5s4 2.02 4 4.5v6z"
                    />
                </svg>
                <img
                    alt="avatarXSAS"
                    :src="userSession.userAvatar"
                    class="w-9 h-9 rounded-full shadow-lg cursor-pointer"
                    @click="toggleDropdown"
                />
            </div>
            <!-- dropdown menu -->
            <div
                class="absolute bg-gray-100 border border-t-0 shadow-xl top-11 text-gray-700 rounded-b-lg w-48 right-0"
                :class="dropDownOpen ? '' : 'hidden'"
            >
                <router-link
                    :to="{ name: 'home' }"
                    :class="currentRouteName === 'home' ? 'bg-main-700' : 'hover:bg-gray-200'"
                    class="w-full flex items-center text-main-400 h-10 pl-4 rounded-lg cursor-pointer"
                >
          <span
              :class="currentRouteName === 'cuenta' ? 'text-white' : 'text-main-700'"
              class="pl-2"
          >Cuenta</span
          >
                </router-link>
                <a href="#" class="block px-4 py-2 hover:bg-gray-200">Configuración</a>
                <span @click="logout" class="block px-4 py-2 hover:bg-gray-200 cursor-pointer">Cerrar sesión</span>
            </div>
            <!-- dropdown menu end -->
        </nav>
    </section>
</template>

<script setup>
import {ref, computed, inject, onMounted} from 'vue';
import {useRouter, useRoute, RouterLink} from 'vue-router';
import {useUserPermissionsStore} from "@/stores/userSession";
// References for reactive data
const dropDownOpen = ref(false);
// plugins
const logoutPlugin = inject('userLogout')
// Router & Route
const router = useRouter();
const route = useRoute();
// Stores
const userPermissionsStore = useUserPermissionsStore();
import {storeToRefs} from 'pinia';

const {loadUserSession} = userPermissionsStore
const {userSession} = storeToRefs(userPermissionsStore)

// Current Route Name
const currentRouteName = computed(() => route.name);

// Toggle Dropdown
const toggleDropdown = () => {
    dropDownOpen.value = !dropDownOpen.value;
};
const logout = async () => {
    const logoutResult = await logoutPlugin();
    if (logoutResult) {
        router.push({name: 'login'});
    }
};

onMounted(async () => {
    loadUserSession();
})
</script>

<style scoped>
/* Add your styles here if necessary */
</style>
