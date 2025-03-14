<script setup>
import {computed, defineProps, inject} from "vue";
import {useRoute} from "vue-router";
import {storeToRefs} from 'pinia';
import {useSessionStore} from '@/stores/session'
// Access the Pinia store
const sessionStore = useSessionStore();
const {sideBarOpen} = storeToRefs(sessionStore);
const userManager = inject('userManager')
// Props
const props = defineProps({
  urlName1: {
    type: String,
    required: true
  },
  urlName2: {
    type: String,
    required: false
  },
  elementName: {
    type: String,
    required: true
  },
  counter: {
    type: Number,
    required: false,
    default: null
  },
  groups: {
    type: Array,
    required: false,
    validator(value) {
      // Check if every element in the array is a string
      return value.every(item => typeof item === 'string');
    }
  }
});

// Vue router's route object
const route = useRoute();

// Computed property to get the current route name
const currentRouteName = computed(() => route.name);

// Computed property to check if the current route is active
const isActiveRoute = computed(() =>
    currentRouteName.value === props.urlName1 || currentRouteName.value === props.urlName2
);

const authorized = computed(() => {
    return userManager.authorizedOption({groups: props.groups})
})
</script>

<template>
  <div>
    <router-link
        :to="{ name: urlName1 }"
        :class="isActiveRoute ? 'bg-main-100 text-main-700' : 'hover:bg-main-50 text-neutral-500'"
        class="flex items-center h-7 xl:h-10 rounded cursor-pointer px-4 w-full"
        v-if="authorized"
        :title="elementName"
    >
      <slot></slot>
      <span v-if="sideBarOpen"
            class="pl-2 text-sm xl:text-base"
      >
                {{ elementName }}
            </span>
      <span v-if="counter && sideBarOpen"
            class="flex justify-center items-center ml-auto bg-main-500 w-6 h-6 text-white text-xs rounded-full">
                {{ counter }}</span>
    </router-link>
  </div>
</template>
