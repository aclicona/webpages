<template>
  <section :class="sectionClasses" class="text-center">
    <div class="w-full flex flex-col justify-center">
      <h1 class="mb-4 font-heading font-bold text-neutral-900 text-6xl sm:text-7xl">{{ head }}</h1>
      <h2
        class="-translate-y-1/2 text-lg md:text-xl 2xl:text-xl font-medium text-neutral-700
        font-gentium"
      >
        {{ titleString }}
      </h2>
    </div>
  </section>
</template>

<script setup lang="ts">
interface Props {
  head?: string
  titleString?: string | null
  secondary?: boolean
}

// Define props with TypeScript interface
const props = withDefaults(defineProps<Props>(), {
  secondary: false
})

// Compute dynamic classes
const sectionClasses = computed(() => ({
  'mt-2 lg:mt-6 mb-2 lg:mb-4': !props.secondary,
  'mb-8': props.secondary
}))
</script>