/**
 * AI提供商和模型配置
 * 统一管理所有AI相关的选项，确保整个应用保持一致
 */

// AI提供商选项
export const AI_PROVIDER_OPTIONS = [
  { label: 'OpenAI', value: 'openai' },
  { label: 'DashScope', value: 'dashscope' },
  { label: 'Deepseek', value: 'deepseek' }
]

// 各提供商对应的模型选项
export const MODEL_OPTIONS = {
  openai: [
    { label: 'GPT-4o', value: 'gpt-4o', supportedTypes: ['text'] },
    { label: 'GPT-5', value: 'gpt-5', supportedTypes: ['text'] },
    { label: 'GPT-4', value: 'gpt-4', supportedTypes: ['text'] },
    { label: 'GPT-5-mini', value: 'gpt-5-mini', supportedTypes: ['text'] }
  ],
  dashscope: [
    { label: 'qwen-plus', value: 'qwen-plus', supportedTypes: ['text'] },
    { label: 'qwen-vl-plus-latest', value: 'qwen-vl-plus-latest', supportedTypes: ['text', 'image', 'video'] },
    { label: 'qwen-vl-max-latest', value: 'qwen-vl-max-latest', supportedTypes: ['text', 'image', 'video'] },
    { label: 'qwen-omni-turbo-latest', value: 'qwen-omni-turbo-latest', supportedTypes: ['text', 'image', 'audio', 'video'] }
  ],
  deepseek: [
    { label: 'deepseek-chat', value: 'deepseek-chat', supportedTypes: ['text'] },
    { label: 'deepseek-coder', value: 'deepseek-coder', supportedTypes: ['text'] }
  ]
}

// 获取指定提供商的模型选项
export const getModelsByProvider = (provider) => {
  return MODEL_OPTIONS[provider] || []
}

// 获取指定提供商的默认模型
export const getDefaultModel = (provider) => {
  const models = getModelsByProvider(provider)
  return models.length > 0 ? models[0].value : ''
}

// AI调试支持的模型（仅支持部分模型进行调试）
export const DEBUG_SUPPORTED_MODELS = {
  openai: [
    { label: 'GPT-4o', value: 'gpt-4o' },
    { label: 'GPT-4', value: 'gpt-4' },
    { label: 'GPT-5-mini', value: 'gpt-5-mini' }
  ],
  dashscope: [
    { label: 'qwen-plus', value: 'qwen-plus' }
  ]
}

// 验证模型是否属于指定提供商
export const isValidModelForProvider = (model, provider) => {
  const models = getModelsByProvider(provider)
  return models.some(m => m.value === model)
}

// 获取所有可用的提供商值
export const getAllProviders = () => {
  return AI_PROVIDER_OPTIONS.map(option => option.value)
}

// 根据提供商值获取提供商标签
export const getProviderLabel = (provider) => {
  const option = AI_PROVIDER_OPTIONS.find(opt => opt.value === provider)
  return option ? option.label : provider
}

// 根据模型值和提供商获取模型标签
export const getModelLabel = (model, provider) => {
  const models = getModelsByProvider(provider)
  const modelOption = models.find(m => m.value === model)
  return modelOption ? modelOption.label : model
}

// 检查模型是否支持指定的 prompt 类型
export const isModelSupportType = (model, provider, type) => {
  const models = getModelsByProvider(provider)
  const modelOption = models.find(m => m.value === model)
  if (!modelOption || !modelOption.supportedTypes) {
    return false
  }
  return modelOption.supportedTypes.includes(type)
}

// 根据 prompt 类型过滤可用的模型
export const getModelsByProviderAndType = (provider, type) => {
  const models = getModelsByProvider(provider)
  if (!type || type === 'text') {
    // 如果没有指定类型或类型是 text，返回所有模型
    return models
  }
  // 过滤出支持该类型的模型
  return models.filter(m => m.supportedTypes && m.supportedTypes.includes(type))
}

// 获取模型支持的类型列表
export const getModelSupportedTypes = (model, provider) => {
  const models = getModelsByProvider(provider)
  const modelOption = models.find(m => m.value === model)
  return modelOption?.supportedTypes || ['text']
}