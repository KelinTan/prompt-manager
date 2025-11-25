import { reactive } from 'vue'

// 简单的状态管理，不使用 Pinia
const authState = reactive({
  token: localStorage.getItem('auth_token') || null,
  user: JSON.parse(localStorage.getItem('auth_user') || 'null'),
  isAuthenticated: false
})

// 初始化认证状态
authState.isAuthenticated = !!authState.token

export const useAuthStore = () => {
  // 设置 token
  const setToken = token => {
    authState.token = token
    authState.isAuthenticated = !!token
    if (token) {
      localStorage.setItem('auth_token', token)
    } else {
      localStorage.removeItem('auth_token')
    }
  }

  // 设置用户信息
  const setUser = user => {
    authState.user = user
    if (user) {
      localStorage.setItem('auth_user', JSON.stringify(user))
    } else {
      localStorage.removeItem('auth_user')
    }
  }

  // 清除认证信息
  const clearAuth = () => {
    setToken(null)
    setUser(null)
  }

  // 获取 token
  const getToken = () => {
    return authState.token
  }

  // 检查是否已认证
  const isAuthenticated = () => {
    return authState.isAuthenticated
  }

  return {
    // 状态
    ...authState,

    // 方法
    setToken,
    setUser,
    clearAuth,
    getToken,
    isAuthenticated
  }
}
