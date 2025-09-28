// Prompt数据模型，对应数据库结构
export class Prompt {
  constructor(data = {}) {
    this.id = data.id || null
    this.name = data.name || ''
    this.title = data.title || ''
    this.type = data.type || ''
    this.model = data.model || ''
    this.return_type = data.return_type || ''
    this.template = data.template || ''
    this.mock = data.mock !== undefined ? data.mock : true
    this.mock_data = data.mock_data || {}
    this.remark = data.remark || ''
    this.format_type = data.format_type || 'braces'
    this.ai_provider = data.ai_provider || ''
    this.created_at = data.created_at || null
    this.updated_at = data.updated_at || null
    this.version = data.version || 1
  }

  // 获取格式化的创建时间
  getFormattedCreatedAt() {
    if (!this.created_at) return ''
    return new Date(this.created_at).toLocaleString('zh-CN')
  }

  // 获取格式化的更新时间
  getFormattedUpdatedAt() {
    if (!this.updated_at) return ''
    return new Date(this.updated_at).toLocaleString('zh-CN')
  }

  // 验证必填字段
  validate() {
    const errors = []
    if (!this.name.trim()) errors.push('唯一标识不能为空')
    if (!this.title.trim()) errors.push('标题不能为空')
    if (!this.template.trim()) errors.push('模板不能为空')
    return errors
  }


}

// 格式类型选项
export const FORMAT_TYPE_OPTIONS = [
  { label: '方括号 []', value: 'square_brackets' },
  { label: '花括号 {}', value: 'braces' },
  { label: '无格式', value: 'none' }
]

// AI提供商选项
export const AI_PROVIDER_OPTIONS = [
  { label: 'OpenAI', value: 'openai' },
  { label: 'Claude', value: 'claude' },
  { label: 'Gemini', value: 'gemini' },
  { label: 'ChatGLM', value: 'chatglm' },
  { label: '其他', value: 'other' }
]

// 返回类型选项
export const RETURN_TYPE_OPTIONS = [
  { label: 'JSON', value: 'json' },
  { label: 'Text', value: 'text' },
  { label: 'Markdown', value: 'markdown' },
  { label: 'HTML', value: 'html' }
]