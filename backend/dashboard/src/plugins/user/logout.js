import { LOGOUT } from '@/graph/user'
import { useUserPermissionsStore } from '@/stores/userSession'
import { executeMutation } from '@/plugins/apollo.js'

const logoutUser = async () => {
  try {
    const { logoutUser: { logout: result } } = await executeMutation(LOGOUT)

    if (result) {
      const userPermissionsStore = useUserPermissionsStore()
      const { clearUserSession } = userPermissionsStore
      clearUserSession()
    }
    return result
  } catch (e) {
    console.error(e)
  }
}

export default {
  install: function(app) {
    const userLogout = () => {
      return logoutUser()
    }
    app.provide('userLogout', userLogout)
  }
}
