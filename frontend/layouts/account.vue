<template>
    <!-- Inherit from default layout -->
    <NuxtLayout name="default">
        <section class="px-8 md:px-24 2xl:px-72 text-neutral-600">
            <MainTitle head="Account" :title-string="pageTitle"/>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mt-8">
                <!-- Sidebar navigation -->
                <div class="md:col-span-1">
                    <div class="bg-white rounded-lg shadow-sm p-4 sticky top-20">
                        <h3 class="text-lg font-semibold text-main-600 mb-4 border-b pb-2">My account</h3>
                        <nav class="space-y-2">
                            <NuxtLink
                                to="/account"
                                class="flex items-center py-2 px-3 rounded-md transition-colors"
                                :class="[isActiveRoute('/account') && !hasSubPath ? 'bg-main-100 text-main-600' : 'hover:bg-gray-100']"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                                Personal information
                            </NuxtLink>

                            <NuxtLink
                                to="/account/password-change"
                                class="flex items-center py-2 px-3 rounded-md transition-colors"
                                :class="[isActiveRoute('/account/password-change') ? 'bg-main-100 text-main-600' : 'hover:bg-gray-100']"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                                Password change
                            </NuxtLink>

                            <div v-if="userHasStaffRole" class="pt-2 mt-2 border-t">
                                <h4 class="text-sm font-semibold text-neutral-500 mb-2 px-3">Administration</h4>

                                <NuxtLink
                                    to="/account/create-staff-user"
                                    class="flex items-center py-2 px-3 rounded-md transition-colors"
                                    :class="[isActiveRoute('/account/create-staff-user') ? 'bg-main-100 text-main-600' : 'hover:bg-gray-100']"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                                    </svg>
                                    Create staff user
                                </NuxtLink>
                            </div>

                            <div class="pt-2 mt-4">
                                <button
                                    @click="handleLogout"
                                    class="cursor-pointer flex items-center py-2 px-3 w-full text-left rounded-md hover:bg-red-50 text-red-600 transition-colors"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                    </svg>
                                    Logout
                                </button>
                            </div>
                        </nav>
                    </div>
                </div>

                <!-- Main content area -->
                <div class="md:col-span-3 bg-white rounded-lg shadow-sm p-6">
                    <slot/>
                </div>
            </div>
        </section>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import MainTitle from '~/components/UI/MainTitle.vue'

const route = useRoute()
const pageTitle = ref<string | null>(null)
const userHasStaffRole = ref(true) // This should be determined by user roles from your auth system

// Set page title from route meta
pageTitle.value = route.meta.pageTitle as string || 'Mi Cuenta'

// Check if route is active
const isActiveRoute = (path: string): boolean => {
    return route.path === path || route.path.startsWith(`${path}/`)
}

// Check if current route has subpaths
const hasSubPath = computed(() => {
    return route.path !== '/account' && route.path.startsWith('/account/')
})

// Logout handler
const { logout } = useAuth()
const handleLogout = async () => {
    await logout()
    navigateTo('/login')
}
</script>

<style scoped>
/* Any additional scoped styles can go here */
</style>