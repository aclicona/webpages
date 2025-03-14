import { ref } from 'vue'
import { useNuxtApp } from '#app'
import { ApolloClient, ApolloError } from '@apollo/client/core'
import type { DocumentNode, NormalizedCacheObject } from '@apollo/client/core'

// Interfaces mejoradas
interface ApolloResponse<T = any> {
  data: T
}

interface QueryOptions {
  fetchPolicy?: 'no-cache' | 'network-only'
  errorPolicy?: 'none' | 'ignore' | 'all'
}

export function useGraphQL() {
  const nuxtApp = useNuxtApp()
  const apollo = nuxtApp.$apollo as ApolloClient<NormalizedCacheObject>

  // Verificar que el cliente Apollo esté disponible
  if (!apollo) {
    throw new Error('Apollo client not found in Nuxt app context')
  }

  const data = ref<any>(null)
  const loading = ref(false)
  const error = ref<ApolloError | null>(null)

  // Función para realizar una consulta GraphQL con tipos genéricos
  async function executeQuery<T = any>(
    query: DocumentNode,
    variables?: Record<string, any>,
    options: QueryOptions = {}
  ): Promise<T> {
    loading.value = true
    error.value = null
    data.value = null

    try {
      const response = await apollo.query<ApolloResponse<T>>({
        query,
        variables,
        fetchPolicy: options.fetchPolicy || 'no-cache',
        errorPolicy: options.errorPolicy || 'all'
      })

      data.value = response.data
      return response.data as T
    } catch (err) {
      const apolloError = err as ApolloError
      error.value = apolloError
      console.error('GraphQL Query Error:', {
        message: apolloError.message,
        networkError: apolloError.networkError,
        graphQLErrors: apolloError.graphQLErrors
      })
      throw apolloError
    } finally {
      loading.value = false
    }
  }

  // Función para realizar una mutación GraphQL con tipos genéricos
  async function executeMutation<T = any>(
    mutation: DocumentNode,
    variables?: Record<string, any>,
    options: QueryOptions = {}
  ): Promise<T> {
    loading.value = true
    error.value = null
    data.value = null

    try {
      const response = await apollo.mutate<ApolloResponse<T>>({
        mutation,
        variables,
        fetchPolicy: (options.fetchPolicy as 'no-cache' | 'network-only') || 'no-cache',
        errorPolicy: options.errorPolicy || 'all'
      })

      if (!response.data) {
        throw new Error('No data returned from mutation')
      }

      data.value = response.data
      return response.data as T
    } catch (err) {
      const apolloError = err as ApolloError
      error.value = apolloError
      console.error('GraphQL Mutation Error:', {
        message: apolloError.message,
        networkError: apolloError.networkError,
        graphQLErrors: apolloError.graphQLErrors
      })
      throw apolloError
    } finally {
      loading.value = false
    }
  }

  // Función para limpiar el estado
  function reset(): void {
    data.value = null
    loading.value = false
    error.value = null
  }

  return {
    data,
    loading,
    error,
    executeQuery,
    executeMutation,
    reset
  }
}