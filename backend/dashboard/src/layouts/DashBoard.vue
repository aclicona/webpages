<template>
  <div class="leading-normal tracking-normal flex flex-wrap min-h-screen" id="main-body">
    <Sidebar />
    <div :class="sideBarOpen ? 'lg:ml-80' : 'lg:ml-14'" class="mx-1 w-full min-h-screen relative" id="main-content">
      <Navbar />
      <div id="alert-block"></div>
      <div class="p-4">
        <router-view />
      </div>
    </div>
  </div>

</template>

<script setup>
import Sidebar from '@/components/sidebar/SideBar.vue'
import Navbar from '@/layouts/NavBar.vue'
import { storeToRefs } from 'pinia'
import { useSessionStore } from '@/stores/session'
// Access the Pinia store
const sessionStore = useSessionStore()
const { sideBarOpen } = storeToRefs(sessionStore)
</script>

<style scoped>

</style>