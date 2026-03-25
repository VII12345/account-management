import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3001, // 固定端口
    cors: true,  // 允许跨域
    proxy: {
      '/account-api': {
        target: 'http://hk.xzzzs.icu:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/account-api/, '')
      }
    }
  }
})