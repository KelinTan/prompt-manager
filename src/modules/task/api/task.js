import api from '@/modules/common/api/request'

/**
 * 任务 API
 */
export const taskApi = {
  /**
   * 获取任务列表
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.size - 每页数量
   * @param {string} params.task_type - 任务类型
   * @param {string} params.status - 任务状态
   */
  async getTasks(params = {}) {
    const response = await api.get('/tasks', { params })
    return response.data
  },

  /**
   * 获取任务详情
   * @param {string|number} id - 任务 ID
   */
  async getTask(id) {
    const response = await api.get(`/tasks/${id}`)
    return response.data
  },

  /**
   * 获取任务类型列表
   */
  async getTaskTypes() {
    const response = await api.get('/tasks/type')
    return response.data || []
  },

  /**
   * 创建任务
   * @param {Object} data - 任务数据
   */
  async createTask(data) {
    const response = await api.post('/tasks', data)
    return response.data
  },

  /**
   * 重试任务
   * @param {string} uuid - 任务 UUID
   */
  async retryTask(uuid) {
    const response = await api.post(`/tasks/${uuid}/retry`)
    return response.data
  },

  /**
   * 取消任务
   * @param {string|number} id - 任务 ID
   */
  async cancelTask(id) {
    const response = await api.post(`/tasks/${id}/cancel`)
    return response.data
  },

  /**
   * 删除任务
   * @param {string|number} id - 任务 ID
   */
  async deleteTask(id) {
    const response = await api.delete(`/tasks/${id}`)
    return response.data
  }
}
