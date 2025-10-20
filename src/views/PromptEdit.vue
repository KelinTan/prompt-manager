<template>
  <div class="prompt-edit">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑 Prompt' : '创建 Prompt' }}</h2>
      <div class="header-actions">
        <el-button @click="handleBack">返回</el-button>
        <el-button 
          type="primary" 
          @click="handleSave"
          :loading="saving"
        >
          保存
        </el-button>
        <el-button
          v-if="isEdit"
          type="warning" 
          @click="handleSaveAndPublish"
          :loading="saving || publishing"
        >
          保存并发布
        </el-button>
        <el-button 
          v-if="isEdit"
          type="success" 
          @click="handlePublish"
          :loading="publishing"
        >
          发布
        </el-button>
      </div>
    </div>

    <el-card shadow="never">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        @submit.prevent
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="标题" prop="title">
              <el-input 
                v-model="form.title" 
                placeholder="请输入Prompt标题"
                maxlength="255"
                show-word-limit
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="业务标识" prop="name">
              <el-input 
                v-model="form.name" 
                placeholder="请输入业务标识（如：user_profile_prompt）"
                maxlength="255"
                show-word-limit
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="类型" prop="type">
              <el-select 
                v-model="form.type" 
                placeholder="请选择类型"
                style="width: 100%"
              >
                <el-option 
                  v-for="option in typeOptions" 
                  :key="option.value" 
                  :label="option.label" 
                  :value="option.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="返回值" prop="return_type">
              <el-select 
                v-model="form.return_type" 
                placeholder="请选择返回值"
                style="width: 100%"
              >
                <el-option 
                  v-for="option in returnTypeOptions" 
                  :key="option.value" 
                  :label="option.label" 
                  :value="option.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="模版参数格式" prop="format_type">
              <el-select 
                v-model="form.format_type" 
                placeholder="请选择模版参数格式"
                style="width: 100%"
              >
                <el-option 
                  v-for="option in formatTypeOptions" 
                  :key="option.value" 
                  :label="option.label" 
                  :value="option.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="启用Mock">
              <el-switch 
                v-model="form.mock"
                active-text="启用"
                inactive-text="禁用"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
           <el-col :span="12">
            <el-form-item label="AI提供商" prop="ai_provider">
              <el-select 
                v-model="form.ai_provider" 
                placeholder="请选择AI提供商"
                style="width: 100%"
              >
                <el-option 
                  v-for="option in aiProviderOptions" 
                  :key="option.value" 
                  :label="option.label" 
                  :value="option.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="模型" prop="model">
              <el-select 
                v-model="form.model" 
                placeholder="请选择模型"
                style="width: 100%"
                :disabled="!form.ai_provider"
              >
                <el-option 
                  v-for="model in availableModels" 
                  :key="model.value" 
                  :label="model.label" 
                  :value="model.value" 
                />
              </el-select>
              <el-text v-if="!form.ai_provider" type="info" size="small" style="margin-top: 4px; display: block;">
                请先选择AI提供商
              </el-text>
              <el-text v-else-if="availableModels.length === 0" type="warning" size="small" style="margin-top: 4px; display: block;">
                当前提供商没有支持 {{ form.type || 'text' }} 输入 → {{ form.return_type || 'text' }} 输出的模型
              </el-text>
              <el-text v-else-if="(form.type && form.type !== 'text') || (form.return_type && form.return_type !== 'text')" type="info" size="small" style="margin-top: 4px; display: block;">
                仅显示支持 {{ form.type || 'text' }} 输入 → {{ form.return_type || 'text' }} 输出的模型
              </el-text>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="模板" prop="template">
          <el-input 
            v-model="form.template" 
            type="textarea" 
            :autosize="{ minRows: 8, maxRows: 20 }"
            placeholder="请输入Prompt模板内容"
            show-word-limit
            resize="vertical"
          />
          <div style="margin-top: 8px; display: flex; justify-content: flex-end; gap: 8px;">
            <el-button type="primary" size="small" plain @click="showPreviewDialog = true" :disabled="!form.template">
              预览模板
            </el-button>
            <el-button 
              type="primary" 
              size="small" 
              plain
              @click="openInAIAssistant"
            >
              <el-icon><ChatDotRound /></el-icon>
              在AI助手中测试
            </el-button>
          </div>
        </el-form-item>

        <!-- (启用Mock 已在上面的 行中与 格式化类型 配对) -->

        <el-form-item v-if="form.mock" label="Mock数据">
          <el-input 
            v-model="mockDataText" 
            type="textarea" 
            :rows="4"
            placeholder="请输入Mock数据"
            @blur="validateMockData"
          />
          <div v-if="mockDataError" class="error-text">
            {{ mockDataError }}
          </div>
        </el-form-item>

        <el-form-item label="备注">
          <el-input 
            v-model="form.remark" 
            type="textarea" 
            :rows="3"
            placeholder="请输入备注信息"
            maxlength="255"
            show-word-limit
          />
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Markdown 预览弹窗 -->
    <el-dialog
      v-model="showPreviewDialog"
      title="模板预览"
      width="70%"
    >
      <PromptMarkdownPreview :content="form.template" />
    </el-dialog>

  </div>
</template>

<script>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ChatDotRound } from '@element-plus/icons-vue'
import { promptApi } from '@/api/prompt'
import { Prompt, FORMAT_TYPE_OPTIONS, RETURN_TYPE_OPTIONS, PROMPT_TYPE_OPTIONS } from '@/models/prompt'
import { 
  AI_PROVIDER_OPTIONS, 
  getModelsByProvider, 
  getDefaultModel, 
  getModelsByProviderAndTypes,
  isModelSupportTypes 
} from '@/config/ai'
import PromptMarkdownPreview from '@/components/PromptMarkdownPreview.vue'


export default {
  name: 'PromptEdit',
  components: {
    PromptMarkdownPreview
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const formRef = ref()
    const saving = ref(false)
    const publishing = ref(false)
    const loading = ref(false)
    const mockDataError = ref('')
    const showPreviewDialog = ref(false) // 控制预览弹窗显示

    // 是否为编辑模式
    const isEdit = computed(() => !!route.params.id)
    const promptId = computed(() => route.params.id)

    // 表单数据
    const form = reactive(new Prompt())

    // Mock数据文本（直接绑定到 form.mock_data）
    const mockDataText = computed({
      get() {
        if (form.mock_data === null || form.mock_data === undefined) return ''
        return typeof form.mock_data === 'string'
          ? form.mock_data
          : JSON.stringify(form.mock_data, null, 2)
      },
      set(val) {
        // always store as string (user requested mock_data is a string)
        form.mock_data = val
      }
    })

    // 选项数据
    const aiProviderOptions = AI_PROVIDER_OPTIONS
    const formatTypeOptions = FORMAT_TYPE_OPTIONS
    const returnTypeOptions = RETURN_TYPE_OPTIONS
    const typeOptions = PROMPT_TYPE_OPTIONS

    // 计算可用模型（根据输入类型和返回类型过滤）
    const availableModels = computed(() => {
      if (!form.ai_provider) return []
      return getModelsByProviderAndTypes(form.ai_provider, form.type, form.return_type)
    })

    // 监听AI供应商变化，自动更新模型
    watch(() => form.ai_provider, (newProvider) => {
      if (newProvider) {
        const models = getModelsByProviderAndTypes(newProvider, form.type, form.return_type)
        if (models.length > 0 && !models.find(m => m.value === form.model)) {
          form.model = models[0]?.value || getDefaultModel(newProvider)
        }
      }
    })

    // 监听输入类型变化，检查当前模型是否支持
    watch(() => form.type, (newType) => {
      if (form.model && form.ai_provider) {
        // 检查当前模型是否支持新的输入类型和返回类型组合
        if (!isModelSupportTypes(form.model, form.ai_provider, newType, form.return_type)) {
          // 如果不支持，尝试选择一个支持该组合的模型
          const supportedModels = getModelsByProviderAndTypes(form.ai_provider, newType, form.return_type)
          if (supportedModels.length > 0) {
            form.model = supportedModels[0].value
            ElMessage.warning(`当前模型不支持该输入输出组合，已自动切换到 ${supportedModels[0].label}`)
          } else {
            ElMessage.warning(`当前提供商没有支持该输入输出组合的模型`)
            form.model = ''
          }
        }
      }
    })

    // 监听返回类型变化，检查当前模型是否支持
    watch(() => form.return_type, (newReturnType) => {
      if (form.model && form.ai_provider) {
        // 检查当前模型是否支持新的输入类型和返回类型组合
        if (!isModelSupportTypes(form.model, form.ai_provider, form.type, newReturnType)) {
          // 如果不支持，尝试选择一个支持该组合的模型
          const supportedModels = getModelsByProviderAndTypes(form.ai_provider, form.type, newReturnType)
          if (supportedModels.length > 0) {
            form.model = supportedModels[0].value
            ElMessage.warning(`当前模型不支持该输入输出组合，已自动切换到 ${supportedModels[0].label}`)
          } else {
            ElMessage.warning(`当前提供商没有支持该输入输出组合的模型`)
            form.model = ''
          }
        }
      }
    })



    // 验证规则
    const rules = {
      title: [
        { required: true, message: '请输入Prompt标题', trigger: 'blur' },
        { max: 255, message: '标题长度不能超过255个字符', trigger: 'blur' }
      ],
      name: [
        { required: true, message: '请输入唯一标识', trigger: 'blur' },
        { max: 255, message: '唯一标识长度不能超过255个字符', trigger: 'blur' },
        { pattern: /^[a-zA-Z][a-zA-Z0-9_]*$/, message: '唯一标识必须以字母开头，只能包含字母、数字和下划线', trigger: 'blur' }
      ],
      type: [
        { required: true, message: '请选择Prompt类型', trigger: 'change' }
      ],
      model: [
        { required: true, message: '请输入模型名称', trigger: 'blur' },
        { max: 255, message: '模型名称长度不能超过255个字符', trigger: 'blur' }
      ],
      ai_provider: [
        { required: true, message: '请选择AI提供商', trigger: 'change' }
      ],
      return_type: [
        { required: true, message: '请选择返回类型', trigger: 'change' }
      ],
      format_type: [
        { required: true, message: '请选择格式化类型', trigger: 'change' }
      ],
      template: [
        { required: true, message: '请输入模板内容', trigger: 'blur' }
      ]
    }

    // 加载数据
    const loadData = async () => {
      if (!isEdit.value) return

      loading.value = true
      try {
        const data = await promptApi.getPrompt(promptId.value)
        Object.assign(form, new Prompt(data))
        

        // 处理Mock数据：确保 form.mock_data 是字符串或空字符串
        if (form.mock_data === null || form.mock_data === undefined) {
          form.mock_data = ''
        } else if (typeof form.mock_data !== 'string') {
          form.mock_data = JSON.stringify(form.mock_data, null, 2)
        }
      } catch (error) {
        ElMessage.error('加载数据失败: ' + error.message)
        router.push('/prompts')
      } finally {
        loading.value = false
      }
    }



    // 验证Mock数据（仅在返回类型为 json 时进行校验）
    const validateMockData = () => {
      mockDataError.value = ''

      if (!form.mock) return
  // only validate when return_type is json_object
  if (form.return_type !== 'json_object') return

      const text = (form.mock_data || '').toString()
      if (!text.trim()) {
        // empty is allowed
        return
      }

      try {
        JSON.parse(text)
      } catch (error) {
        mockDataError.value = 'Mock数据格式错误，请输入有效的JSON格式'
      }
    }

    // 保存
    const handleSave = async () => {
      try {
        await formRef.value.validate()
        
        // 验证Mock数据（仅在 return_type === 'json_object' 时校验）
        if (form.mock && form.return_type === 'json_object') {
          validateMockData()
          if (mockDataError.value) return
        }

        saving.value = true
        
        const submitData = { ...form }

        if (isEdit.value) {
          await promptApi.updatePrompt(promptId.value, submitData)
          ElMessage.success('更新成功')
        } else {
          await promptApi.createPrompt(submitData)
          ElMessage.success('创建成功')
          router.push('/prompts')
        }
      } catch (error) {
        if (error.message) {
          ElMessage.error('保存失败: ' + error.message)
        }
      } finally {
        saving.value = false
      }
    }

    // 发布
    const handlePublish = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要发布Prompt "${form.title || form.name}" 吗？发布后版本号将+1。`,
          '确认发布',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        publishing.value = true
        await promptApi.publishPrompt(promptId.value)
        ElMessage.success('发布成功')
        
        // 发布完成后跳转回首页，避免二次发布
        router.push('/prompts')
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('发布失败: ' + error.message)
        }
      } finally {
        publishing.value = false
      }
    }

    // 保存并发布
    const handleSaveAndPublish = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要保存并发布Prompt "${form.title || form.name}" 吗？保存后将立即发布，版本号将+1。`,
          '确认保存并发布',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        // 先验证表单
        await formRef.value.validate()
        
        // 验证Mock数据（仅在 return_type === 'json_object' 时校验）
        if (form.mock && form.return_type === 'json_object') {
          validateMockData()
          if (mockDataError.value) return
        }

        saving.value = true
        publishing.value = true
        
        const submitData = { ...form }

        // 先保存
        if (isEdit.value) {
          await promptApi.updatePrompt(promptId.value, submitData)
        } else {
          await promptApi.createPrompt(submitData)
        }

        // 保存成功后发布
        await promptApi.publishPrompt(promptId.value)
        ElMessage.success('保存并发布成功')
        
        // 跳转回首页
        router.push('/prompts')
      } catch (error) {
        if (error !== 'cancel') {
          if (error.message) {
            ElMessage.error('保存并发布失败: ' + error.message)
          }
        }
      } finally {
        saving.value = false
        publishing.value = false
      }
    }

    // 在AI助手中打开测试
    const openInAIAssistant = () => {
      // 将当前的配置信息存储到localStorage，供AI助手页面使用
      const configData = {
        model: form.model,
        aiProvider: form.ai_provider,
        template: form.template,
        formatType: form.format_type,
        type: form.type,
        returnType: form.return_type,
        urls: form.urls || [],
        timestamp: Date.now()
      }
      localStorage.setItem('ai-assistant-config', JSON.stringify(configData))
      
      // 在新标签页打开AI助手
      const routeData = router.resolve({ name: 'AIAssistant' })
      window.open(routeData.href, '_blank')
      
      ElMessage.success('已在新标签页打开AI助手')
    }

    // 返回
    const handleBack = () => {
      router.push('/prompts')
    }

    onMounted(() => {
      loadData()
    })

    return {
      formRef,
      form,
      saving,
      publishing,
      loading,
      isEdit,
      mockDataText,
      mockDataError,
      showPreviewDialog,
      openInAIAssistant,
      aiProviderOptions,
      availableModels,
      formatTypeOptions,
      returnTypeOptions,
      typeOptions,
      rules,
      validateMockData,
      handleSave,
      handlePublish,
      handleSaveAndPublish,
      handleBack
    }
  }
}
</script>

<style scoped>
.prompt-edit {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}



.error-text {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 5px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-textarea__inner) {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  line-height: 1.6;
  font-size: 14px;
}

/* 专门为模板字段优化 */
:deep(.el-form-item:has([prop="template"]) .el-textarea__inner) {
  min-height: 200px;
  max-height: 500px;
  line-height: 1.8;
  font-size: 14px;
  padding: 16px;
  border-radius: 8px;
  border: 2px solid #e4e7ed;
  transition: border-color 0.2s ease;
}

:deep(.el-form-item:has([prop="template"]) .el-textarea__inner:focus) {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
}

:deep(.el-form-item:has([prop="template"]) .el-textarea__inner:hover) {
  border-color: #c0c4cc;
}

.template-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 8px;
}
</style>