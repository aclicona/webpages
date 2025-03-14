import {useUserPermissionsStore} from '@/stores/userSession'
import {storeToRefs} from 'pinia';

const authorizedByGroup = (authLevels = [], permisos = []) => {
    if (authLevels) {
        for (let group of authLevels) {
            if (permisos.includes(group)) {
                return true
            }
        }
        return false
    }
    return false
}
const authorizedOption =  (option) => {
    const userPermissionsStore = useUserPermissionsStore();
    const {userSession} = storeToRefs(userPermissionsStore);
    const grupos = userSession.value.groups
    if (grupos !== undefined) {
        if (option.groups !== undefined && option.groups) {
            const authorized = authorizedByGroup(option.groups, grupos);
            return authorized || grupos.includes('Admin');
        }
        return true;
    }
    return false
};


export default {
    install: async function (app) {
        const userManager = {
            authorizedOption(option) {
                return authorizedOption(option)
            }
        }
        app.provide('userManager', userManager)
    }
}
