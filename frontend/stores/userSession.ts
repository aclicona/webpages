import {defineStore} from 'pinia'
import {ref} from 'vue'
import type {UserSession} from '~/types/user'

export const useUserPermissionsStore = defineStore('userPermissions', () => {
        // State
        const userSession = ref<UserSession>({
            userName: null,
            userAvatar: null,
            isLoggedIn: false
        })

        // Actions
        const setUserSession = (
            userName: string | null,
            userAvatar: string | null,
            isLoggedIn: boolean
        ): void => {
            userSession.value = {
                userName,
                userAvatar,
                isLoggedIn
            }
        }

        const clearUserSession = (): void => {
            userSession.value = {
                userName: null,
                userAvatar: null,
                isLoggedIn: false
            }
        }

        return {
            // State
            userSession,

            // Actions
            setUserSession,
            clearUserSession
        }
    },
    {
        persist: {
            storage: piniaPluginPersistedstate.localStorage(),
        }
    })

