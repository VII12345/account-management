/**
 * 文件注释：autostra/frontend/vite.config.js
 *
 * 职责：定义自动化前端项目的构建入口、开发服务器端口与 API 代理规则。
 * 边界：仅承担工程配置，不处理业务组件逻辑。
 */

import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  return {
    plugins: [react()],
    server: {
      port: 3001,
      cors: true,
      proxy: {
        '/api': {
          target: 'http://165.154.4.83',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    }
  }
})