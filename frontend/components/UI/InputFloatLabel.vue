<template>
  <div :class="wrapperClasses" class="group relative h-10 input-component">
    <input
      :id="id"
      :class="inputClasses"
      :list="listId"
      :maxlength="maxlength"
      :name="name"
      ref="inputRef"
      :required="required"
      :type="inputType"
      :value="modelValue"
      :readonly="readonly"
      @blur="checkEmpty"
      @focusin="deformatValue"
      @focusout="formatValue"
      @input="handleInput"
      class="px-3 py-2 bg-white border shadow-sm placeholder-slate-400 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-500 focus:outline-none focus:border-main-600 focus:ring-main-600 block w-full rounded-sm sm:text-sm focus:ring-0 focus:invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500 disabled:shadow-none"
    />
    <label
      :for="id"
      :class="labelClasses"
      @click="focusInput"
      class="select-none transform -translate-y-1/2 w-fit top-0 text-sm absolute left-2 transition-all bg-white px-1 rounded-sm text-left"
    >
      <slot />
    </label>
    <label v-if="alertEmpty" class="text-pink-500 text-sm">Campo requerido</label>
    <datalist v-if="list" :id="listId">
      <option v-for="element in list" :key="element.name">{{ element.name }}</option>
    </datalist>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

interface ListItem {
  name: string;

  [key: string]: any;
}

interface Props {
  modelValue?: any;
  tipo?: 'text' | 'number' | 'float' | 'currency' | 'email' | 'password';
  list?: ListItem[];
  maxlength?: number;
  minvalue?: number;
  maxvalue?: number;
  readonly?: boolean;
  required?: boolean;
  name?: string;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  tipo: 'text',
  readonly: false,
  required: false
})

const emit = defineEmits<{
  'update:modelValue': [value: any]
}>()

const id = `input-${Math.random().toString(36).substr(2, 9)}`
const alertEmpty = ref(false)
const inputRef = ref<HTMLInputElement>()

const wrapperClasses = computed(() => ({
  'empty': !props.modelValue,
  'mb-10': alertEmpty.value
}))

const inputClasses = computed(() => ({
  'border-pink-500': alertEmpty.value,
  'border-neutral-400': !alertEmpty.value,
  'bg-teal-100': props.readonly
}))

const labelClasses = computed(() =>
  props.modelValue ? 'text-main-500' : 'text-neutral-800'
)

const listId = computed(() => props.list ? `list-${id}` : '')

const inputType = computed(() =>
  ['number', 'float'].includes(props.tipo) ? 'number' : props.tipo
)

const formatMoney = (value: number): string => {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP'
  }).format(value)
}

const deformatValue = (event: Event) => {
  if (props.tipo === 'currency') {
    const target = event.target as HTMLInputElement
    target.value = target.value.replace(/[$ .]/g, '').replace(',', '.')
  }
}

const formatValue = (event: Event) => {
  if (props.tipo === 'currency') {
    const target = event.target as HTMLInputElement
    target.value = formatMoney(Number(target.value))
  }
}

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  let value = target.value

  if (['number', 'float'].includes(props.tipo)) {
    const numValue = Number(value)
    if (props.maxvalue && numValue > props.maxvalue) {
      value = props.maxvalue.toString()
      target.value = value
    }
    emit('update:modelValue', numValue || null)
    return
  }

  if (props.list) {
    const found = props.list.find(item => item.name === value)
    emit('update:modelValue', found?.name ?? null)
    return
  }

  emit('update:modelValue', value || null)
}

const checkEmpty = (event: Event) => {
  const target = event.target as HTMLInputElement
  alertEmpty.value = target.value === '' && props.required
}

const focusInput = () => {
  inputRef.value?.focus()
}

onMounted(() => {
  if (!inputRef.value) return

  switch (props.tipo) {
    case 'float':
      inputRef.value.pattern = '[0-9.-]'
      inputRef.value.step = '0.01'
      break
    case 'number':
      inputRef.value.pattern = '[-0-9]'
      inputRef.value.step = '1'
      break
    case 'currency':
      inputRef.value.pattern = '[0-9.-]'
      inputRef.value.step = '0.1'
      inputRef.value.value = formatMoney(Number(inputRef.value.value))
      break
  }
})
</script>

<style scoped>
@reference "../../assets/css/main.css";
.empty input:not(:focus) + label {
  @apply text-sm top-1/2 -translate-y-1/2 w-full max-w-inputlabel;
}

input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
}
</style>