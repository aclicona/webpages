<template>
  <div :class="{ 'empty': isEmpty, 'mb-10': alertEmpty }" class="group relative h-10 input-component">
    <input
      :class="{ 'border-pink-500': alertEmpty, 'border-neutral-400': !alertEmpty, 'bg-teal-100': readonly }"
      :id="id"
      :list="(list ? 'list-' + id : '')"
      :maxlength="maxlength"
      :name="name"
      ref="inputRef"
      :required="required"
      :type="inputType"
      :value="modelValue"
      :readonly="readonly"
      @blur="checkIfAlert"
      @focus="unformatValue"
      @input="handleInput"
      class="px-3 py-2 bg-white border shadow-sm placeholder-slate-400 disabled:bg-slate-50
             disabled:text-slate-500 disabled:border-slate-500 focus:outline-none
             focus:border-main-600 focus:ring-main-600 block w-full rounded-sm sm:text-sm
             focus:ring-0 focus:invalid:text-pink-600 focus:invalid:border-pink-500
             focus:invalid:ring-pink-500 disabled:shadow-none"
    />
    <label
      :class="modelValue ? 'text-main-500' : 'text-neutral-800'"
      @click="focusInput"
      class="select-none transform -translate-y-1/2 w-fit top-0 text-sm absolute left-2 transition-all bg-white px-1 rounded-sm"
      :for="id"
    >
      <slot></slot>
    </label>
    <label class="text-pink-500 text-sm" v-if="alertEmpty">Campo requerido</label>
    <datalist :id="'list-' + id" v-if="list">
      <option v-for="(element, index) in list" :key="'option-' + index">{{ element.name }}</option>
    </datalist>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

const props = withDefaults(defineProps<{
  modelValue: string | number | null;
  tipo?: string;
  list?: { name: string }[];
  maxlength?: number;
  minvalue?: number;
  maxvalue?: number;
  readonly?: boolean;
  required?: boolean;
  name?: string;
}>(), {
  modelValue: null,
  tipo: 'text',
  list: undefined,
  maxlength: undefined,
  minvalue: undefined,
  maxvalue: undefined,
  readonly: false,
  required: false,
  name: undefined,
});

const emit = defineEmits(['update:modelValue']);

const id = `input-${Math.random().toString(36).slice(2, 11)}`; // More concise random ID
const alertEmpty = ref(false);
const inputRef = ref<HTMLInputElement | null>(null);

const inputType = computed(() => props.tipo === 'number' || props.tipo === 'float' ? 'number' : props.tipo);
const isEmpty = computed(() => props.modelValue === '' || props.modelValue === null); // Computed for emptiness

const formatCurrency = (value: number | string): string => {
  return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(Number(value));
};

const unformatValue = () => {
  if (props.tipo === 'currency' && inputRef.value) {
    inputRef.value.value = inputRef.value.value.replace(/[$ .]/g, '').replace(',', '.');
  }
};

const formatValue = () => {
  if (props.tipo === 'currency' && inputRef.value) {
    inputRef.value.value = formatCurrency(inputRef.value.value);
  }
};

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = target.value;

  if (props.tipo === 'number' || props.tipo === 'float') {
    const numValue = Number(value) || null;
    if (props.maxvalue && numValue > props.maxvalue) {
      target.value = String(props.maxvalue);
      emit('update:modelValue', props.maxvalue);
      return;
    }
    emit('update:modelValue', numValue);
  } else if (props.list) {
    const selectedItem = props.list.find(item => item.name === value);
    emit('update:modelValue', selectedItem ? selectedItem.name : null);
  } else {
    emit('update:modelValue', value || null);
  }
};

const checkIfAlert = () => {
  alertEmpty.value = inputRef.value?.value === '' && props.required;
};

const focusInput = () => {
  inputRef.value?.focus();
};

onMounted(() => {
  if (inputRef.value) {  // Check if inputRef is available
    if (props.tipo === 'float') {
      inputRef.value.pattern = '[0-9.-]';
      inputRef.value.step = '0.01';
    } else if (props.tipo === 'number') {
      inputRef.value.pattern = '[-0-9]';
      inputRef.value.step = '1';
    } else if (props.tipo === 'currency') {
      inputRef.value.pattern = '[0-9.-]';
      inputRef.value.step = '0.1';
      inputRef.value.value = formatCurrency(props.modelValue || 0);
    }
  }
});
</script>

<style scoped>
/* ... (styles remain the same) */
</style>