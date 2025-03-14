<template>
  <section class="relative pt-16 pb-36 bg-gradient-gray2 overflow-hidden">
    <img class="absolute top-0 transform left-1/2 -translate-x-1/2" src="~assets/images/radial2.svg" alt="" />
    <div class="relative z-10 container mx-auto px-4">
      <img class="mx-auto mb-20" src="~assets/images/gradia-name-black.svg" alt="" />
      <div class="flex flex-wrap -m-6">
        <div class="w-full p-6">
          <div class="md:max-w-xl text-center mx-auto">
            <h2 class="mb-4 font-heading font-bold text-gray-900 text-6xl sm:text-7xl">Account activation</h2>
            <div v-if="loading">
              <p class="mb-11 text-lg text-gray-500">Lorem ipsum dolor sit ame a ver.</p>
              <SpinLoader size="xl" />
            </div>
            <div v-else>
              <div class="text-center px-4 md:px-24" v-if="success">
                <h4 class="text-center py-3 text-2xl text-main-600 md:pt-28">¡Tu cuenta ha sido activada!</h4>
                <div class="flex flex-wrap">
                  <p class="text-justify">Ahora está todo listo. Ya puedes
                    <nuxt-link to="/login"
                               class="font-semibold mx-1 text-main-600 hover:text-main-600 border-b">
                      iniciar sesión
                    </nuxt-link>
                    con tu cuenta
                  </p>
                </div>
              </div>
              <div class="px-4 md:px-24" v-else>
                <h4 class="text-center text-3xl text-main-600">¡Uups. Algo salió mal!</h4>
                <div class="flex flex-wrap">
                  <p>No hemos podido verificar tu cuenta por esta razón:
                  </p>
                </div>
                <div ref="errorSection">
                  <div class="text-red-600 text-md pb-4 text-left" v-for="error in errors">{{ error }}
                  </div>
                </div>
                <div class="flex flex-wrap">
                  <p>Haz
                    <nuxt-link to="/account/register/resend-activation-email"
                               class="font-semibold mx-1 text-main-600 hover:text-main-600">
                      clic aquí
                    </nuxt-link>
                    y te enviaremos un nuevo enlace de activación si es necesario
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
import { VERIFY_ACCOUNT } from '~/graphql/user'
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import { ERROR_MESSAGES, type ActivationErrors, type ActivationError } from '~/types/registration'
import InputFloatLabel from '~/components/UI/InputFloatLabel.vue'
import MainButton from '~/components/UI/MainButton.vue'
import SpinLoader from '~/components/SpinLoader.vue'

const { executeQuery } = useGraphQL()

const route = useRoute()
const success = ref<null | boolean>(null)
const loading = ref<boolean>(true)
const errors = ref<string[]>([])
const errorSection = ref<HTMLElement | null>(null)

interface VerifyAccountResponse {
  verifyAccount: {
    success: boolean
    errors?: ActivationErrors
  }
}

const verifyAccount = async () => {
  const token = route.params.token
  try {
    const { verifyAccount: result } = await executeQuery<VerifyAccountResponse>(VERIFY_ACCOUNT, {
      token: token
    })
    loading.value = false
    success.value = result.success
    if (result.success) {
      success.value = true
    } else if (result.errors) {
      errors.value = handleErrors(result.errors)
      errorSection.value?.focus()
    }
  } catch (error) {
    console.log(error)
  }
}

// Methods
const handleErrors = (errors: ActivationErrors): string[] => {
  const errorMessages: string[] = []

  if (errors.nonFieldErrors) {
    Object.entries(errors.nonFieldErrors).forEach(([_, error]: [string, ActivationError]) => {
      errorMessages.push(ERROR_MESSAGES[error.code] || error.message || 'Error de validación')
    })
  }
  return errorMessages
}

// Lifecycle hooks
onMounted(async () => {
  await verifyAccount()
})

</script>

<style scoped>

</style>