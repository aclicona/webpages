import { GET_GRUPOS_USUARIO, LOGIN, ME_USER } from '@/graph/user'
import { useUserPermissionsStore } from '@/stores/userSession'
import { executeMutation, executeQuery } from '@/plugins/apollo.js'

const loginUser = async (credentials) => {
  try {
    const loginAuthToken = await executeMutation(LOGIN, credentials)

    if (loginAuthToken.success && loginAuthToken.user.isActive && loginAuthToken.user.isStaff) {
      // store the user groups in the Pinia store
      const userPermissionsStore = useUserPermissionsStore()
      const { setUserSession } = userPermissionsStore
      const grupos = await executeQuery(GET_GRUPOS_USUARIO)
      const userInfo = await executeQuery(ME_USER)
      setUserSession(grupos, [], `${userInfo.firstName} ${userInfo.lastName}`, userInfo.avatar)
      return true
    }
  } catch (e) {
    console.error('Error:', e)
  }


}
const userIsLoggedIn = async () => {
  try {
    const { me } = await executeQuery(ME_USER)
    return !!me
  } catch (e) {
    console.error(e)
    return false
  }
}
const loginPlugin = {
  install(app) {
    app.userLogin = loginUser
    app.config.globalProperties.$userLogin = loginUser
    app.userIsLoggedIn = userIsLoggedIn
    app.config.globalProperties.$userIsLoggedIn = userIsLoggedIn
  }
}

export default {
  install: async function(app) {
    const loginPlugin = {
      async login(option) {
        return await loginUser(option)
      },
      isLogged() {
        return userIsLoggedIn()
      }
    }
    app.provide('loginPlugin', loginPlugin)
  }
}

export { loginPlugin, userIsLoggedIn }