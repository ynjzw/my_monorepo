import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue' // 1. 引入插件
import { resolve } from 'path'

export default defineConfig({
  plugins: [
    vue() // 2. 将插件添加到数组中
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src')
    }
  },
  server:{
    proxy:{
      '/api':{
        target:'http://127.0.0.1:8000',
        changeOrigin:true,
        rewrite:(path)=> path.replace(/^\/api/,'')
      }
    }
  }
})