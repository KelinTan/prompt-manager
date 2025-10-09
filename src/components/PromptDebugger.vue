<template>
  <div class="prompt-debugger">
    <!-- 调试配置区域 -->
    <div v-if="!hasStarted" class="debug-config">
      <el-form :model="debugConfig" label-width="100px" size="default">
        <el-form-item label="AI提供商">
          <el-select 
            v-model="debugConfig.aiProvider" 
            placeholder="选择提供商" 
            style="width: 100%"
            @change="onProviderChange"
          >
            <el-option 
              v-for="provider in aiProviderOptions" 
              :key="provider.value" 
              :label="provider.label" 
              :value="provider.value" 
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="AI模型">
          <el-select 
            v-model="debugConfig.model" 
            placeholder="选择模型" 
            style="width: 100%"
            :disabled="!debugConfig.aiProvider"
          >
            <el-option 
              v-for="model in availableModels" 
              :key="model.value" 
              :label="model.label" 
              :value="model.value" 
            />
          </el-select>
          <el-text v-if="!debugConfig.aiProvider" type="info" size="small" style="margin-top: 4px;">
            请先选择AI提供商
          </el-text>
        </el-form-item>

        <el-form-item label="参数格式">
          <el-select 
            v-model="debugConfig.formatType" 
            placeholder="选择参数格式类型" 
            style="width: 100%"
          >
            <el-option 
              v-for="format in formatTypeOptions" 
              :key="format.value" 
              :label="format.label" 
              :value="format.value" 
            />
          </el-select>
          <el-text type="info" size="small" style="margin-top: 4px;">
            选择模板中参数的格式类型，如 [param] 或 {param}
          </el-text>
        </el-form-item>

        <el-form-item label="Prompt模板">
          <el-input
            v-model="debugConfig.template"
            type="textarea"
            :autosize="{ minRows: 8, maxRows: 20 }"
            placeholder="编辑你的prompt模板..."
            show-word-limit
            resize="vertical"
          />
          <div style="margin-top: 8px; display: flex; justify-content: space-between; align-items: center;">
            <el-text type="info" size="small">
              根据选择的参数格式在模板中使用参数，如：[用户名]、{产品名称} 等
            </el-text>
            <el-button size="small" @click="showPreviewDialog = true" :disabled="!debugConfig.template">
              预览模板
            </el-button>
          </div>
        </el-form-item>

        <!-- 参数设置区域 -->
        <div class="template-variables">
          <el-divider content-position="left">
            模板参数
            <el-button 
              type="primary" 
              size="small" 
              @click="addCustomParameter" 
              style="margin-left: 10px;"
              :icon="ElIconPlus"
            >
              添加参数
            </el-button>
          </el-divider>
          
          <!-- 从模板自动提取的参数 -->
          <div v-if="templateVariables.length > 0">
            <el-text type="success" size="small">自动检测到的参数：</el-text>
            <el-form-item 
              v-for="variable in templateVariables" 
              :key="`auto-${variable}`"
              :label="variable"
              class="parameter-item"
            >
              <el-input
                v-model="debugConfig.variables[variable]"
                :placeholder="`请输入 ${variable} 的值`"
              />
            </el-form-item>
          </div>

          <!-- 手动添加的参数 -->
          <div v-if="customParameters.length > 0">
            <el-text type="info" size="small">手动添加的参数：</el-text>
            <el-form-item 
              v-for="(param, index) in customParameters" 
              :key="`custom-${index}`"
              :label="param.name"
              class="parameter-item"
            >
              <div class="parameter-input-group">
                <el-input
                  v-model="param.name"
                  placeholder="参数名称"
                  style="width: 150px; margin-right: 8px;"
                  @blur="updateParameterName(index, param.name)"
                />
                <el-input
                  v-model="debugConfig.variables[param.name]"
                  :placeholder="`请输入 ${param.name} 的值`"
                  style="flex: 1; margin-right: 8px;"
                />
                <el-button 
                  type="danger" 
                  size="small" 
                  @click="removeCustomParameter(index)"
                  :icon="ElIconDelete"
                />
              </div>
            </el-form-item>
          </div>

          <!-- 空状态提示 -->
          <div v-if="templateVariables.length === 0 && customParameters.length === 0" class="empty-parameters">
            <el-text type="info">
              暂无参数。您可以在模板中使用参数（如 [参数名] 或 {参数名}），或手动添加参数。
            </el-text>
          </div>
        </div>

        <!-- 高级设置 -->
        <!-- <el-collapse v-model="advancedSettingsOpen">
          <el-collapse-item title="高级设置" name="advanced">
            <el-form-item label="温度">
              <el-slider 
                v-model="debugConfig.temperature" 
                :min="0" 
                :max="2" 
                :step="0.1"
                show-input
              />
            </el-form-item>
            <el-form-item label="最大tokens">
              <el-input-number 
                v-model="debugConfig.maxTokens" 
                :min="1" 
                :max="4000"
                style="width: 100%"
              />
            </el-form-item>
          </el-collapse-item>
        </el-collapse> -->
      </el-form>

      <div class="config-actions">
        <el-button type="primary" @click="startDebugWithConfig" :disabled="!canDebugWithConfig">
          <el-icon><Loading v-if="isDebugging" /></el-icon>
          开始调试
        </el-button>
        <el-button @click="resetConfig">重置配置</el-button>
      </div>
    </div>

        <!-- 实时调试结果显示 -->
    <div v-else class="streaming-result">
      <div class="result-header">
        <div class="result-meta">
          <el-tag type="primary" size="small" v-if="isDebugging">
            <el-icon class="is-loading" style="margin-right: 4px;">
              <Loading />
            </el-icon>
            正在生成...
          </el-tag>
          <el-tag type="success" size="small" v-else-if="streamBuffer && !isDebugging">
            生成完成
          </el-tag>
          <el-tag type="info" size="small" v-if="streamBuffer && !isDebugging && debugDuration > 0">
            耗时: {{ debugDuration }}ms
          </el-tag>
          <el-tag type="info" size="small" v-if="totalCharCount > 0">
            字符进度: {{ visibleCharCount }} / {{ totalCharCount }}
          </el-tag>
          <el-tag type="warning" size="small" v-if="useCharByChar">
            实时模式
          </el-tag>
        </div>
        
        <div class="result-actions">
          <el-button size="small" @click="backToConfig">
            <el-icon><Back /></el-icon>
            重新配置
          </el-button>
          <el-button 
            v-if="streamBuffer" 
            size="small" 
            @click="copyResult"
          >
            复制结果
          </el-button>
        </div>
      </div>
      
      <div class="streaming-text">
        <div style="font-family: monospace; white-space: pre-wrap; padding: 12px; background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 6px; min-height: 100px; line-height: 1.5;">
          <span v-if="useCharByChar">{{ currentVisibleText }}</span>
          <span v-else>{{ streamBuffer }}</span>
          <span v-if="isDebugging" class="cursor">|</span>
        </div>
      </div>
    </div>

    <!-- Markdown 预览弹窗 -->
    <el-dialog
      v-model="showPreviewDialog"
      title="模板预览"
      width="70%"
    >
      <PromptMarkdownPreview :content="debugConfig.template" />
    </el-dialog>

  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading, Back, Plus, Delete } from '@element-plus/icons-vue'
import { promptApi } from '@/api/prompt'
import PromptMarkdownPreview from '@/components/PromptMarkdownPreview.vue'
import { 
  getDefaultModel, 
  isValidModelForProvider,
  getDebugSupportedProviders,
  getDebugSupportedModelsByProvider,
  isModelSupportedForDebug
} from '@/config/ai'
import { FORMAT_TYPE_OPTIONS } from '@/models/prompt'

export default {
  name: 'PromptDebugger',
  components: {
    Loading,
    Back,
    PromptMarkdownPreview
  },
  props: {
    model: {
      type: String,
      default: ''
    },
    aiProvider: {
      type: String,
      default: ''
    },
    template: {
      type: String,
      default: ''
    },
    formatType: {
      type: String,
      default: 'square_brackets'
    },
    autoStart: {
      type: Boolean,
      default: false
    }
  },
  emits: ['debug-complete'],
  setup(props, { emit }) {
    const isDebugging = ref(false)
    const debugResult = ref('')
    const debugError = ref('')
    const debugDuration = ref(0)
    const streamBuffer = ref('')

    const debugStartTime = ref(0)
    const useCharByChar = ref(false) // 是否使用逐字符显示模式
    const visibleCharCount = ref(0) // 当前可见字符数
    const totalCharCount = ref(0) // 总字符数
    const fullText = ref('') // 完整文本
    const hasStarted = ref(false) // 是否已开始调试
    const advancedSettingsOpen = ref([]) // 高级设置展开状态
    const showPreviewDialog = ref(false) // 控制预览弹窗显示

    // 调试配置
    const debugConfig = ref({
      model: props.model || '',
      aiProvider: props.aiProvider || 'openai',
      template: props.template || '',
      formatType: props.formatType || 'square_brackets',
      variables: {},
    //   temperature: 0.7,
    //   maxTokens: 1000
    })

    // 自定义参数列表
    const customParameters = ref([])

    // AI提供商选项（仅支持调试的提供商）
    const aiProviderOptions = getDebugSupportedProviders()
    
    // 格式化类型选项
    const formatTypeOptions = FORMAT_TYPE_OPTIONS

    // 根据当前提供商获取可用的模型（仅支持调试的模型）
    const availableModels = computed(() => {
      const provider = debugConfig.value.aiProvider
      return getDebugSupportedModelsByProvider(provider)
    })

    // 提供商改变时的处理
    const onProviderChange = (newProvider) => {
      // 清空当前选择的模型
      debugConfig.value.model = ''
      
      // 如果新提供商有可用模型，自动选择第一个
      const supportedModels = getDebugSupportedModelsByProvider(newProvider)
      if (supportedModels.length > 0) {
        debugConfig.value.model = supportedModels[0].value
      }
    }

    // 添加自定义参数
    const addCustomParameter = () => {
      customParameters.value.push({
        name: '',
        value: ''
      })
    }

    // 移除自定义参数
    const removeCustomParameter = (index) => {
      const param = customParameters.value[index]
      if (param && param.name) {
        // 从变量对象中删除对应的值
        delete debugConfig.value.variables[param.name]
      }
      customParameters.value.splice(index, 1)
    }

    // 更新参数名称
    const updateParameterName = (index, newName) => {
      const oldParam = customParameters.value[index]
      if (oldParam && oldParam.name !== newName) {
        // 如果参数名改变了，删除旧的变量值，保留新的
        if (oldParam.name) {
          delete debugConfig.value.variables[oldParam.name]
        }
        oldParam.name = newName
      }
    }
    
    // 计算当前可见的文本
    const currentVisibleText = computed(() => {
      return fullText.value.substring(0, visibleCharCount.value)
    })

    // 提取模板中的变量（根据格式化类型）
    const templateVariables = computed(() => {
      const template = debugConfig.value.template
      const formatType = debugConfig.value.formatType
      let regex
      
      // 根据格式化类型选择正则表达式
      switch (formatType) {
        case 'square_brackets':
          // 只匹配不包含引号、冒号等JSON字符的参数
          regex = /\[([a-zA-Z_][a-zA-Z0-9_]*)\]/g
          break
        case 'braces':
          // 只匹配不包含引号、冒号等JSON字符的参数
          regex = /\{([a-zA-Z_][a-zA-Z0-9_]*)\}/g
          break
        case 'none':
        default:
          return [] // 无格式化时不自动提取参数
      }
      
      const variables = new Set()
      let match
      
      while ((match = regex.exec(template)) !== null) {
        const variable = match[1].trim()
        if (variable) {
          variables.add(variable)
        }
      }
      
      return Array.from(variables)
    })

    // 生成最终的prompt内容（替换变量）
    const finalPrompt = computed(() => {
      let prompt = debugConfig.value.template
      const formatType = debugConfig.value.formatType
      
      // 替换所有参数（包括自动提取的和手动添加的）
      const allVariables = [...templateVariables.value, ...customParameters.value.map(p => p.name)].filter(Boolean)
      
      allVariables.forEach(variable => {
        const value = debugConfig.value.variables[variable] || `[${variable}]`
        let regex
        
        // 根据格式化类型创建替换正则
        switch (formatType) {
          case 'square_brackets':
            regex = new RegExp(`\\[${escapeRegExp(variable)}\\]`, 'g')
            break
          case 'braces':
            regex = new RegExp(`\\{${escapeRegExp(variable)}\\}`, 'g')
            break
          case 'none':
          default:
            // 无格式化时，尝试替换常见的参数格式
            const regex1 = new RegExp(`\\[${escapeRegExp(variable)}\\]`, 'g')
            const regex2 = new RegExp(`\\{${escapeRegExp(variable)}\\}`, 'g')
            prompt = prompt.replace(regex1, value).replace(regex2, value)
            return
        }
        
        prompt = prompt.replace(regex, value)
      })
      
      return prompt
    })

    // 辅助函数：转义正则表达式特殊字符
    const escapeRegExp = (string) => {
      return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    }
    


    const canDebug = computed(() => {
      return props.model?.trim() && 
             props.aiProvider?.trim() && 
             props.template?.trim()
    })

    // 新的配置验证
    const canDebugWithConfig = computed(() => {
      const config = debugConfig.value
      const hasRequiredFields = config.model?.trim() && 
                               config.aiProvider?.trim() && 
                               config.template?.trim()
      
      // 检查模型是否支持调试
      const isModelSupported = isModelSupportedForDebug(config.model, config.aiProvider)
      
      // 检查自动提取的变量是否都有值
      const hasAllAutoVariables = templateVariables.value.every(variable => 
        config.variables[variable]?.trim()
      )
      
      // 检查自定义参数是否都有名称和值
      const hasAllCustomVariables = customParameters.value.every(param => 
        param.name?.trim() && config.variables[param.name]?.trim()
      )
      
      return hasRequiredFields && isModelSupported && hasAllAutoVariables && hasAllCustomVariables
    })

    // 开始调试
    const startDebug = async () => {
      if (!canDebug.value) {
        ElMessage.warning('请填写完整的调试信息')
        return
      }

      isDebugging.value = true
      debugResult.value = ''
      debugError.value = ''
      streamBuffer.value = ''
      debugStartTime.value = Date.now()
      
      // 立即启用逐字符显示模式
      useCharByChar.value = true
      fullText.value = ''
      visibleCharCount.value = 0
      totalCharCount.value = 0

      try {
        
        // 将模板内容作为消息发送给AI
        const message = props.template || '请根据模板生成一个示例内容'
        
        await promptApi.debugPromptStream({
          message: message,
          model: props.model,
          ai_provider: props.aiProvider
        }, (chunk) => {
          // 累积完整文本
          fullText.value += chunk
          totalCharCount.value = fullText.value.length
          
          // 逐字符显示新接收的内容
          const newChars = chunk.split('')
          let charIndex = 0
          
          const showNextChar = () => {
            if (charIndex < newChars.length && visibleCharCount.value < totalCharCount.value) {
              visibleCharCount.value++
              charIndex++
              
              // 继续显示下一个字符
              setTimeout(showNextChar, 30)
            }
          }
          
          // 开始逐字显示
          showNextChar()
          
          // 保持向后兼容
          streamBuffer.value += chunk
        })

        // 流式调用完成
        debugResult.value = fullText.value || streamBuffer.value
        debugDuration.value = Date.now() - debugStartTime.value
        
        // 确保所有字符都显示完成
        if (useCharByChar.value && visibleCharCount.value < totalCharCount.value) {
          visibleCharCount.value = totalCharCount.value
        }
        
        ElMessage.success('调试完成')
        emit('debug-complete')
      } catch (error) {
        debugError.value = error.message || '调试失败，请检查网络连接和参数设置'
        ElMessage.error('调试失败')
        emit('debug-complete')
      } finally {
        isDebugging.value = false
      }
    }

    // 复制结果
    const copyResult = async () => {
      try {
        const textToCopy = streamBuffer.value || debugResult.value
        await navigator.clipboard.writeText(textToCopy)
        ElMessage.success('结果已复制到剪贴板')
      } catch (error) {
        // 降级处理
        const textToCopy = streamBuffer.value || debugResult.value
        const textArea = document.createElement('textarea')
        textArea.value = textToCopy
        document.body.appendChild(textArea)
        textArea.select()
        document.execCommand('copy')
        document.body.removeChild(textArea)
        ElMessage.success('结果已复制到剪贴板')
      }
    }

    // 清空结果
    const clearResult = () => {
      debugResult.value = ''
      debugError.value = ''
      streamBuffer.value = ''
      debugDuration.value = 0
      isDebugging.value = false
      
      // 重置逐字符显示状态
      useCharByChar.value = false
      fullText.value = ''
      visibleCharCount.value = 0
      totalCharCount.value = 0
    }

    // 使用配置开始调试
    const startDebugWithConfig = async () => {
      hasStarted.value = true
      
      isDebugging.value = true
      debugResult.value = ''
      debugError.value = ''
      streamBuffer.value = ''
      debugStartTime.value = Date.now()
      
      // 立即启用逐字符显示模式
      useCharByChar.value = true
      fullText.value = ''
      visibleCharCount.value = 0
      totalCharCount.value = 0

      try {
        // 使用最终的prompt（已替换变量）
        const message = finalPrompt.value
        
        await promptApi.debugPromptStream({
          message: message,
          model: debugConfig.value.model,
          ai_provider: debugConfig.value.aiProvider,
          temperature: debugConfig.value.temperature,
          max_tokens: debugConfig.value.maxTokens
        }, (chunk) => {
          // 累积完整文本
          fullText.value += chunk
          totalCharCount.value = fullText.value.length
          
          // 逐字符显示新接收的内容
          const newChars = chunk.split('')
          let charIndex = 0
          
          const showNextChar = () => {
            if (charIndex < newChars.length && visibleCharCount.value < totalCharCount.value) {
              visibleCharCount.value++
              charIndex++
              
              // 继续显示下一个字符
              setTimeout(showNextChar, 30)
            }
          }
          
          // 开始逐字显示
          showNextChar()
          
          // 保持向后兼容
          streamBuffer.value += chunk
        })

        // 流式调用完成
        debugResult.value = fullText.value || streamBuffer.value
        debugDuration.value = Date.now() - debugStartTime.value
        
        // 确保所有字符都显示完成
        if (useCharByChar.value && visibleCharCount.value < totalCharCount.value) {
          visibleCharCount.value = totalCharCount.value
        }
        
        ElMessage.success('调试完成')
        emit('debug-complete')
      } catch (error) {
        debugError.value = error.message || '调试失败，请检查网络连接和参数设置'
        ElMessage.error('调试失败')
        emit('debug-complete')
      } finally {
        isDebugging.value = false
      }
    }

    // 重置配置
    const resetConfig = () => {
      const provider = props.aiProvider || 'openai'
      const defaultModel = getDefaultModel(provider)
      
      debugConfig.value = {
        model: props.model || defaultModel,
        aiProvider: provider,
        template: props.template || '',
        variables: {},
        temperature: 0.7,
        maxTokens: 1000
      }
    }

    // 返回配置页面
    const backToConfig = () => {
      hasStarted.value = false
      clearResult()
    }

    // 加载外部配置（从PromptEdit等页面传递过来）
    const loadExternalConfig = (config) => {
      if (config) {
        // 先设置提供商
        const provider = config.aiProvider || debugConfig.value.aiProvider
        debugConfig.value.aiProvider = provider
        debugConfig.value.template = config.template || debugConfig.value.template
        
        // 加载参数格式类型
        if (config.formatType) {
          debugConfig.value.formatType = config.formatType
        }
        
        // 验证模型是否适用于当前提供商
        if (config.model && isValidModelForProvider(config.model, provider)) {
          debugConfig.value.model = config.model
        } else {
          // 如果模型不适用，使用该提供商的默认模型
          debugConfig.value.model = getDefaultModel(provider)
        }
        
        // 重置其他状态
        hasStarted.value = false
        clearResult()
        
        console.log('已加载外部配置到PromptDebugger:', config)
      }
    }

    // 监听 autoStart 变化，自动开始调试
    watch(() => props.autoStart, (newVal) => {
      if (newVal && canDebug.value) {
        // 重置所有状态，开始新的调试
        debugResult.value = ''
        debugError.value = ''
        streamBuffer.value = ''
        debugDuration.value = 0
        startDebug()
      }
    }, { immediate: true })

    // 监听props变化，同步到配置
    watch(() => [props.model, props.aiProvider, props.template, props.formatType], ([model, aiProvider, template, formatType]) => {
      const provider = aiProvider || debugConfig.value.aiProvider
      debugConfig.value.aiProvider = provider
      debugConfig.value.template = template || debugConfig.value.template
      debugConfig.value.formatType = formatType || debugConfig.value.formatType
      
      // 设置模型：优先使用props中的model，如果没有则使用该提供商的默认模型
      if (model) {
        debugConfig.value.model = model
      } else {
        const defaultModel = getDefaultModel(provider)
        if (defaultModel && !debugConfig.value.model) {
          debugConfig.value.model = defaultModel
        }
      }
      
      // 重置调试状态
      debugResult.value = ''
      debugError.value = ''
      streamBuffer.value = ''
      hasStarted.value = false
    }, { immediate: true })

    // 监听模板变量变化，同步变量对象
    watch(templateVariables, (newVariables, oldVariables = []) => {
      // 保留现有的变量值，只为新变量添加空值
      newVariables.forEach(variable => {
        if (!(variable in debugConfig.value.variables)) {
          debugConfig.value.variables[variable] = ''
        }
      })
      
      // 清理不再使用的自动提取变量（但保留自定义参数的变量）
      const customParamNames = customParameters.value.map(p => p.name).filter(Boolean)
      Object.keys(debugConfig.value.variables).forEach(key => {
        if (!newVariables.includes(key) && !customParamNames.includes(key)) {
          delete debugConfig.value.variables[key]
        }
      })
    }, { immediate: true })





    return {
      isDebugging,
      debugResult,
      debugError,
      debugDuration,
      streamBuffer,
      useCharByChar,
      visibleCharCount,
      totalCharCount,
      fullText,
      currentVisibleText,
      hasStarted,
      advancedSettingsOpen,
      showPreviewDialog,
      debugConfig,
      aiProviderOptions,
      formatTypeOptions,
      availableModels,
      customParameters,
      onProviderChange,
      templateVariables,
      finalPrompt,
      canDebug,
      canDebugWithConfig,
      startDebug,
      startDebugWithConfig,
      resetConfig,
      backToConfig,
      loadExternalConfig,
      copyResult,
      clearResult,
      addCustomParameter,
      removeCustomParameter,
      updateParameterName,
      // 图标组件
      ElIconPlus: Plus,
      ElIconDelete: Delete
    }
  }
}
</script>

<style scoped>
.prompt-debugger {
  padding: 0;
}





.streaming-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #409eff;
  font-size: 14px;
  margin-bottom: 12px;
}

.stream-preview {
  margin-top: 10px;
  background: #f0f9ff;
  border-radius: 4px;
  padding: 12px;
  border: 1px solid #b3d8ff;
  max-height: 200px;
  overflow-y: auto;
}

.streaming-result {
  background: #fff;
  border-radius: 6px;
  padding: 15px;
  border: 1px solid #e4e7ed;
  margin-bottom: 15px;
}

.streaming-text {
  background: #f0f9ff;
  border-radius: 4px;
  padding: 16px;
  border: 1px solid #b3d8ff;
  min-height: 60px;
  max-height: 400px;
  overflow-y: auto;
}

.streaming-text pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #1f2937;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.6;
}

.cursor {
  display: inline-block;
  background-color: #409eff;
  animation: blink 1s infinite;
  width: 2px;
  margin-left: 1px;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.streaming-result {
  margin: 16px 0;
  padding: 0;
}

.result-meta {
  margin-bottom: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.streaming-result .streaming-text {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.debug-config {
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.config-actions {
  margin-top: 20px;
  text-align: center;
  padding-top: 16px;
  border-top: 1px solid #e0e0e0;
}

.config-actions .el-button {
  margin: 0 8px;
}

.template-variables {
  margin: 16px 0;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #409eff;
  overflow: hidden;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.result-actions {
  display: flex;
  align-items: center;
}

.stream-preview pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #1f2937;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.5;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

:deep(.el-textarea__inner) {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  line-height: 1.6;
}

.template-variables {
  margin: 16px 0;
}

.parameter-item {
  margin-bottom: 12px;
}

.parameter-item :deep(.el-form-item__label) {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.parameter-input-group {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  max-width: 100%;
  overflow: hidden;
}

.empty-parameters {
  text-align: center;
  padding: 20px;
  color: #909399;
  background: #f9f9f9;
  border-radius: 4px;
  border: 1px dashed #dcdfe6;
}
</style>