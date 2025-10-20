import api from '@/api/request'
import { useAuthStore } from '@/stores/auth'

export const promptApi = {
  // 获取prompt列表
  async getPrompts(params = {}) {
    const response = await api.get('/prompts', { params })
    return response.data
  },

  // 获取单个prompt详情
  async getPrompt(id) {
    const response = await api.get(`/prompts/${id}`)
    return response.data
  },

  // 创建prompt
  async createPrompt(data) {
    const response = await api.post('/prompts', data)
    return response.data
  },

  // 更新prompt
  async updatePrompt(id, data) {
    const response = await api.put(`/prompts/${id}`, data)
    return response.data
  },

  // 删除prompt
  async deletePrompt(id) {
    const response = await api.delete(`/prompts/${id}`)
    return response.data
  },

  // 发布prompt（版本号+1）
  async publishPrompt(id) {
    const response = await api.post(`/prompts/${id}/publish`)
    return response.data
  },

  // 启用prompt
  async enablePrompt(id) {
    const response = await api.post(`/prompts/${id}/enable`)
    return response.data
  },

  // 禁用prompt
  async disablePrompt(id) {
    const response = await api.post(`/prompts/${id}/disable`)
    return response.data
  },

  // 获取prompt历史版本
  async getPromptHistory(id, params = {}) {
    const response = await api.get(`/prompts/${id}/history`, { params })
    return response.data
  },

  // 获取特定版本的prompt
  async getPromptVersion(id, version) {
    const response = await api.get(`/prompts/${id}/versions/${version}`)
    return response.data
  },

  // 回滚到指定版本
  async rollbackPrompt(id, data) {
    const response = await api.post(`/prompts/${id}/rollback`, data)
    return response.data
  },

  // 调试prompt - 流式接口
  async debugPromptStream(data, onChunk) {
    const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'
    const url = `${BASE_URL}/prompts/chat/stream`
    
    // 使用 auth store 获取token，保持与其他API调用一致
    const authStore = useAuthStore()
    const token = authStore.getToken() || ''
    
    return new Promise((resolve, reject) => {
      // 由于 EventSource 不支持 POST，我们使用 fetch 来处理流式响应
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'Cache-Control': 'no-cache',
          'Accept': 'text/event-stream',
          'X-Requested-With': 'fetch'
        },
        body: JSON.stringify(data)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder()

        let chunkCount = 0
        const startTime = performance.now()
        
        function readStream() {
          return reader.read().then(({ done, value }) => {
            if (done) {
              const totalTime = performance.now() - startTime
              console.log(`流式读取完成，总共接收 ${chunkCount} 个数据块，耗时 ${totalTime.toFixed(2)}ms`) // 调试日志
              resolve()
              return
            }

            chunkCount++
            const now = performance.now()
            const elapsed = now - startTime
            const chunk = decoder.decode(value, { stream: true })
            console.log(`[${elapsed.toFixed(2)}ms] 第${chunkCount}个数据块，长度:${chunk.length}，内容预览:`, chunk.substring(0, 100)) // 调试日志
            const lines = chunk.split('\n')
            
            lines.forEach(line => {
              if (line.trim()) {
                try {
                  console.log('接收到原始行数据:', line) // 调试日志
                  
                  let jsonStr = line
                  let isSSE = false
                  
                  // 检查是否是 SSE 格式数据
                  if (line.startsWith('data: ')) {
                    jsonStr = line.slice(6) // 移除 "data: " 前缀
                    isSSE = true
                    console.log('SSE格式 - 解析JSON字符串:', jsonStr) // 调试日志
                    
                    if (jsonStr.trim() === '[DONE]') {
                      console.log('接收到完成标志') // 调试日志
                      return
                    }
                  } else {
                    console.log('直接JSON格式 - 解析JSON字符串:', jsonStr) // 调试日志
                  }
                  
                  const parsed = JSON.parse(jsonStr)
                  console.log('解析后的数据:', parsed) // 调试日志
                  
                  // 处理消息数据
                  if (parsed.type === 'message' && parsed.data) {
                    const now = performance.now()
                    const timestamp = new Date().toLocaleTimeString() + '.' + (now % 1000).toFixed(0)
                    console.log(`[${timestamp}] API调用onChunk:`, parsed.data) // 调试日志
                    
                    // 立即调用onChunk，确保实时处理
                    onChunk(parsed.data)
                  }
                } catch (error) {
                  console.warn('解析流式数据失败:', error, 'line:', line)
                }
              }
            })

            return readStream()
          })
        }

        return readStream()
      })
      .catch(error => {
        reject(error)
      })
    })
  },

  // 调试prompt - 媒体生成接口（用于图片、音频、视频）
  async debugPromptMedia(data) {
    // 媒体生成可能需要较长时间，设置50秒超时
    const response = await api.post('/prompts/synthesis/media', data, {
      timeout: 50000 // 50秒
    })
    return response.data
  }
}
