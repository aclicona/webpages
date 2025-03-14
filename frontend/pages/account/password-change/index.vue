<template>
  <section class="items-center">
    <div class="py-4 px-4 md:px-24 2xl:w-1/2" v-if="!changeOk">
      <form @submit.prevent="passwordChange" class="grid grid-cols-1 w-full gap-2">
        <input-float-label v-model="password" :required="true" key="password1"
                           tipo="password">Current password
        </input-float-label>
        <input-float-label v-model="password1" :required="true" key="password2"
                           tipo="password">New password
        </input-float-label>
        <input-float-label v-model="password2" :required="true" key="password2"
                           tipo="password">Repeat your password
        </input-float-label>
        <div ref="errorSection">
          <div class="text-red-600 text-md pb-4 text-left" v-for="error in errors">{{ error }}
          </div>
        </div>
        <div class="flex justify-center">
          <main-button class="w-8/12">
            <div class="py-2">
              Change password
            </div>
          </main-button>
        </div>

      </form>
    </div>
    <div class="py-10 px-4 md:px-24" v-else>
      <h4 class="text-center py-3 text-lg text-main-600">¡Tu contraseña ha sido cambiada!</h4>
      <p class="flex flex-wrap">Has cambiado exitosamente tu contraseña
      </p>
    </div>
    <div class="h-96 lg:h-auto top-0 right-0 bottom-0  bg-no-repeat bg-contain bg-center">
    </div>
  </section>
</template>

<script setup lang="ts">

import { ref } from 'vue'
import MainButton from '@/components/UI/MainButton.vue'
import InputFloatLabel from '@/components/UI/InputFloatLabel.vue'
import { PASSWORD_CHANGE } from '@/graphql/user'
import { ERROR_MESSAGES, type PasswordChangeErrors, type ValidationError } from '~/types/passwordChange'

definePageMeta({
  middleware: ['authentication'],
  layout: 'account',
  pageTitle: 'Password change'
})

const { executeMutation } = useGraphQL()

const changeOk = ref(false)
const password = ref<string | null>(null)
const password1 = ref<string | null>(null)
const password2 = ref<string | null>(null)
const errors = ref<string[]>([])
const errorSection = ref<HTMLElement | null>(null)

const passwordChange = async () => {
  if (password1.value !== password2.value) {
    errors.value.push('Las contraseñas no coinciden')
    errorSection.value?.focus()
    return
  }
  try {
    const variables = { oldPassword: password.value, newPassword: password1.value }
    const { passwordChange: resultPasswordChange } = await executeMutation(PASSWORD_CHANGE, variables)
    if (resultPasswordChange.success) {
      changeOk.value = true
    } else {
      errors.value.push(...handleChangeErrors(resultPasswordChange.errors))
      errorSection.value?.focus()
    }
  } catch (error) {
    console.error('Change password error:', error)
    errors.value.push('Error en el cambio de contraseña. Por favor, intenta nuevamente.')
    errorSection.value?.focus()
  }
}
const handleChangeErrors = (errors: PasswordChangeErrors): string[] => {
  const errorMessages: string[] = []

  // Handle field-specific errors
  // Check and process oldPassword errors if they exist
  if (errors.oldPassword) {
    errors.oldPassword.forEach((error: ValidationError) => {
      const message: string = ERROR_MESSAGES[error.code] || error.message || 'Error de validación'
      errorMessages.push(message)
    })
  }
  if (errors.newPassword2) {
    errors.newPassword2.forEach((error: ValidationError) => {
      const message: string = ERROR_MESSAGES[error.code] || error.message || 'Error de validación'
      errorMessages.push(message)
    })
  }
  if (errors.nonFieldErrors) {
    errors.nonFieldErrors.forEach((error: ValidationError) => {
      const message: string = ERROR_MESSAGES[error.code] || error.message || 'Error de validación'
      errorMessages.push(message)
    })
  }

  // Handle general errors
  if (errors.generalErrors) {
    errorMessages.push(...errors.generalErrors)
  }

  // Handle server error
  if (errors.serverError) {
    errorMessages.push(errors.serverError.message)
  }
  return errorMessages
}

</script>

<style scoped>

</style>