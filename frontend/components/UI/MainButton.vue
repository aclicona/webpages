<template xmlns="">


    <button :disabled="!enabled"
            :class="[enabled ? 'cursor-pointer' : 'cursor-not-allowed']"
            class="p-1 w-full font-heading font-medium text-base text-white overflow-hidden rounded-md">
        <div :class="[enabled ? 'bg-gradient-to-r from-blue-300 to-blue-700' : 'bg-neutral-500']"
            class="relative py-4 px-9 bg-gradient-to-r from-blue-300 to-blue-700 overflow-hidden rounded-md">
            <div
                class="absolute top-0 left-0 transform -translate-y-full group-hover:-translate-y-0 h-full w-full bg-gray-900 transition ease-in-out duration-500"></div>
            <p class="relative z-10">
                <slot></slot>
            </p>
        </div>
    </button>
</template>

<script setup lang="ts">

defineProps({
    enabled: {
        type: Boolean,
        required: false,
        default: true
    }
})
</script>

<style scoped>
/*  No styles needed here as the classes are directly in the template */
</style>