<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
      <main>
          <slot />
      </main>

  </div>
</template>

<script setup lang="ts">
// Importar el componente del header
import AppHeader from '~/components/AppHeader.vue'
</script>