import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/prompts'
  },
  {
    path: '/prompts',
    name: 'PromptList',
    component: () => import('@/views/PromptList.vue'),
    meta: { title: 'Prompt 列表' }
  },
  {
    path: '/prompts/create',
    name: 'PromptCreate',
    component: () => import('@/views/PromptEdit.vue'),
    meta: { title: '创建 Prompt' }
  },
  {
    path: '/prompts/:id/edit',
    name: 'PromptEdit',
    component: () => import('@/views/PromptEdit.vue'),
    meta: { title: '编辑 Prompt' }
  },
  {
    path: '/prompts/:id/history',
    name: 'PromptHistory',
    component: () => import('@/views/PromptHistory.vue'),
    meta: { title: 'Prompt 历史版本' }
  },
  {
    path: '/prompts/:id/versions/:version',
    name: 'PromptVersion',
    component: () => import('@/views/PromptVersion.vue'),
    meta: { title: 'Prompt 版本详情' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - Prompt Manager`
  }
  next()
})

export default router