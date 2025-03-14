import { LOGIN, LOGOUT, GRUPOS_USUARIOS, ME_QUERY, USER_IS_LOGGED } from '~/graphql/user'

export default function useAuth() {

  const store = useUserPermissionsStore()
  const { executeQuery, executeMutation } = useGraphQL()

  const login = async (credentials: {
    email: string | null;
    password: string | null
  }): Promise<{ success: boolean; errors?: any } | undefined>  => {
    try {

      const { loginAuthToken } = await executeMutation(LOGIN, credentials)
      if (loginAuthToken?.success) {
        const { me: userInfo } = await executeQuery(ME_QUERY) as {
          me: { firstName: string; lastName: string; avatar: string | null }
        }
        store.setUserSession( `${userInfo.firstName} ${userInfo.lastName}`, userInfo.avatar, true)
      }
      return { success: loginAuthToken.success, errors: loginAuthToken.errors }
    } catch (error) {
      // Handle login errors
      console.error('Login failed:', error)
    }
  }
  const isAuthenticated = async (): Promise<boolean> => {
    try {

      const {authenticated} = await executeQuery(USER_IS_LOGGED)
      return authenticated
    } catch (error) {
      console.error('Error checking authentication:', error)
      return false
    }
  }

  const logout = async () => {
    const { logoutUser:result } = await executeMutation(LOGOUT)
    if (result?.success) {
      store.clearUserSession()
    }
  }

  return {
    login,
    logout,
    isAuthenticated
  }
}