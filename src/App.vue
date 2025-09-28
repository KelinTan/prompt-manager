<template>
  <div id="app">
    <div class="app-layout">
      <!-- 现代化顶部导航 -->
      <header class="top-navbar">
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
            <el-button type="primary" class="create-btn" @click="$router.push('/prompts/create')">
              <el-icon><Plus /></el-icon>
              新建 Prompt
            </el-button>
          </div>
        </div>
      </header>
      
      <!-- 主要内容区域 -->
      <main class="main-content">
        <div class="content-container">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import config from '@/utils/config'

export default {
  name: 'App',
  setup() {
    const appTitle = computed(() => config.appTitle)
    
    return {
      appTitle
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

.create-btn {
  background: var(--primary-gradient);
  border: none;
  border-radius: var(--radius-md);
  padding: var(--spacing-sm) var(--spacing-md);
  font-weight: 600;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}

.create-btn:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  padding: var(--spacing-xl) 0;
}

.content-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
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