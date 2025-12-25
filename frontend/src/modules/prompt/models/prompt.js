// Prompt数据模型，对应数据库结构
export class Prompt {
  constructor(data = {}) {
    this.id = data.id || null
    this.name = data.name || ''
    this.title = data.title || ''
    this.type = data.type || 'text'
    this.model = data.model || ''
    this.return_type = data.return_type || 'json_object'
    this.template = data.template || ''
    this.mock = data.mock !== undefined ? data.mock : false
    this.mock_data = data.mock_data || ''
    this.remark = data.remark || ''
    this.format_type = data.format_type || 'none'
    this.ai_provider = data.ai_provider || 'openai'
    this.urls = data.urls || [] // audio/video 类型的 URL 列表
    this.created_at = data.created_at || null
    this.updated_at = data.updated_at || null
    this.version = data.version || 1
    this.status = data.status || 'draft' // draft | published
    this.is_latest = data.is_latest !== undefined ? data.is_latest : true
    this.root_id = data.root_id || null
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

    // audio 和 video 类型需要至少一个 URL
    if (
      (this.type === 'audio' || this.type === 'video') &&
      (!this.urls || this.urls.length === 0)
    ) {
      errors.push(`${this.type === 'audio' ? '音频' : '视频'}类型需要至少提供一个URL`)
    }

    return errors
  }

  // 判断当前类型是否需要 URLs
  needsUrls() {
    return this.type === 'audio' || this.type === 'video'
  }
}

// 格式类型选项
export const FORMAT_TYPE_OPTIONS = [
  { label: '方括号 []', value: 'square_brackets' },
  { label: '花括号 {}', value: 'braces' },
  { label: '无', value: 'none' }
]

// 返回类型选项
export const RETURN_TYPE_OPTIONS = [
  { label: 'Text', value: 'text' },
  { label: 'JSON', value: 'json_object' },
  { label: 'Image', value: 'image' },
  { label: 'Audio', value: 'audio' },
  { label: 'Video', value: 'video' }
]

// Prompt类型选项
export const PROMPT_TYPE_OPTIONS = [
  { label: 'Text', value: 'text' },
  { label: 'Image', value: 'image' },
  { label: 'Audio', value: 'audio' },
  { label: 'Video', value: 'video' }
]

// Prompt状态选项
export const PROMPT_STATUS_OPTIONS = [
  { label: '草稿', value: 'draft' },
  { label: '已发布', value: 'published' },
  { label: '已归档', value: 'archived' }
]
