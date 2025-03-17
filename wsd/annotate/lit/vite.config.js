import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

const __dirname = dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
  build: {
    lib: {
      entry: resolve(__dirname, 'pop.js'),
      name: 'LinPop',
      fileName: 'linpop',
    },
  },
  server: {
    watch: {
      usePolling: true
    }
  }
})
