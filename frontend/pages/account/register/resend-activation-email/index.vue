<template>
  <!-- Sección principal con diseño responsive de 1 columna en móvil y 2 en desktop -->
  <section class="grid grid-cols-1 md:grid-cols-2">
    <div class="text-center py-10 px-4 md:px-24" v-if="!resendActivationOk">
      <!-- Formulario de reenvío de activación -->
      <form @submit.prevent="resendActivationEmail">
        <h3 class="mb-12 text-3xl font-semibold font-heading text-main-600">Activación de
          cuenta</h3>
        <p class="mb-6 text-justify">Ingresa y confirma tu correo. Si existe una cuenta sin activar asociada a
          este, te
          enviaremos un mensaje para que puedas activar tu cuenta</p>
        <div class="relative">
          <input-float-label v-model="email" :required="true" key="email"
                             tipo="email">Email
          </input-float-label>
        </div>
        <div class="relative">
          <input-float-label v-model="email2" :required="true" key="email"
                             tipo="email">Confirma tu correo
          </input-float-label>
        </div>
        <div ref="errorSection">
          <div class="text-red-600 text-md pb-4 text-left" v-for="error in errors">{{ error }}
          </div>
        </div>
        <main-button class="w-8/12">
          <div class="py-2">
            Solicitar activación
          </div>
        </main-button>
      </form>
    </div>
    <!-- Mensaje de éxito después del reenvío -->
    <div class="py-10 px-4 md:px-24" v-else>
      <!-- ... mensaje de confirmación ... -->
      <h4 class="text-center py-3 text-2xl text-main-600 md:pt-28">¡Ya casi está todo listo!</h4>
      <p>hemos enviado un mensaje de confirmación para activar tu cuenta al correo {{ email }}</p>
    </div>
    <div class="h-96 lg:h-auto lg:absolute top-0 right-0 bottom-0 lg:w-1/2 bg-no-repeat bg-contain bg-center">

    </div>
  </section>
</template>

<script setup lang="ts">
// Importaciones necesarias
import { ref } from 'vue'
import InputFloatLabel from '~/components/UI/InputFloatLabel.vue'
import MainButton from '~/components/UI/MainButton.vue'
import { RESEND_ACTIVATION_EMAIL } from '~/graphql/user'

definePageMeta({
  middleware: ['authentication']
})

// Inicialización de utilidades
const { executeMutation } = useGraphQL()

// Referencias reactivas
const resendActivationOk = ref(false)
const email = ref<string | null>(null)
const email2 = ref<string | null>(null)
const errors = ref<string[]>([])
const errorSection = ref<HTMLElement | null>(null)


const resendActivationEmail = async () => {
  /**
   * Maneja el reenvío del email de activación
   * Valida los emails y procesa la respuesta del servidor
   */

  if (email.value !== email2.value) {
    return
  }
  const variables = { email: email.value }
  const { resultResendEmail } = await executeMutation(RESEND_ACTIVATION_EMAIL, variables)
  if (resultResendEmail.success) {
    resendActivationOk.value = true
  } else if (!resultResendEmail.success) {
    if (resultResendEmail.errors?.nonFieldErrors) {
      for (const error of resultResendEmail.errors.nonFieldErrors) {
        if (error.code === 'email_fail') {
          errors.value.push('Lo sentimos, ha fallado el envío del correo. Intenta de nuevo')
        }
      }
    }
    if (resultResendEmail.errors?.email) {
      for (const error of resultResendEmail.errors.email) {
        if (error.code === 'already_verified') {
          errors.value.push('La cuenta ya está activa')
        } else if (error.code === 'invalid') {
          errors.value.push('El correo ingresado no es válido')
        }
      }
    }
    // Enfoca la sección de errores para mejor UX
    errorSection.value?.focus()
  }
}

</script>
