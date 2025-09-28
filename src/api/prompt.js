import api from '@/api/request'

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

  // 获取prompt历史版本
  async getPromptHistory(id, params = {}) {
    const response = await api.get(`/prompts/${id}/history`, { params })
    return response.data
  },

  // 获取特定版本的prompt
  async getPromptVersion(id, version) {
    const response = await api.get(`/prompts/${id}/versions/${version}`)
    return response.data
  }
}