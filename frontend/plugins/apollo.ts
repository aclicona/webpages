import {defineNuxtPlugin} from '#app'
import {ApolloClient, InMemoryCache, HttpLink, ApolloLink} from '@apollo/client/core'

// Función helper para parsear cookies
const parseCookies = (cookieString: string): { [key: string]: string } => {
    return cookieString
        .split(';')
        .map(cookie => cookie.trim())
        .reduce((acc, cookie) => {
            const [key, value] = cookie.split('=')
            if (key && value) {
                acc[key.trim()] = value.trim()
            }
            return acc
        }, {} as { [key: string]: string })
}

export default defineNuxtPlugin((nuxtApp) => {
    const accessTokenCookieName = (process.env.accessTokenCookieName as string) || 'accessToken'
    const refreshTokenCookieName = (process.env.refreshTokenCookieName as string) || 'refreshToken'
    const httpLink = new HttpLink({
        uri: (process.env.BACKEND_API_URL as string) || 'http://localhost:8000/graphql',
        credentials: 'include'
    })

    const authLink = new ApolloLink((operation, forward) => {
        let token: string | null = null
        let refreshToken: string | null = null

        if (process.server) {
            // En el servidor, accedemos a las cookies a través del evento del servidor
            const event = nuxtApp.ssrContext?.event
            const cookieHeader = event?.req.headers.cookie

            if (cookieHeader) {
                const cookies = parseCookies(cookieHeader)
                token = cookies[accessTokenCookieName]
                refreshToken = cookies[refreshTokenCookieName]
            }


            if (token) {
                operation.setContext({
                    headers: {
                        Authorization: `JWT ${token}`,
                        refreshToken: refreshToken
                    }
                })
            }
        }

        return forward(operation)
    })

    const apolloClient = new ApolloClient({
        link: authLink.concat(httpLink),
        cache: new InMemoryCache(),
        // Configuraciones adicionales para manejar errores
        defaultOptions: {
            watchQuery: {
                errorPolicy: 'all'
            },
            query: {
                errorPolicy: 'all'
            },
            mutate: {
                errorPolicy: 'all'
            }
        }
    })

    return {
        provide: {
            apollo: apolloClient
        }
    }
})