// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  
  // Development server configuration
  server: {
    host: '0.0.0.0',
    port: 5173,
    // Configure CORS for Django integration
    cors: true,
    // Configure proxy for API requests
    proxy: {
      '/api': {
        target: 'http://localhost:8000/api',
        changeOrigin: true,
      },
      '/graphql': {
        target: 'http://localhost:8000/graphql',
        changeOrigin: true,
      }
    }
  },
  
  // Build configuration
  build: {
    // Output directory for production build
    outDir: 'dist',
    
    // Generate manifest.json for Django integration
    manifest: true,
    
    // Configure asset handling
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'src/main.js'),
      },
      output: {
        // Customize chunk filenames
        chunkFileNames: 'js/[name]-[hash].js',
        entryFileNames: 'js/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash][extname]',
      },
    },
  },
  
  // Resolve configuration
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
})