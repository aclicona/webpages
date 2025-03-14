<template>
  <div>
    <h3 class="text-xl font-semibold text-main-600 mb-6">Personal information</h3>

    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-main-500"></div>
    </div>

    <div v-else-if="userInfo" class="space-y-6">
      <!-- User profile section -->
      <div class="flex items-center space-x-4 mb-8">
        <div class="h-20 w-20 rounded-full bg-main-200 flex items-center justify-center overflow-hidden">
          <img v-if="userInfo.avatar" :src="userInfo.avatar" alt="Avatar" class="h-full w-full object-cover"/>
          <span v-else class="text-2xl font-bold text-main-600">{{ getUserInitials() }}</span>
        </div>

        <div>
          <h4 class="text-lg font-medium text-gray-900">{{ `${userInfo.firstName} ${userInfo.lastName || ''}` }}</h4>
          <p class="text-gray-500">{{ userInfo.email }}</p>
        </div>
      </div>

      <!-- User details form -->
      <form @submit.prevent="updateProfile" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <input-float-label v-model="form.firstName" :required="true" tipo="text">
              Name
            </input-float-label>
          </div>

          <div>
            <input-float-label v-model="form.lastName" tipo="text">
              Last name
            </input-float-label>
          </div>
        </div>

        <div>
          <input-float-label v-model="form.email" :required="true" tipo="email" :readonly="true">
            Email
          </input-float-label>
          <p class="text-xs text-gray-500 mt-1">The email can't be changed</p>
        </div>

        <div ref="errorSection">
          <div
            v-for="(error, index) in errors"
            :key="index"
            class="text-red-600 text-md pb-4 text-left"
          >
            {{ error }}
          </div>
        </div>

        <div class="flex justify-end">
          <main-button class="w-auto px-6">
            <div class="px-4">
              Update information
            </div>
          </main-button>
        </div>
      </form>
    </div>

    <div v-else class="py-4 text-center text-gray-500">
      No se pudo cargar la información del usuario.
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ME_QUERY } from '~/graphql/user'
import InputFloatLabel from '~/components/UI/InputFloatLabel.vue'
import MainButton from '~/components/UI/MainButton.vue'

definePageMeta({
  middleware: ['authentication'],
  layout: 'account',
  pageTitle: 'Personal information'
})

// GraphQL client
const { executeQuery, loading } = useGraphQL()

// Reactive state
const userInfo = ref<any>(null)
const errors = ref<string[]>([])
const errorSection = ref<HTMLElement | null>(null)

// Form data
const form = reactive({
  firstName: '',
  lastName: '',
  email: ''
})

// Get user initials for avatar placeholder
const getUserInitials = (): string => {
  if (!userInfo.value) return '?'

  return [userInfo.value.firstName, userInfo.value.lastName]
    .filter(Boolean)
    .map(name => name.charAt(0).toUpperCase())
    .slice(0, 2)
    .join('')
}

// Load user information
const loadUserInfo = async () => {
  try {
    const { me } = await executeQuery(ME_QUERY)
    userInfo.value = me

    // Populate form
    form.firstName = me.firstName || ''
    form.lastName = me.lastName || ''
    form.email = me.email || ''
  } catch (error) {
    console.error('Error fetching user info:', error)
    errors.value.push('No se pudo cargar la información del usuario')
  }
}

// Update profile information
const updateProfile = async () => {
  errors.value = []

  // Form validation
  if (!form.firstName.trim()) {
    errors.value.push('El nombre es requerido')
    errorSection.value?.focus()
    return
  }

  // Here you would implement the actual update logic with a GraphQL mutation
  // This is a placeholder for demonstration purposes
  try {
    // Example mutation call (commented out since it doesn't exist in your current schema)
    // const result = await executeMutation(UPDATE_PROFILE_MUTATION, {
    //   firstName: form.firstName,
    //   lastName: form.lastName
    // })

    // For now, just show a success message
    alert('Información actualizada correctamente')
  } catch (error) {
    console.error('Error updating profile:', error)
    errors.value.push('Error al actualizar la información')
    errorSection.value?.focus()
  }
}

// Load user data on component mount
onMounted(async () => {
  await loadUserInfo()
})
</script>