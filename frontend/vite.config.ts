/**
 * 文件注释：frontend/vite.config.ts
 *
 * 职责：定义 TypeScript 版本 Vite 配置，协调 Vue/React 插件与开发代理参数。
 * 边界：仅承担工程构建配置，不处理页面业务逻辑。
 */

import { fileURLToPath, URL } from 'node:url'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vueJsx(),
        vueDevTools(),
        react(),

    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        },
    },
    server: {
        host: '0.0.0.0', // 允许局域网其他设备访问
        proxy: {
            '/api': {
                target: 'http://165.154.4.83:8080', // 后端地址，按需修改
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, '')
            }
        }
    }
})
