import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // 根据当前工作目录中的 `mode` 加载 .env 文件
  // 设置第三个参数为 '' 来加载所有环境变量，而不管是否有 `VITE_` 前缀。
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
        '@prompt': resolve(__dirname, 'src/modules/prompt'),
        '@common': resolve(__dirname, 'src/modules/common')
      }
    },
    server: {
      port: 3000,
      open: true
    },
    build: {
      // 确保构建输出适合静态部署
      outDir: 'dist',
      assetsDir: 'assets',
      // 生成相对路径，适合OSS等静态托管
      rollupOptions: {
        output: {
          // 分块策略，适合CDN缓存
          manualChunks: {
            vendor: ['vue', 'vue-router'],
            elementPlus: ['element-plus', '@element-plus/icons-vue']
          }
        }
      }
    },
    // 根据环境设置 base 路径
    // 本地开发: 相对路径
    // 测试/生产环境: OSS 部署路径
    base: (mode === 'production' || mode === 'beta') ? '/prompt-manager/' : './',
    define: {
      // 让环境变量在客户端代码中可用
      __APP_ENV__: JSON.stringify(env.APP_ENV),
    }
  }
})