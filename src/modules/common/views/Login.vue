<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <div class="logo-icon">
            <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="16" cy="16" r="16" fill="url(#gradient)" />
              <rect x="7" y="9" width="18" height="12" rx="3" fill="white" opacity="0.95" />
              <rect x="10" y="12" width="8" height="1.5" rx="0.75" fill="#6366F1" />
              <rect x="10" y="15" width="12" height="1.5" rx="0.75" fill="#6366F1" opacity="0.7" />
              <rect x="10" y="18" width="6" height="1.5" rx="0.75" fill="#6366F1" opacity="0.5" />
              <polygon points="12,21 15,21 13.5,24" fill="white" opacity="0.95" />
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color: #6366f1" />
                  <stop offset="100%" style="stop-color: #8b5cf6" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1>AIGC Admin</h1>
        </div>
        <p class="login-subtitle">AI 内容生成管理平台</p>
      </div>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            class="login-input"
            :prefix-icon="User"
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            class="login-input"
            :prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            <span v-if="!loading">登录</span>
            <span v-else>登录中...</span>
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="login-footer">
      <p>&copy; 2025 AIGC Admin. All rights reserved.</p>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { authApi } from '@/modules/common/api/auth'
import { useAuthStore } from '@/modules/common/stores/auth'

export default {
  name: 'Login',
  components: {
    User,
    Lock
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const loginFormRef = ref()
    const loading = ref(false)

    // 表单数据
    const loginForm = reactive({
      username: import.meta.env.DEV ? 'kelin.tan' : '', // 开发环境预填用户名
      password: import.meta.env.DEV ? 'tanzhuchao' : '' // 开发环境预填密码
    })

    // 验证规则
    const loginRules = {
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少6位', trigger: 'blur' }
      ]
    }

    // 登录处理
    const handleLogin = async () => {
      try {
        await loginFormRef.value.validate()

        loading.value = true
        const response = await authApi.login(loginForm)

        // 检查是否获取到 token
        if (!response.token) {
          throw new Error('登录响应格式错误，未获取到访问令牌')
        }

        // 保存认证信息
        authStore.setToken(response.token)
        authStore.setUser(response.user || { username: loginForm.username })

        ElMessage.success({
          message: '登录成功',
          duration: 1500
        })

        // 跳转到首页
        const redirect = router.currentRoute.value.query.redirect || '/prompts'
        router.push(redirect)
      } catch (error) {
        console.error('登录错误:', error)

        // 处理不同类型的错误
        let errorMessage = '登录失败，请检查用户名和密码'

        if (error.response) {
          const status = error.response.status
          const data = error.response.data

          switch (status) {
            case 401:
              errorMessage = '用户名或密码错误'
              break
            case 403:
              errorMessage = '账户无权限登录，请联系管理员'
              break
            case 429:
              errorMessage = '登录次数过多，请稍后再试'
              break
            case 500:
              errorMessage = '服务器错误，请稍后再试'
              break
            default:
              errorMessage = data?.message || `登录失败 (${status})`
          }
        } else if (error.request) {
          errorMessage = '网络连接失败，请检查网络设置'
        } else {
          errorMessage = error.message || '登录失败'
        }

        ElMessage.error(errorMessage)
      } finally {
        loading.value = false
      }
    }

    return {
      loginFormRef,
      loginForm,
      loginRules,
      loading,
      handleLogin,
      User,
      Lock
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.logo-icon {
  width: 48px;
  height: 48px;
}

.logo h1 {
  font-size: 28px;
  font-weight: 800;
  color: #1f2937;
  margin: 0;
  letter-spacing: -0.025em;
}

.login-subtitle {
  color: #6b7280;
  font-size: 16px;
  margin: 0;
}

.login-form {
  margin-bottom: 24px;
}

.login-form .el-form-item {
  margin-bottom: 20px;
}

.login-form .el-form-item:last-child {
  margin-bottom: 0;
}

:deep(.login-input .el-input__wrapper) {
  border-radius: 12px;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  box-shadow: none;
  transition: all 0.2s ease;
}

:deep(.login-input .el-input__wrapper:hover) {
  border-color: #6366f1;
}

:deep(.login-input .el-input__wrapper.is-focus) {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

:deep(.login-input .el-input__inner) {
  border: none;
  background: transparent;
  box-shadow: none;
  font-size: 16px;
}

.login-button {
  width: 100%;
  height: 48px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  transition: all 0.2s ease;
}

.login-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

.login-footer {
  margin-top: 32px;
  text-align: center;
}

.login-footer p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  margin: 0;
}

@media (max-width: 480px) {
  .login-card {
    padding: 32px 24px;
    margin: 16px;
  }

  .logo h1 {
    font-size: 24px;
  }
}
</style>
