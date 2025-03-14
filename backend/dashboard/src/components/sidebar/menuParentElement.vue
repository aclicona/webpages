<script setup>
import {ref, defineProps, inject, computed} from 'vue';

const userManager = inject('userManager')
import {storeToRefs} from 'pinia';
import {useSessionStore} from '@/stores/session'
// Access the Pinia store
const sessionStore = useSessionStore();
const {sideBarOpen} = storeToRefs(sessionStore);
// Props
const props = defineProps({
    elementName: {
        type: String,
        required: true
    },
    groups: {
        type: Array,
        required: false,
        default: () => [],
        validator(value) {
            // Check if every element in the array is a string
            return value.every(item => typeof item === 'string');
        }
    },
    visible: {
        type: Boolean,
        required: false,
        default: false
    }
});

// Helper function to check group authorization

const authorized = computed(() => {
    return userManager.authorizedOption({groups: props.groups})
})

// Ref for visibility
const isVisible = ref(props.visible);

// Toggle visibility function
const toggleVisible = () => {
    isVisible.value = !isVisible.value;
};
</script>

<template>
    <div
        :class="isVisible ? 'bg-main-200' : 'hover:bg-main-50'"
        class="flex items-center h-7 xl:h-10 rounded cursor-pointer text-main-700 px-4 w-full"
        v-if="authorized"
        @click="toggleVisible"
        :title="elementName"
    >
        <slot></slot>
        <span v-if="sideBarOpen" class="pl-2 text-sm xl:text-base">
            {{ elementName }}{{authorized}}
        </span>
        <span v-if="sideBarOpen" class="inline-block ml-auto">
            <svg :class="{'rotate-180': isVisible}" class="transform transition-transform duration-500 w-3 h-3"
                 viewBox="0 0 10 6" fill="none"
                 xmlns="http://www.w3.org/2000/svg">
              <path
                  d="M9.08329 0.666626C8.74996 0.333293 8.24996 0.333293 7.91663 0.666626L4.99996 3.58329L2.08329 0.666626C1.74996 0.333293 1.24996 0.333293 0.916626 0.666626C0.583293 0.999959 0.583293 1.49996 0.916626 1.83329L4.41663 5.33329C4.58329 5.49996 4.74996 5.58329 4.99996 5.58329C5.24996 5.58329 5.41663 5.49996 5.58329 5.33329L9.08329 1.83329C9.41663 1.49996 9.41663 0.999959 9.08329 0.666626Z"
                  fill="currentColor"></path>
            </svg>
        </span>
    </div>
    <slot name="children" v-if="isVisible && authorized"></slot>
</template>
