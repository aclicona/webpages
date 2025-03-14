import {defineStore} from 'pinia'
import {ref} from 'vue'

export const useUserPermissionsStore = defineStore('userPermissions', () => {
    // Define state using Composition API's ref
    const userSession = ref({
        groups: [],
        permissions: [],
        userName: null,
        userAvatar: null
    });

    // Actions
    const setUserSession = (groups, permissions, userName, userAvatar) => {
        userSession.value.groups = groups;
        userSession.value.permissions = permissions;
        userSession.value.userName = userName;
        userSession.value.userAvatar = userAvatar;

        localStorage.setItem('user-permissions', JSON.stringify(userSession.value));
    };
    const loadUserSession = () => {
        const storedData = localStorage.getItem('user-permissions');
        if (storedData) {
            userSession.value = JSON.parse(storedData);
        }
    };
    const clearUserSession = () => {
        userSession.value.groups = [];
        userSession.value.permissions = [];
        userSession.value.userName = null;
        userSession.value.userAvatar = null;
    };

   loadUserSession()

    // Return the state and actions for use in components
    return {
        userSession,
        setUserSession,
        clearUserSession,
        loadUserSession
    };
});
