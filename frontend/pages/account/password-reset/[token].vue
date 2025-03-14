<template>
  <section class="relative pt-16 pb-36 bg-gradient-gray2 overflow-hidden">
    <img class="absolute top-0 transform left-1/2 -translate-x-1/2" src="~assets/images/radial2.svg" alt="" />
    <div class="relative z-10 container mx-auto px-4">
      <img class="mx-auto mb-20" src="~assets/images/gradia-name-black.svg" alt="" />
      <div class="flex flex-wrap -m-6">
        <div class="w-full p-6">
          <div class="md:max-w-xl text-center mx-auto">
            <h2 class="mb-4 font-heading font-bold text-gray-900 text-6xl sm:text-7xl">Reset password</h2>
            <div>
              <!-- Reset Password Form -->
              <div
                v-if="!changeOk"
                class="py-10 px-2"
              >
                <form @submit.prevent="passwordReset" class="grid grid-cols-1 w-full gap-4">
                  <p class="text-justify pb-4">
                    Almost everything is done for password recovery. Now enter and confirm your new password
                  </p>
                  <input-float-label v-model="password1" :required="true" key="password1"
                                     tipo="password" class="md:mx-24">Password
                  </input-float-label>
                  <input-float-label v-model="password2" :required="true" key="password2"
                                     tipo="password" class="md:mx-24">Repeat your password
                  </input-float-label>

                  <div ref="errorSection">
                    <div class="text-red-600 text-md pb-4 text-left" v-for="error in errors">{{ error }}
                    </div>
                  </div>
                  <div class="flex justify-center">
                    <main-button class="w-1/2">
                      <div class="py-2">
                        Reset password
                      </div>
                    </main-button>
                  </div>
                </form>
              </div>
              <div class="px-4" v-else>
                <h4 class="text-center text-xl font-bold text-main-500">
                  Your password has been reset successfully!</h4>
                <p class="text-center">
                  Now you can
                  <nuxt-link to="/login"
                             class="font-semibold px-1 text-main-500">
                    login
                  </nuxt-link>
                  again
                </p>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

</template>

<script setup lang="ts">
import MainButton from '~/components/UI/MainButton.vue'
import InputFloatLabel from '~/components/UI/InputFloatLabel.vue'
import { PASSWORD_RESET } from '~/graphql/user'
import { useRoute } from 'vue-router'
import { ref } from 'vue'
import { ERROR_MESSAGES, type RegistrationErrors, type ValidationError } from '~/types/registration'


// Inicialización de utilidades
const { executeMutation } = useGraphQL()
const route = useRoute()

// Referencias reactivas
const changeOk = ref(false)
const password1 = ref<string | null>('')
const password2 = ref<string | null>('')
const errors = ref<string[]>([])
const errorSection = ref<HTMLElement | null>(null)

const passwordReset = async () => {
  /**
   * Maneja el cambio de contraseña del usuario, en este caso si el usuario ha olvidado la contraseña
   * Valida que los dos passwords sean válidad y procesa la respuesta del servidor, utilizando el
   * token de la url como parámetro
   */

  if (password1.value !== password2.value) {
    errors.value.push('Las contraseñas no coinciden')
    errorSection.value?.focus()
    return
  }
  const token = route.params.token
  const variables = { token: token, password: password1.value }

  const { passwordReset: resultPasswordReset } = await executeMutation(PASSWORD_RESET, variables)
  if (resultPasswordReset.success) {
    changeOk.value = true
  } else {
    errors.value.push(...handleRegistrationErrors(resultPasswordReset.errors))
    errorSection.value?.focus()
  }
}
const handleRegistrationErrors = (errors: RegistrationErrors): string[] => {
  const errorMessages: string[] = []

  // Handle field-specific errors
  if (errors.fieldErrors) {
    Object.entries(errors.fieldErrors).forEach(([_field, fieldErrors]) => {
      fieldErrors?.forEach((error: ValidationError) => {
        const message: string = ERROR_MESSAGES[error.code] || error.message || 'Error de validación'
        errorMessages.push(message)
      })
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
