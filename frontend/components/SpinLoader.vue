<template>
  <div
    :class="[
      'flex items-center justify-center',
      fullScreen ? 'fixed inset-0 z-50 bg-white/80' : 'w-full py-6'
    ]"
  >
    <div
      :class="[
        'rounded-full animate-spin',
        sizeClasses,
        colorClasses
      ]"
    >
      <div class="h-full w-full rounded-full border-4 border-t-transparent" :class="borderColorClass"></div>
    </div>
    <span v-if="label" class="ml-3 font-medium text-gray-600">{{ label }}</span>
  </div>
</template>

<script setup lang="ts">
interface Props {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  color?: 'main' | 'secondary' | 'gray' | 'blue' | 'red';
  fullScreen?: boolean;
  label?: string;
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  color: 'main',
  fullScreen: false,
  label: ''
});

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16'
  };
  return sizes[props.size];
});

const colorClasses = computed(() => {
  const colors = {
    main: 'border-main-500',
    secondary: 'border-teal-500',
    gray: 'border-gray-500',
    blue: 'border-blue-500',
    red: 'border-red-500'
  };
  return colors[props.color];
});

const borderColorClass = computed(() => {
  const borderColors = {
    main: 'border-main-200',
    secondary: 'border-teal-200',
    gray: 'border-gray-200',
    blue: 'border-blue-200',
    red: 'border-red-200'
  };
  return borderColors[props.color];
});
</script>