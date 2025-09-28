<template>
  <div id="app">
    <div class="app-layout">
      <!-- 现代化顶部导航 - 登录页面时隐藏 -->
      <header v-if="!isLoginPage" class="top-navbar">
        <div class="navbar-container">
          <div class="navbar-brand">
            <div class="brand-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
              </svg>
            </div>
            <h1 class="brand-title">{{ appTitle }}</h1>
          </div>
          
          <div class="navbar-actions">
            <div class="user-section">
              <el-dropdown @command="handleUserCommand" trigger="click">
                <div class="user-info">
                  <el-avatar :size="32" class="user-avatar">
                    <el-icon><User /></el-icon>
                  </el-avatar>
                  <span class="username">{{ authStore.user?.username || '用户' }}</span>
                  <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
                </div>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="logout">
                      <el-icon><SwitchButton /></el-icon>
                      退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </div>
      </header>
      
      <!-- 主要内容区域 -->
      <main class="main-content" :class="{ 'login-layout': isLoginPage }">
        <div class="content-container" :class="{ 'login-container': isLoginPage }">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { config } from '@/utils/config'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'App',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    const appTitle = computed(() => config.appTitle)
    
    // 检查是否为登录页面
    const isLoginPage = computed(() => route.path === '/login')
    
    // 用户操作处理
    const handleUserCommand = async (command) => {
      if (command === 'logout') {
        try {
          await ElMessageBox.confirm(
            '确定要退出登录吗？',
            '确认退出',
            {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }
          )
          
          // 清除认证信息
          authStore.clearAuth()
          ElMessage.success('退出登录成功')
          
          // 跳转到登录页
          router.push('/login')
        } catch (error) {
          // 用户取消操作
        }
      }
    }
    
    return {
      appTitle,
      isLoginPage,
      authStore,
      handleUserCommand
    }
  }
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  background: var(--bg-secondary);
}

.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 现代化顶部导航栏 */
.top-navbar {
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.brand-icon {
  width: 32px;
  height: 32px;
  background: var(--primary-gradient);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.brand-icon svg {
  width: 18px;
  height: 18px;
}

.brand-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.025em;
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
  font-size: 14px;
}

.nav-link:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.nav-link.active {
  background: var(--primary-color);
  color: white;
}

.navbar-actions {
  display: flex;
  align-items: center;
}

/* 顶部导航用户信息 */
.user-section {
  flex-shrink: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.user-info:hover {
  background: rgba(99, 102, 241, 0.2);
  border-color: var(--primary-color);
  transform: translateY(-1px);
}

.user-avatar {
  background: var(--primary-gradient);
  color: white;
  flex-shrink: 0;
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
}

.dropdown-icon {
  font-size: 12px;
  color: var(--text-secondary);
  transition: transform 0.2s ease;
}

.user-info:hover .dropdown-icon {
  transform: rotate(180deg);
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  padding: var(--spacing-xl) 0;
}

.main-content.login-layout {
  padding: 0;
  min-height: 100vh;
}

.content-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
}

.content-container.login-container {
  max-width: none;
  padding: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .navbar-container {
    padding: 0 var(--spacing-md);
  }
  
  .navbar-nav {
    display: none;
  }
  
  .brand-title {
    font-size: 18px;
  }
  
  .content-container {
    padding: 0 var(--spacing-md);
  }
  
  .main-content {
    padding: var(--spacing-lg) 0;
  }
}

@media (max-width: 480px) {
  .navbar-container {
    height: 56px;
    padding: 0 var(--spacing-sm);
  }
  
  .navbar-actions .create-btn span {
    display: none;
  }
  
  .content-container {
    padding: 0 var(--spacing-sm);
  }
}
</style>