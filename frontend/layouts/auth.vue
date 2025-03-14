<template>
  <section class="relative grid grid-cols-1 lg:grid-cols-2">
    <!-- Área de contenido principal (formularios, etc.) -->
    <div class="min-h-screen bg-main-400 flex justify-center items-center">
      <div class="w-full lg:w-1/2 m-auto">
        <div class="lg:max-w-md">
          <slot />
        </div>
      </div>
    </div>
    <!-- Área de ilustración/banner (lado derecho) -->
    <div class="h-96 lg:h-auto lg:absolute top-0 right-0 bottom-0 lg:w-1/2">
      <!-- Aquí puedes añadir imágenes/banners específicos de autenticación -->
    </div>
  </section>
</template>

<script setup lang="ts">
// Lógica específica para páginas de autenticación
</script>