<template>
  <section class="relative pt-16 pb-36 bg-gradient-gray2 overflow-hidden">
    <img class="absolute top-0 transform left-1/2 -translate-x-1/2" src="~assets/images/radial2.svg" alt="" />
    <div class="relative z-10 container mx-auto px-4">
      <img class="mx-auto mb-10" src="~assets/images/gradia-name-black.svg" alt="" />
      <div class="flex flex-wrap -m-6">
        <div class="w-full p-6">
          <div class="md:max-w-xl text-center mx-auto">
            <MainTitle head="Forgot password?"/>
            <div>
              <!-- Reset Password Form -->
              <div
                v-if="!emailOk"
                class="py-10 px-2"
              >
                <form
                  @submit.prevent="resetPassword"
                  class=""
                >
                  <p class="text-center pb-4">
                    Type your email and we will send you a message for access recovery
                  </p>
                  <div class="w-full p-2">

                    <input-float-label
                      v-model="email"
                      required
                      key="email"
                      class="md:mx-24"
                      tipo="email"
                    >
                      Email
                    </input-float-label>
                  </div>
                  <div
                    ref="errorSection"
                    class="md:mx-24"
                  >
                    <div
                      v-for="error in errors"
                      :key="error"
                      class="text-red-600 text-md pb-4 text-left"
                    >
                      {{ error }}
                    </div>
                  </div>
                  <div class="w-full p-2">
                    <MainButton>Recover access</MainButton>
                  </div>
                </form>
              </div>

              <!-- Success Message -->
              <div v-else
                   class="px-4"
              >
                <h4 class="text-center py-3 text-2xl text-main-500 font-bold">
                  Done, your request has been processed!
                </h4>

                <div class="text-justify">
                  <p>
                    We have sent a message with instructions to reset your password to the email {{ email }}.
                  </p>
                  <p>
                    If you don't see it, check your spam folder or contact our customer service department.
                  </p>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </section>
</template>
<script setup lang="ts">
import { ref, computed } from 'vue'
import MainButton from '@/components/UI/MainButton.vue'
import InputFloatLabel from '@/components/UI/InputFloatLabel.vue'
import MainTitle from '@/components/UI/MainTitle.vue'
import { PASSWORD_RESET_EMAIL } from '@/graphql/user'
import { ERROR_MESSAGES, type ForgotPasswordErrors, type ValidationError } from '~/types/forgotPassword'
import SpinLoader from '~/components/SpinLoader.vue'

definePageMeta({
  middleware: ['authentication']
})

interface ResetPasswordResponse {
  sendPasswordResetEmail: {
    success: boolean
    errors?: ForgotPasswordErrors
  }
}

// Composables
const { isValidEmail } = useValidateEmail()
const { executeMutation } = useGraphQL()

// Reactive state
const email = ref<string>('')
const emailOk = ref(false)
const errors = ref<string[]>([])
const errorSection = ref<HTMLElement | null>(null)

// Computed
const isValidForm = computed(() =>
  isValidEmail(email.value) && email.value.trim() !== ''
)

// Methods
const handleErrors = (errors: ForgotPasswordErrors): string[] => {
  const errorMessages: string[] = []

  if (errors.fieldErrors) {
    Object.entries(errors.fieldErrors).forEach(([_, fieldErrors]) => {
      fieldErrors?.forEach((error: ValidationError) => {
        errorMessages.push(ERROR_MESSAGES[error.code] || error.message || 'Error de validación')
      })
    })
  }

  if (errors.generalErrors) {
    errorMessages.push(...errors.generalErrors)
  }

  if (errors.serverError) {
    errorMessages.push(errors.serverError.message)
  }

  return errorMessages
}

const resetPassword = async () => {
  errors.value = [] // Clear previous errors

  if (!isValidForm.value) {
    errors.value.push('Ingrese un email válido')
    errorSection.value?.focus()
    return
  }

  try {
    const { sendPasswordResetEmail } = await executeMutation(
      PASSWORD_RESET_EMAIL,
      { email: email.value }
    ) as ResetPasswordResponse
    emailOk.value = sendPasswordResetEmail.success
    if (sendPasswordResetEmail.errors) {
      errors.value = handleErrors(sendPasswordResetEmail.errors)
      errorSection.value?.focus()
    }
  } catch (error) {
    console.error('Forgot password error:', error)
    errors.value.push('Error en la solicitud para enviar correo. Por favor, intenta nuevamente.')
  }
}
</script>
