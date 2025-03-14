<template>
  <section class="relative pt-16 pb-36 bg-gradient-gray2 overflow-hidden">
    <img class="absolute top-0 transform left-1/2 -translate-x-1/2" src="~assets/images/radial2.svg" alt="" />
    <div class="relative z-10 container mx-auto px-4">
      <img class="mx-auto mb-20" src="~assets/images/gradia-name-black.svg" alt="" />
      <div class="flex flex-wrap -m-6">
        <div class="w-full p-6">
          <div class="md:max-w-xl text-center mx-auto">
            <h2 class="mb-4 font-heading font-bold text-gray-900 text-6xl sm:text-7xl">Login to get
              access</h2>
            <p class="mb-11 text-lg text-gray-500">Lorem ipsum dolor sit ame a ver.</p>
            <form @submit.prevent="handleSubmit" class="flex flex-wrap max-w-md mx-auto -m-2 mb-5">
              <div class="w-full p-2">
                <InputFloatLabel
                  class="w-full"
                  :required="true"
                  v-model="email"
                  tipo="email"
                >
                  Email
                </InputFloatLabel>

              </div>
              <div class="w-full p-2">
                <InputFloatLabel
                  class="w-full"
                  :required="true"
                  v-model="password"
                  tipo="password"
                >
                  Password
                </InputFloatLabel>
              </div>
              <div ref="errorSection">
                <div class="text-red-600 text-md pb-4 text-left" v-for="error in errors">{{ error }}
                </div>
              </div>
              <div class="w-full p-2">
                  <MainButton>Login</MainButton>
              </div>
            </form>
            <p class="text-base text-gray-600">
              <nuxt-link class="text-main-400 hover:text-main-600 cursor-pointer" to="/account/forgot-password">
                Forgot password?
              </nuxt-link>
            </p>
            <p class="text-base text-gray-600">
              <span>Don’t have an account? </span>
              <nuxt-link class="text-main-400 hover:text-main-600 cursor-pointer" to="/account/register">Create free
                account
              </nuxt-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>

</template>

<script setup lang="ts">
import MainButton from '~/components/UI/MainButton.vue'
import type { Ref } from 'vue'
import { ref } from 'vue'
import { navigateTo, useRoute } from '#app'
import InputFloatLabel from '~/components/UI/InputFloatLabel.vue'
import { ERROR_MESSAGES, type LoginErrors, type ValidationError } from '~/types/login'

definePageMeta({
  middleware: ['authentication']
})

const { login } = useAuth()

interface Credentials {
  email: string | null;
  password: string | null;
}

const email: Ref<string | null> = ref('')
const password: Ref<string | null> = ref('')
const errors = ref<string[]>([])
const errorSection = ref<HTMLElement | null>(null)
const route = useRoute()

const handleSubmit = async () => {
  errors.value = []
  const credentials: Credentials = {
    email: email.value,
    password: password.value
  }

  try {
    const result = await login(credentials)
    if (result) {
      if (result.success) {
        const redirectParam = route.query.redirect
        const redirectUrl = Array.isArray(redirectParam) ? redirectParam[0]?.toString() : redirectParam?.toString() || '/'
        await navigateTo(redirectUrl)
      } else {
        errors.value.push(...handleLoginErrors(result.errors))
        errorSection.value?.focus()
      }
    }
  } catch (error) {
    console.error('An error occurred during login:', error)
  }
}

const handleLoginErrors = (errors: LoginErrors): string[] => {
  const errorMessages: string[] = []

  // Handle field-specific errors
  if (errors.nonFieldErrors) {
    Object.entries(errors.nonFieldErrors).forEach(([_, error]: [string, ValidationError]) => {
      errorMessages.push(ERROR_MESSAGES[error.code] || error.message || 'Error de validación')
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