<template>
    <section>
        <section class="relative pt-16 pb-36 bg-gradient-gray2 overflow-hidden">
            <img class="absolute top-0 transform left-1/2 -translate-x-1/2" src="~assets/images/radial2.svg" alt=""/>
            <div class="relative z-10 container mx-auto px-4">
                <img class="mx-auto mb-20" src="~assets/images/gradia-name-black.svg" alt=""/>
                <div class="flex flex-wrap -m-6">
                    <form class="w-full p-6" @submit.prevent="handleRegister">
                        <div class="md:max-w-xl text-center mx-auto">
                            <h2 class="mb-4 font-heading font-bold text-gray-900 text-6xl sm:text-7xl">Ready to get
                                started?</h2>
                            <p class="mb-11 text-lg text-gray-500">Lorem ipsum dolor sit amet, consectetur adipis.</p>
                            <div class="flex flex-wrap max-w-md mx-auto -m-2">
                                <div class="w-full p-2">
                                    <input-float-label v-model="formData.name" :required="true"
                                                       tipo="text">Name
                                    </input-float-label>
                                </div>
                                <div class="w-full p-2">
                                    <input-float-label v-model="formData.email" :required="true"
                                                       tipo="email">Email
                                    </input-float-label>
                                </div>
                                <div class="w-full p-2">
                                    <input-float-label v-model="formData.password1" :required="true"
                                                       tipo="password">Password
                                    </input-float-label>
                                </div>
                                <div class="w-full p-2">
                                    <input-float-label v-model="formData.password2" :required="true"
                                                       tipo="password">Repeat Password
                                    </input-float-label>
                                </div>
                                <div ref="errorSection">
                                    <div class="text-red-600 text-md pb-4 text-left" v-for="error in errors">{{ error }}
                                    </div>
                                </div>
                                <div class="w-full p-2">
                                    <div class="group relative">
                                        <div
                                            class="absolute top-0 left-0 w-full h-full bg-gradient-blue opacity-0 group-hover:opacity-50 rounded-lg transition ease-out duration-300"></div>
                                        <MainButton>Sign up</MainButton>
                                    </div>
                                </div>
                            </div>
                            <div class="mt-2 text-justify text-gray-600" v-if="registerOk">
                                <h4 class="text-center font-medium py-3 text-2xl text-main-500">
                                    Your registration has been successful!
                                </h4>
                                <p>{{ formData.name }}, we have sent a confirmation message to activate your account to
                                    your email
                                    ({{ formData.email }})</p>
                                <div class="flex flex-wrap">
                                    <p>Didn't receive the message?
                                        <nuxt-link to="/account/register/resend-activation-email"
                                                   class="font-semibold mx-1 text-main-400 hover:text-main-500 ">
                                            Resend activation email.
                                        </nuxt-link>
                                    </p>
                                </div>
                                <p>Also check your spam folder or contact our customer service department.
                                </p>
                            </div>
                            <p class="text-base text-gray-600 mt-6">
                                <span>Already have an account? </span>
                                <nuxt-link class="text-main-400 hover:text-main-600 cursor-pointer" to="/login">Login now</nuxt-link>
                            </p>
                        </div>
                    </form>
                </div>
            </div>
        </section>
    </section>


</template>

<script setup lang="ts">
import {reactive, ref} from 'vue'
import {REGISTER_USER} from '~/graphql/user'
import InputFloatLabel from '~/components/UI/InputFloatLabel.vue'
import MainButton from '~/components/UI/MainButton.vue'
import {ERROR_MESSAGES, type RegistrationErrors, type ValidationError} from '~/types/registration'

definePageMeta({
    middleware: ['authentication']
})


const {executeMutation} = useGraphQL()
const {isValidEmail} = useValidateEmail()
// Reactive state
const registerOk = ref(false)
const errors = ref<string[]>([])
const errorSection = ref<HTMLElement | null>(null)

const formData = reactive({
    name: '',
    email: '',
    password1: '',
    password2: ''
})


// Methods

const validateForm = (): boolean => {
    errors.value = []

    if (!formData.email || !formData.name || !formData.password1 || !formData.password2) {
        errors.value.push('Todos los campos son requeridos')
        return false
    }

    if (!isValidEmail(formData.email)) {
        errors.value.push('Email inválido')
        return false
    }

    if (formData.password1 !== formData.password2) {
        errors.value.push('Las contraseñas no coinciden')
        return false
    }

    if (formData.password1.length < 8) {
        errors.value.push('La contraseña debe tener al menos 8 caracteres')
        return false
    }

    return true
}

const handleRegister = async () => {
    if (!validateForm()) {
        errorSection.value?.focus()
        return
    }
    try {
        const {registerUser} = await executeMutation(REGISTER_USER,
            {
                email: formData.email,
                password: formData.password1,
                firstName: formData.name
            })

        if (registerUser.success) {
            registerOk.value = true
            formData.email = ''
            formData.password1 = ''
            formData.password2 = ''
            formData.name = ''
        } else {
            errors.value.push(...handleRegistrationErrors(registerUser.errors))
            errorSection.value?.focus()
        }
    } catch (error) {
        console.error('Registration error:', error)
        errors.value.push('Error en el registro. Por favor, intenta nuevamente.')
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

<style scoped>

</style>