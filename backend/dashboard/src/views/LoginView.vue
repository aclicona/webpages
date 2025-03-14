<template>
  <section class="relative grid grid-cols-2">
    <div class="min-h-screen bg-main-400 flex justify-center items-center">
      <div class="w-full lg:w-1/2 m-auto">
        <div class="lg:max-w-md">
          <div class="max-w-md mx-auto text-center">
            <h3 class="mb-12 text-3xl font-semibold font-heading text-main-900">
              DASHBOARD </h3>
            <form @submit.prevent="loginUser">
              <div class="relative flex flex-wrap mb-6">
                <input-float-label
                  class="w-full"
                  :required="true"
                  v-model="email"
                  tipo="email"
                >
                  Email
                </input-float-label>
              </div>
              <div class="relative flex flex-wrap mb-6">
                <input-float-label
                  class="w-full"
                  :required="true"
                  v-model="password"
                  tipo="password"
                >
                  Contraseña
                </input-float-label>
              </div>
              <button
                class="
                  w-full
                  inline-block
                  py-4
                  mb-4
                  text-2xl text-white
                  font-medium
                  leading-normal
                  bg-main-800
                  hover:bg-main-900
                  rounded
                  transition
                  duration-200
                  border-1 border-main-900
                "
              >
                Iniciar sesión
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="h-96 lg:h-auto lg:absolute top-0 right-0 bottom-0 lg:w-1/2">
    </div>
  </section>
</template>

<script setup>
import { inject, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import inputFloatLabel from '../components/UI/inputFloatLabel.vue'

const LoginPlugin = inject('loginPlugin')

const email = ref(null)
const password = ref(null)
const router = useRouter()
const route = useRoute()

async function loginUser() {
  const credentials = { email: email.value, password: password.value }
  const login = await LoginPlugin.login(credentials)
  if (login) {
    const redirectUrl = route.query.next || '/'
    router.push({ path: redirectUrl })
  }
}
</script>

