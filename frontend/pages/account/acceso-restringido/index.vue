<template>
  <section class="px-8 md:px-24 2xl:px-72 text-neutral-600">
    <main-title head="Seguridad"
                title-string="Acceso restringido" />
    El recurso al que intenta acceder es de uso restringido.
    <div class="flex justify-center">
      <img src="~assets/images/acceso_denegado.jpg" class="w-3/4 md:w-1/2" alt="Acceso denegado">
    </div>
  </section>

</template>

<script setup lang="ts">
import MainTitle from '@/components/UI/MainTitle.vue'
</script>

<style scoped>

</style>