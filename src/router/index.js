import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '@/modules/common/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/modules/common/views/Login.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/prompts'
  },

  // ========== Prompt 模块 ==========
  {
    path: '/prompts',
    name: 'PromptList',
    component: () => import('@/modules/prompt/views/PromptList.vue'),
    meta: { title: 'Prompt 列表', requiresAuth: true, module: 'prompt' }
  },
  {
    path: '/prompts/create',
    name: 'PromptCreate',
    component: () => import('@/modules/prompt/views/PromptEdit.vue'),
    meta: { title: '创建 Prompt', requiresAuth: true, module: 'prompt' }
  },
  {
    path: '/prompts/:id/edit',
    name: 'PromptEdit',
    component: () => import('@/modules/prompt/views/PromptEdit.vue'),
    meta: { title: '编辑 Prompt', requiresAuth: true, module: 'prompt' }
  },
  {
    path: '/prompts/:id/history',
    name: 'PromptHistory',
    component: () => import('@/modules/prompt/views/PromptHistory.vue'),
    meta: { title: 'Prompt 历史版本', requiresAuth: true, module: 'prompt' }
  },
  {
    path: '/prompts/:id/versions/:version',
    name: 'PromptVersion',
    component: () => import('@/modules/prompt/views/PromptVersion.vue'),
    meta: { title: 'Prompt 版本详情', requiresAuth: true, module: 'prompt' }
  },

  // ========== Task 模块 ==========
  {
    path: '/tasks',
    name: 'TaskList',
    component: () => import('@/modules/task/views/TaskList.vue'),
    meta: { title: '任务列表', requiresAuth: true, module: 'task' }
  },

  // ========== AI 助手 ==========
  {
    path: '/ai-assistant',
    name: 'AIAssistant',
    component: () => import('@/modules/common/views/AIAssistant.vue'),
    meta: { title: 'AI助手', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - AIGC Admin`
  }

  // 检查是否需要认证
  if (to.meta.requiresAuth !== false) {
    // 默认需要认证
    if (!authStore.isAuthenticated()) {
      // 未认证，跳转到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      return
    }
  } else {
    // 不需要认证的页面（如登录页）
    if (authStore.isAuthenticated() && to.path === '/login') {
      // 已认证用户访问登录页，跳转到首页
      next('/prompts')
      return
    }
  }

  next()
})

export default router
