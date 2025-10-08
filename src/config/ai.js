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
    { label: 'GPT-4o', value: 'gpt-4o' },
    { label: 'GPT-5', value: 'gpt-5' },
    { label: 'GPT-4', value: 'gpt-4' },
    { label: 'GPT-5-mini', value: 'gpt-5-mini' }
  ],
  dashscope: [
    { label: 'qwen-plus', value: 'qwen-plus' },
    { label: 'qwen-vl-plus-latest', value: 'qwen-vl-plus-latest' },
    { label: 'qwen-vl-max-latest', value: 'qwen-vl-max-latest' },
    { label: 'qwen-omni-turbo-latest', value: 'qwen-omni-turbo-latest' }
  ],
  deepseek: [
    { label: 'deepseek-chat', value: 'deepseek-chat' },
    { label: 'deepseek-coder', value: 'deepseek-coder' }
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

// 获取指定提供商支持调试的模型选项
export const getDebugSupportedModelsByProvider = (provider) => {
  return DEBUG_SUPPORTED_MODELS[provider] || []
}

// 获取支持调试的提供商选项
export const getDebugSupportedProviders = () => {
  return AI_PROVIDER_OPTIONS.filter(provider => 
    DEBUG_SUPPORTED_MODELS[provider] && DEBUG_SUPPORTED_MODELS[provider].length > 0
  )
}

// 检查模型是否支持调试
export const isModelSupportedForDebug = (model, provider) => {
  const supportedModels = getDebugSupportedModelsByProvider(provider)
  return supportedModels.some(m => m.value === model)
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