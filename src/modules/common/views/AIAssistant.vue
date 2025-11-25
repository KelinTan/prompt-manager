<template>
  <div class="ai-assistant">
    <div class="page-header">
      <h1>AI助手</h1>
      <p class="page-description">测试prompt效果，支持多种模型和参数配置</p>
    </div>

    <div class="assistant-container">
      <PromptDebugger
        ref="debuggerRef"
        :model="''"
        :ai-provider="''"
        :template="''"
        :auto-start="false"
        @debug-complete="handleDebugComplete"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import PromptDebugger from '@/modules/prompt/components/PromptDebugger.vue'

export default {
  name: 'AIAssistant',
  components: {
    PromptDebugger
  },
  setup() {
    const debuggerRef = ref()

    const handleDebugComplete = () => {
      console.log('AI对话完成')
    }

    // 检查是否有从PromptEdit传递过来的配置
    const loadConfigFromStorage = () => {
      try {
        const storedConfig = localStorage.getItem('ai-assistant-config')
        if (storedConfig) {
          const config = JSON.parse(storedConfig)

          // 检查配置是否是最近的（5分钟内）
          const now = Date.now()
          if (now - config.timestamp < 5 * 60 * 1000) {
            // 将配置传递给PromptDebugger组件
            if (debuggerRef.value) {
              debuggerRef.value.loadExternalConfig(config)
            }

            // 清除存储的配置
            localStorage.removeItem('ai-assistant-config')

            console.log('已加载外部配置:', config)
          }
        }
      } catch (error) {
        console.error('加载外部配置失败:', error)
      }
    }

    // 组件挂载后尝试加载配置
    onMounted(() => {
      // 延迟一点加载，确保子组件已经就绪
      setTimeout(loadConfigFromStorage, 100)
    })

    return {
      debuggerRef,
      handleDebugComplete,
      loadConfigFromStorage
    }
  }
}
</script>

<style scoped>
.ai-assistant {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
  text-align: center;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.page-description {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

.assistant-container {
  background: #ffffff;
  border-radius: 12px;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 24px;
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .page-header h1 {
    color: #f9fafb;
  }

  .page-description {
    color: #d1d5db;
  }

  .assistant-container {
    background: #374151;
  }
}
</style>
