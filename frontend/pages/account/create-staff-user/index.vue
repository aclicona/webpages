<template>
    <section class="px-8 md:px-24 2xl:px-72 text-neutral-600">
        <main-title head="Cuenta"
                    title-string="Creación de cuenta de usuario"/>
        <div class="grid grid-cols-1 md:grid-cols-2">
            <div class="py-10 px-4 md:px-24" v-if="!registerOk">
                <form @submit.prevent="createUser" class="grid grid-cols-1 w-full gap-4">
                    <p class="text-justify pb-4">
                        Por favor ingresa los datos del usuario a crear. Cuando se cree el usuario, se le enviará un
                        correo a este para que establezca su contraseña.
                    </p>
                    <input-float-label v-model="firstName" :required="true" key="firstName"
                                       tipo="text" class="mx-20">Nombre
                    </input-float-label>
                    <input-float-label v-model="lastName" :required="false" key="lastName"
                                       tipo="text" class="mx-20">Apellidos
                    </input-float-label>
                    <input-float-label v-model="email" :required="true" key="email"
                                       tipo="email" class="mx-20">Email
                    </input-float-label>
                    <div class="mx-20 flex flex-wrap">
                        <h1 class="w-full text-center text-main-500 pb-2">Grupos</h1>
                        <div class="flex items-center mb-2 mr-2" v-for="grupo in gruposUsuario">
                            <input :checked="grupo.add" class="accent-main-800 text-white h-6 w-6"
                                   :id="'grupo-' + grupo.name"
                                   type="checkbox"
                                   v-model="grupo.add"/>
                            <label class="text-xs pl-2" :for="'grupo-' + grupo.name">{{ grupo.name }}</label>
                        </div>
                    </div>

                    <div ref="errorSection">
                        <div class="text-red-600 text-md pb-4 text-left" v-for="error in errors">{{ error }}
                        </div>
                    </div>
                    <div class="flex justify-center">
                        <main-button class="w-1/2">
                            <div class="py-2">
                                Crear
                            </div>
                        </main-button>
                    </div>
                </form>
            </div>
            <div class="py-10 px-4 md:px-24" v-else>
                <h4 class="text-center py-3 text-xl font-bold text-main-500">¡La creación del usuario ha sido
                    exitosa</h4>
                <p>Hemos enviado un mensaje de confirmación para activar la cuenta al correo {{ email }}</p>
                <br>
                <div class="text-justify">
                    <p>Si el usuario no recibe el mensaje en los próximos 5 minutos, deberás comunicarte con el
                        administrador del sistema
                    </p>
                    <br>
                    <p>También verifica en el buzón de correo no deseado o comunícate con nuestra área de atención al
                        cliente.
                    </p>
                </div>
            </div>
            <div class="w-3/4">
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import InputFloatLabel from '@/components/UI/InputFloatLabel.vue'
import MainButton from '@/components/UI/MainButton.vue'
import {USER_STAFF_CREATION} from '@/graphql/user'
import MainTitle from '@/components/UI/MainTitle.vue'
import {reactive, ref} from 'vue'
import {ERROR_MESSAGES, type ForgotPasswordErrors, type ValidationError} from '~/types/forgotPassword'

definePageMeta({
    middleware: ['authentication']
})

const {executeMutation} = useGraphQL()
const {grupos: groupsList} = useGetGroups()

interface Group {
    name: string;
    add: boolean;
}


const registerOk = ref(false)
const email = ref<string | null>(null)
const firstName = ref<string | null>(null)
const lastName = ref<string | null>(null)
const gruposUsuario = reactive<Group[]>([])
const errors = ref<string[]>([])
const errorSection = ref<HTMLElement | null>(null)

const createUser = async () => {
    const variables = {
        email: email.value,
        firstName: firstName.value,
        lastName: lastName.value,
        groups: gruposUsuario
    }
    errors.value = []
    try {
        const {createStaffUser: result} = await executeMutation(USER_STAFF_CREATION, variables)
        registerOk.value = result.success
        if (result.errors) {
            errors.value = handleChangeErrors(result.errors)
            errorSection.value?.focus()
        }
    } catch (error) {
        console.log('Staff User Creation error:', error)
        errors.value.push('Error en la solicitud para crear el usuario. Por favor, intenta nuevamente.')
    }
}

const handleChangeErrors = (errors: ForgotPasswordErrors): string[] => {
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

const {data: groups} = await useAsyncData('groups',
    async () => {
        return await groupsList()
    })

if (groups.value) {
    for (const group of groups.value) {
        gruposUsuario.push({name: group, add: false})
    }
}
</script>
