import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/modules/common/stores/auth'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'

// 创建 axios 实例
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加认证头
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    const token = authStore.getToken()
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理认证错误
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const authStore = useAuthStore()
    
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // 未授权，清除认证信息并跳转到登录页
          authStore.clearAuth()
          ElMessage.error('登录已过期，请重新登录')
          
          // 避免在登录页面重复跳转
          if (!window.location.hash.includes('#/login')) {
            // Preserve the current pathname (deployment base) when redirecting to the hash route.
            // e.g. if app is served from https://.../prompt-manager/, this will redirect to
            // https://.../prompt-manager/#/login instead of https://.../#/login
            const basePath = window.location.pathname || '/'
            window.location.href = `${window.location.origin}${basePath}#/login`
          }
          break
          
        case 403:
          ElMessage.error('没有权限访问此资源')
          break
          
        case 404:
          ElMessage.error('请求的资源不存在')
          break
          
        case 500:
          ElMessage.error('服务器内部错误')
          break
          
        default:
          ElMessage.error(data?.message || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络连接失败，请检查网络设置')
    } else {
      ElMessage.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

export default api