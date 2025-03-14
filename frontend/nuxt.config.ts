const pathtostatic = process.env.CDN_STATIC_HOST || ''
const serverPort: number = parseInt(process.env.PORT as string, 10) || 3000
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  devServer: {
    port: serverPort
  },

  // Server configuration
  nitro: {
    preset: 'node-server',
    compressPublicAssets: true,
    minify: true,
    storage: {
      data: {
        driver: 'fs',
        base: './.data/storage'
      }
    },
    devProxy: {
      '/graphql': {
        target: process.env.BACKEND_API_URL || 'http://localhost:8000/graphql',
        changeOrigin: true
      }
    }
  },

  // App configuration
  app: {
    head: {
      titleTemplate: `%s - ${process.env.SITE_NAME}`,
      title: process.env.SITE_NAME || 'Nombre del sitio',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: process.env.SITE_DESCRIPTION || '' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: `${pathtostatic}/favicon.png` },
        { rel: 'shortcut icon', type: 'image/png', href: `${pathtostatic}/favicon.png` },
        { rel: 'apple-touch-icon', type: 'image/png', href: `${pathtostatic}/favicon.png` }
      ]
    }
  },
  // Configuración SSR
  ssr: true,
  // Funcionalidades experimentales
  experimental: {
    crossOriginPrefetch: true,
    treeshakeClientOnly: true,
    payloadExtraction: true
  },

  // Configuración de TypeScript
  typescript: {
    strict: true,
    typeCheck: true,
    shim: false
  },

  // CSS configuration
  css: ['~/assets/css/main.css'],

  // Modules configuration
  modules: [
    '@pinia/nuxt',
    '@nuxtjs/google-fonts',
    'pinia-plugin-persistedstate/nuxt'
  ],

  // Google Fonts configuration
  googleFonts: {
    families: {
      Montserrat: [200, 400, 600, 800, 900],
      'Gentium+Book+Plus': [400, 700]
    },
    display: 'swap',
    preconnect: true,
    prefetch: true,
    preload: true
  },

  // Runtime configuration
  runtimeConfig: {
    public: {
      siteName: process.env.SITE_NAME,
      siteDescription: process.env.SITE_DESCRIPTION,
      googleMapsApiKey: process.env.GOOGLE_MAPS_API_KEY,
      graphqlEndpoint: process.env.BACKEND_API_URL || 'http://localhost:8000/graphql'
    }
  },

  // Build configuration
  build: {
    transpile: ['@fawmi/vue-google-maps']
  },
  // Vite configuration
  vite: {
    build: {
      rollupOptions: {
        output: {
          assetFileNames: (assetInfo) => {
            if (assetInfo.name) {
              if (assetInfo.name.endsWith('.css')) return 'css/[name].[hash].[ext]'
              if (/\.(png|jpe?g|gif|svg|webp|ico)$/.test(assetInfo.name)) return 'img/[name].[hash].[ext]'
              if (/\.(woff2?|eot|ttf|otf)$/.test(assetInfo.name)) return 'fonts/[name].[hash].[ext]'
              if (/\.(mp4|webm|ogg|mp3|wav|flac|aac)$/.test(assetInfo.name)) return 'media/[name].[hash].[ext]'
            }
            return '[name].[hash].[ext]'
          }
        }
      }
    },
    plugins: [tailwindcss()],
    optimizeDeps: {
      include: ['vue', 'pinia', '@apollo/client/core']
    }
  },

  compatibilityDate: '2025-02-21'
})