import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// 前端固定使用本通道端口 5172，代理到后端 8082
export default defineConfig({
  plugins: [vue()],
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
  server: {
    host: '127.0.0.1',
    port: 5172,
    proxy: {
      '/api': { target: 'http://127.0.0.1:8082', changeOrigin: true },
      '/uploads': { target: 'http://127.0.0.1:8082', changeOrigin: true }
    }
  }
})
