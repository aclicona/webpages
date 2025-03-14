// types/auth.d.ts
import { ApolloClient, NormalizedCacheObject } from '@apollo/client/core'

export interface User {
  id: string
  email: string
  // Add other user properties
}


declare module '#app' {
  interface NuxtApp {
    $apolloClient: ApolloClient<NormalizedCacheObject>
  }
}

// For Composables
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $apolloClient: ApolloClient<NormalizedCacheObject>
  }
}