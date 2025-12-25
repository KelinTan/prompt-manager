import api from '@/modules/common/api/request'
import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'

export const authApi = {
  // 登录 - 使用独立的 axios 实例，避免拦截器循环
  async login(credentials) {
    const response = await axios.post(
      `${BASE_URL}/login`,
      {
        username: credentials.username,
        password: credentials.password
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )

    // 适配新的响应格式
    const data = response.data
    return {
      token: data.meta?.accessToken,
      user: {
        username: credentials.username // 从请求参数中获取用户名
      }
    }
  }

  // 注意：登出功能由前端直接处理，无需调用后端接口
}
