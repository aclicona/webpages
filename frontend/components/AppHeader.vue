<template>
  <header
    class="sticky z-30 top-0 h-16 flex items-center justify-between px-2 lg:px-8 py-2 bg-[url(assets/images/bg-header.png)] bg-cover bg-no-repeat">
    <!-- Versión móvil - barra superior con botón de menú -->
    <div class="lg:hidden flex justify-between items-center px-2 py-3">
      <button @click="toggleMobileMenu" class="text-white focus:outline-none">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
             stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </div>
    <!--    Logo con link al home-->
    <div class="w-full lg:w-auto">
      <div class="flex flex-wrap items-center justify-center">
        <div class="w-auto">
          <NuxtLink to="/" class="text-2xl font-bold">
            <img src="~assets/images/gradia-name-white.svg" alt="" />
          </NuxtLink>
        </div>
      </div>
    </div>
    <!-- Versión para pantallas grandes -->
    <div class="hidden lg:flex justify-between items-center px-8 py-4">
      <!-- Acciones de usuario -->
      <div class="flex items-center space-x-4">
        <!-- Navegación principal -->
        <nav class="flex-1 mx-10">
          <ul class="flex space-x-6 justify-center">
            <li v-for="(item, index) in navItems" :key="index">
              <NuxtLink
                :to="item.route"
                class="font-heading mr-9 text-gray-300 hover:text-white text-lg transition-colors px-2 py-2"
                :class="{ 'font-black text-white': isActiveRoute(item.route) }"
              >
                {{ item.label }}
              </NuxtLink>
            </li>
          </ul>
        </nav>
        <div v-if="userSession.isLoggedIn" class="flex items-center space-x-2">
          <NuxtLink to="/account" class="h-10 w-10 rounded-full  items-center justify-center overflow-hidden">
            <img v-if="userSession.userAvatar" :src="userSession.userAvatar" alt="Avatar"
                 class="h-full w-full object-cover" />
            <span v-else class="text-lg">{{ getUserInitials() }}</span>
          </NuxtLink>
          <button @click="handleLogout"
                  class="group relative font-heading block py-2 px-5 text-lg text-white border-2 border-white overflow-hidden rounded-lg cursor-pointer">
            <div
              class="absolute top-0 left-0 transform -translate-y-full group-hover:-translate-y-0 h-full w-full bg-white transition ease-in-out duration-500"></div>
            <p class="relative z-10 group-hover:text-gray-800">Logout</p>
          </button>
        </div>
        <NuxtLink v-else to="/login"
                  class="group relative font-heading block py-2 px-5 text-lg text-white border-2 border-white overflow-hidden rounded-lg cursor-pointer">
          <div
            class="absolute top-0 left-0 transform -translate-y-full group-hover:-translate-y-0 h-full w-full bg-white transition ease-in-out duration-500"></div>
          <p class="relative z-10 group-hover:text-gray-800">Login</p>
        </NuxtLink>
      </div>
    </div>
  </header>
  <div v-if="isMobileMenuOpen" class="fixed top-0 left-0 bottom-0 w-4/6 sm:max-w-xs z-50 block inset-0 lg:hidden">
    <!-- Overlay para cerrar el menú al hacer clic fuera -->
    <div @click="toggleMobileMenu" class="fixed inset-0 bg-gray-800 opacity-80"></div>
    <nav class="relative z-60 px-9 py-8 bg-white h-full">
      <div class="flex flex-wrap justify-between h-full">
        <div class="w-full">
          <div class="flex items-center justify-between -m-2">
            <div class="w-auto p-2">
              <nuxt-link class="inline-block" to="/">
                <img src="~assets/images/gradia-name-black.svg" alt="" />
              </nuxt-link>
            </div>
            <div class="w-auto p-2">
              <button @click="toggleMobileMenu">
                <svg width="24" height="24" viewbox="0 0 24 24" fill="none"
                     xmlns="http://www.w3.org/2000/svg">
                  <path d="M6 18L18 6M6 6L18 18" stroke="#111827" stroke-width="2"
                        stroke-linecap="round" stroke-linejoin="round"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
        <div class="flex flex-col justify-center py-8 w-full">
          <ul>

            <li v-for="(item, index) in navItems" :key="index" class="mb-12">
              <NuxtLink
                :to="item.route"
                class="font-heading font-medium text-lg text-gray-900 hover:text-gray-700"
                :class="{ 'font-black': isActiveRoute(item.route) }"
              >
                {{ item.label }}
              </NuxtLink>
            </li>

          </ul>
        </div>
        <div class="flex flex-col justify-end w-full">
          <div class="flex flex-wrap">
            <div class="w-full">
              <div v-if="userSession.isLoggedIn" class="flex items-center space-x-2">
                <NuxtLink to="/account" class="h-10 w-10 rounded-full  items-center justify-center overflow-hidden">
                  <img v-if="userSession.userAvatar" :src="userSession.userAvatar" alt="Avatar"
                       class="h-full w-full object-cover" />
                  <span v-else class="text-lg">{{ getUserInitials() }}</span>
                </NuxtLink>
                <button @click="handleLogout"
                        class="group relative font-heading block py-2 px-5 text-lg text-neutral-900 border-2 border-neutral-900 overflow-hidden rounded-lg cursor-pointer">
                  <p class="relative z-10 group-hover:text-gray-800">Logout</p>
                </button>
              </div>
              <NuxtLink v-else to="/login"
                        class="group relative font-heading block py-2 px-5 text-lg text-neutral-900 border-2 border-neutral-900 overflow-hidden rounded-lg cursor-pointer">
                <p class="relative z-10 group-hover:text-gray-800">Login</p>
              </NuxtLink>
            </div>

          </div>
        </div>
      </div>
    </nav>


  </div>

</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

// Referencia al estado del menú móvil
const isMobileMenuOpen = ref(false)

// Store de usuario
const userStore = useUserPermissionsStore()
const userSession = computed(() => userStore.userSession)

// Instanciar funcionalidades de autenticación
const { logout } = useAuth()
const route = useRoute()

interface NavItem {
  label: string;
  route: string
}

// Elementos de navegación
const navItems = [
  { label: 'Account', route: '/account' }
] as NavItem[]


// Métodos
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const isActiveRoute = (path: string): boolean => {
  return route.path === path || route.path.startsWith(`${path}/`)
}

const getUserInitials = (): string => {
  if (!userSession.value.userName) return '?'

  return userSession.value.userName
    .split(' ')
    .map(name => name.charAt(0).toUpperCase())
    .slice(0, 2)
    .join('')
}

const handleLogout = async () => {
  await logout()
  isMobileMenuOpen.value = false
  navigateTo('/login')
}
</script>
<style scoped>
.bg-gradient-cyan {
  background-image: linear-gradient(90deg, rgba(108, 213, 246, 1) 0%, rgba(248, 157, 92, 1) 50%, rgba(91, 106, 240, 1) 100%)
}
</style>