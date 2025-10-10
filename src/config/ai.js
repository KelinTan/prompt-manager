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
    { 
      label: 'GPT-4o', 
      value: 'gpt-4o', 
      capabilities: {
        inputTypes: ['text'],
        returnTypes: ['text', 'json_object']
      }
    },
    { 
      label: 'GPT-5', 
      value: 'gpt-5', 
      capabilities: {
        inputTypes: ['text'],
        returnTypes: ['text', 'json_object']
      }
    },
    { 
      label: 'GPT-4', 
      value: 'gpt-4', 
      capabilities: {
        inputTypes: ['text'],
        returnTypes: ['text', 'json_object']
      }
    },
    { 
      label: 'GPT-5-mini', 
      value: 'gpt-5-mini', 
      capabilities: {
        inputTypes: ['text'],
        returnTypes: ['text', 'json_object']
      }
    }
  ],
  dashscope: [
    { 
      label: 'qwen-plus', 
      value: 'qwen-plus', 
      capabilities: {
        inputTypes: ['text'],
        returnTypes: ['text', 'json_object']
      }
    },
    { 
      label: 'qwen3-max', 
      value: 'qwen3-max', 
      capabilities: {
        inputTypes: ['text'],
        returnTypes: ['text', 'json_object']
      }
    },
    { 
      label: 'qwen3-vl-plus', 
      value: 'qwen3-vl-plus', 
      capabilities: {
        inputTypes: ['text', 'image', 'video'],
        returnTypes: ['text', 'json_object']
      }
    },
    { 
      label: 'qwen-vl-plus-latest', 
      value: 'qwen-vl-plus-latest', 
      capabilities: {
        inputTypes: ['text', 'image', 'video'],
        returnTypes: ['text', 'json_object']
      }
    },
    { 
      label: 'qwen-vl-max-latest', 
      value: 'qwen-vl-max-latest', 
      capabilities: {
        inputTypes: ['text', 'image', 'video'],
        returnTypes: ['text', 'json_object']
      }
    },
    { 
      label: 'qwen-omni-turbo-latest', 
      value: 'qwen-omni-turbo-latest', 
      capabilities: {
        inputTypes: ['text', 'image', 'audio', 'video'],
        returnTypes: ['text', 'json_object']
      }
    },
    { 
      label: 'wanx2.1-t2i-turbo (文生图)', 
      value: 'wanx2.1-t2i-turbo', 
      capabilities: {
        inputTypes: ['text'],
        returnTypes: ['image']
      }
    }
  ],
  deepseek: [
    { 
      label: 'deepseek-chat', 
      value: 'deepseek-chat', 
      capabilities: {
        inputTypes: ['text'],
        returnTypes: ['text', 'json_object']
      }
    },
    { 
      label: 'deepseek-coder', 
      value: 'deepseek-coder', 
      capabilities: {
        inputTypes: ['text'],
        returnTypes: ['text', 'json_object']
      }
    }
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

// ===== 新的能力检查函数 =====

// 检查模型是否支持指定的输入类型
export const isModelSupportInputType = (model, provider, inputType) => {
  const models = getModelsByProvider(provider)
  const modelOption = models.find(m => m.value === model)
  if (!modelOption?.capabilities?.inputTypes) {
    return false
  }
  return modelOption.capabilities.inputTypes.includes(inputType)
}

// 检查模型是否支持指定的返回类型
export const isModelSupportReturnType = (model, provider, returnType) => {
  const models = getModelsByProvider(provider)
  const modelOption = models.find(m => m.value === model)
  if (!modelOption?.capabilities?.returnTypes) {
    return false
  }
  return modelOption.capabilities.returnTypes.includes(returnType)
}

// 检查模型是否同时支持指定的输入类型和返回类型
export const isModelSupportTypes = (model, provider, inputType, returnType) => {
  return isModelSupportInputType(model, provider, inputType) && 
         isModelSupportReturnType(model, provider, returnType)
}

// 根据输入类型过滤可用的模型
export const getModelsByProviderAndInputType = (provider, inputType) => {
  const models = getModelsByProvider(provider)
  if (!inputType || inputType === 'text') {
    // 如果没有指定类型或类型是 text，返回所有模型
    return models
  }
  // 过滤出支持该输入类型的模型
  return models.filter(m => 
    m.capabilities?.inputTypes?.includes(inputType)
  )
}

// 根据返回类型过滤可用的模型
export const getModelsByProviderAndReturnType = (provider, returnType) => {
  const models = getModelsByProvider(provider)
  if (!returnType) {
    return models
  }
  // 过滤出支持该返回类型的模型
  return models.filter(m => 
    m.capabilities?.returnTypes?.includes(returnType)
  )
}

// 根据输入类型和返回类型过滤可用的模型
export const getModelsByProviderAndTypes = (provider, inputType, returnType) => {
  const models = getModelsByProvider(provider)
  
  // 如果都没有指定，返回所有模型
  if (!inputType && !returnType) {
    return models
  }
  
  return models.filter(m => {
    const capabilities = m.capabilities
    if (!capabilities) return false
    
    const inputMatch = !inputType || capabilities.inputTypes?.includes(inputType)
    const returnMatch = !returnType || capabilities.returnTypes?.includes(returnType)
    
    return inputMatch && returnMatch
  })
}

// 获取模型支持的输入类型列表
export const getModelSupportedInputTypes = (model, provider) => {
  const models = getModelsByProvider(provider)
  const modelOption = models.find(m => m.value === model)
  return modelOption?.capabilities?.inputTypes || ['text']
}

// 获取模型支持的返回类型列表
export const getModelSupportedReturnTypes = (model, provider) => {
  const models = getModelsByProvider(provider)
  const modelOption = models.find(m => m.value === model)
  return modelOption?.capabilities?.returnTypes || ['text']
}

// 获取模型的完整能力信息
export const getModelCapabilities = (model, provider) => {
  const models = getModelsByProvider(provider)
  const modelOption = models.find(m => m.value === model)
  return modelOption?.capabilities || {
    inputTypes: ['text'],
    returnTypes: ['text']
  }
}

// ===== 向后兼容的函数（保持旧代码能正常工作） =====

// 检查模型是否支持指定的 prompt 类型（向后兼容，映射到输入类型）
export const isModelSupportType = (model, provider, type) => {
  return isModelSupportInputType(model, provider, type)
}

// 根据 prompt 类型过滤可用的模型（向后兼容，映射到输入类型）
export const getModelsByProviderAndType = (provider, type) => {
  return getModelsByProviderAndInputType(provider, type)
}

// 获取模型支持的类型列表（向后兼容，返回输入类型）
export const getModelSupportedTypes = (model, provider) => {
  return getModelSupportedInputTypes(model, provider)
}