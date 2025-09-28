import request from '@/utils/request'

export const promptApi = {
  // 获取prompt列表
  getPrompts(params = {}) {
    return request({
      url: '/prompts',
      method: 'get',
      params
    })
  },

  // 获取单个prompt详情
  getPrompt(id) {
    return request({
      url: `/prompts/${id}`,
      method: 'get'
    })
  },

  // 创建prompt
  createPrompt(data) {
    return request({
      url: '/prompts',
      method: 'post',
      data
    })
  },

  // 更新prompt
  updatePrompt(id, data) {
    return request({
      url: `/prompts/${id}`,
      method: 'put',
      data
    })
  },

  // 删除prompt
  deletePrompt(id) {
    return request({
      url: `/prompts/${id}`,
      method: 'delete'
    })
  },

  // 发布prompt（版本号+1）
  publishPrompt(id) {
    return request({
      url: `/prompts/${id}/publish`,
      method: 'post'
    })
  },

  // 获取prompt历史版本
  getPromptHistory(id, params = {}) {
    return request({
      url: `/prompts/${id}/history`,
      method: 'get',
      params
    })
  },

  // 获取特定版本的prompt
  getPromptVersion(id, version) {
    return request({
      url: `/prompts/${id}/versions/${version}`,
      method: 'get'
    })
  }
}