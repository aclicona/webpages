import { ApolloClient, InMemoryCache } from '@apollo/client/core'

const endpoint = import.meta.env.VITE_API_URL || '/graphql'

const apolloClient = new ApolloClient({
  uri: endpoint, // Replace with your GraphQL endpoint
  cache: new InMemoryCache(),
  connectToDevTools: true, // Optional: For development
  headers: {
    // Include cookies in the request headers
    'Cookie': document.cookie
  }
});

export default {
  install(app) {
    app.provide({
      apolloClient,
    });
  },
};
const executeQuery = async (query,  variables = {}, client= apolloClient) => {
 try {
   const { data } = await client.query({
     query,
     variables,
     fetchPolicy: 'network-only' // Skip cache
   });

   // Get first property from data object
   return Object.values(data)[0];
 } catch (error) {
   console.error('Query error:', error);
   throw error;
 }
};

const executeMutation = async (mutation,  variables = {}, client= apolloClient) => {
 try {
   const { data } = await client.mutate({
     mutation,
     variables,
     fetchPolicy: 'network-only' // Skip cache
   });

   // Get first property from data object
   return Object.values(data)[0];
 } catch (error) {
   console.error('Query error:', error);
   throw error;
 }
};
export {apolloClient, executeQuery, executeMutation};