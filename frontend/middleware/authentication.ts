import {defineNuxtRouteMiddleware} from '#app'

/**
 * Middleware de autenticación para Nuxt
 * Controla el acceso a las rutas basado en el estado de autenticación del usuario
 * Se ejecuta en el lado del servidor para manejar la navegación segura
 */
export default defineNuxtRouteMiddleware(async (to) => {

  try {
    /**
     * Verifica si la ruta actual está en la lista de rutas públicas
     * @returns {boolean} - true si la ruta es pública, false en caso contrario
     */
    const routes_check = (): boolean => {
      const publicOnlyRoutes = ['/login', '/account/register', '/account/forgot-password', '/account/password-reset']
      return publicOnlyRoutes.includes(to.path)
    }

    // Obtiene el estado de autenticación del usuario
    const { isAuthenticated } = useAuth()
    const isLogged = await isAuthenticated()

    // Si el usuario está autenticado
    if (isLogged) {
      // Redirige a la página principal si intenta acceder a rutas públicas
      if (routes_check()) {
        return navigateTo('/', { replace: true })
      }
      return
    }

    // Permite acceso a rutas públicas para usuarios no autenticados
    if (routes_check()) {
      return
    }

    // Redirige a login si intenta acceder a rutas protegidas
    return navigateTo('/login?redirect=' + to.fullPath, { replace: true })

  } catch (error) {
    // Manejo de errores de autenticación
    console.error('Authentication error:', error)
    return navigateTo('/login?redirect=' + to.fullPath, { replace: true })
  }
})