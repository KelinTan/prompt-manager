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
   * @param {string} params.task_uuid - 任务UUID（精确查询）
   * @param {string} params.task_type - 任务类型
   * @param {string} params.status - 任务状态
   */
  async getTasks(params = {}) {
    const response = await api.get('/tasks', { params })
    return response.data
  },

  /**
   * 获取任务类型列表
   * @returns {Array} 任务类型数组，格式：[{value: string, label: string}]
   */
  async getTaskTypes() {
    const response = await api.get('/tasks/type')
    return response.data || []
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
   * @param {string} uuid - 任务 UUID
   */
  async cancelTask(uuid) {
    const response = await api.post(`/tasks/${uuid}/cancel`)
    return response.data
  }
}
