/**
 * 任务数据模型
 */
export class Task {
  constructor(data = {}) {
    this.id = data.id || null
    this.uuid = data.uuid || ''
    this.task_type = data.task_type || ''
    this.status = data.status || 'pending' // pending, started, success, failure, canceled
    this.params = data.params || {}
    this.result = data.result || null
    this.retry_count = data.retry_count || 0
    this.cost_time = data.cost_time || 0
    this.error_message = data.error_message || ''
    this.created_at = data.created_at || null
    this.updated_at = data.updated_at || null
  }
}

// 任务状态选项
export const TASK_STATUS_OPTIONS = [
  { label: '待处理', value: 'pending', type: 'warning', color: '#f59e0b' },
  { label: '执行中', value: 'started', type: 'primary', color: '#3b82f6' },
  { label: '成功', value: 'success', type: 'success', color: '#10b981' },
  { label: '失败', value: 'failure', type: 'danger', color: '#ef4444' },
  { label: '已取消', value: 'canceled', type: 'info', color: '#909399' }
]

// 获取状态信息
export function getStatusInfo(status) {
  const option = TASK_STATUS_OPTIONS.find(item => item.value === status)
  return option || { label: status, type: 'info', color: '#909399' }
}

// 格式化持续时间（毫秒转秒）
export function formatDuration(ms) {
  if (!ms) return '-'
  return `${(ms / 1000).toFixed(2)}s`
}

// 格式化日期
export function formatDate(dateString) {
  if (!dateString) return '-'
  try {
    const date = new Date(dateString)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch {
    return dateString
  }
}

// 格式化 JSON
export function formatJson(str) {
  if (!str) return ''
  try {
    const obj = typeof str === 'string' ? JSON.parse(str) : str
    return JSON.stringify(obj, null, 2)
  } catch {
    return str
  }
}
