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
            <el-form-item label="唯一标识" prop="name">
              <el-input 
                v-model="form.name" 
                placeholder="请输入唯一标识（如：user_profile_prompt）"
                maxlength="255"
                show-word-limit
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="类型" prop="type">
              <el-input 
                v-model="form.type" 
                placeholder="请输入类型"
                maxlength="255"
                show-word-limit
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <!-- 占位列 -->
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="模型" prop="model">
              <el-input 
                v-model="form.model" 
                placeholder="请输入模型名称"
                maxlength="255"
                show-word-limit
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="返回类型" prop="return_type">
              <el-select 
                v-model="form.return_type" 
                placeholder="请选择返回类型"
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
            <el-form-item label="格式类型" prop="format_type">
              <el-select 
                v-model="form.format_type" 
                placeholder="请选择格式类型"
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
        </el-row>

        <el-form-item label="模板" prop="template">
          <el-input 
            v-model="form.template" 
            type="textarea" 
            :rows="8"
            placeholder="请输入Prompt模板内容"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="参数">
          <div class="parameters-container">
            <div class="parameters-header">
              <span>参数列表</span>
              <el-button 
                type="primary" 
                size="small" 
                @click="addParameter"
              >
                <el-icon><Plus /></el-icon>
                添加参数
              </el-button>
            </div>
            <div v-if="form.parameters.length === 0" class="empty-parameters">
              暂无参数，点击上方按钮添加
            </div>
            <div v-else class="parameters-list">
              <div 
                v-for="(param, index) in form.parameters" 
                :key="index"
                class="parameter-item"
              >
                <el-input 
                  v-model="param.name" 
                  placeholder="参数名"
                  style="width: 200px; margin-right: 10px;"
                />
                <el-input 
                  v-model="param.type" 
                  placeholder="参数类型"
                  style="width: 150px; margin-right: 10px;"
                />
                <el-input 
                  v-model="param.description" 
                  placeholder="参数描述"
                  style="width: 300px; margin-right: 10px;"
                />
                <el-button 
                  type="danger" 
                  size="small" 
                  @click="removeParameter(index)"
                >
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </el-form-item>

        <el-row :gutter="20">
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

        <el-form-item v-if="form.mock" label="Mock数据">
          <el-input 
            v-model="mockDataString" 
            type="textarea" 
            :rows="4"
            placeholder="请输入Mock数据 (JSON格式)"
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
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { promptApi } from '@/api/prompt'
import { Prompt, AI_PROVIDER_OPTIONS, FORMAT_TYPE_OPTIONS, RETURN_TYPE_OPTIONS } from '@/models/prompt'

export default {
  name: 'PromptEdit',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const formRef = ref()
    const saving = ref(false)
    const publishing = ref(false)
    const loading = ref(false)
    const mockDataError = ref('')

    // 是否为编辑模式
    const isEdit = computed(() => !!route.params.id)
    const promptId = computed(() => route.params.id)

    // 表单数据
    const form = reactive(new Prompt())

    // Mock数据字符串（用于界面显示和编辑）
    const mockDataString = ref('')

    // 选项数据
    const aiProviderOptions = AI_PROVIDER_OPTIONS
    const formatTypeOptions = FORMAT_TYPE_OPTIONS
    const returnTypeOptions = RETURN_TYPE_OPTIONS

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
        
        // 处理参数数据
        if (form.parameters && typeof form.parameters === 'string') {
          form.parameters = JSON.parse(form.parameters)
        }
        if (!Array.isArray(form.parameters)) {
          form.parameters = []
        }

        // 处理Mock数据
        if (form.mock_data) {
          mockDataString.value = typeof form.mock_data === 'string' 
            ? form.mock_data 
            : JSON.stringify(form.mock_data, null, 2)
        }
      } catch (error) {
        ElMessage.error('加载数据失败: ' + error.message)
        router.push('/prompts')
      } finally {
        loading.value = false
      }
    }

    // 添加参数
    const addParameter = () => {
      form.parameters.push({
        name: '',
        type: '',
        description: ''
      })
    }

    // 删除参数
    const removeParameter = (index) => {
      form.parameters.splice(index, 1)
    }

    // 验证Mock数据
    const validateMockData = () => {
      mockDataError.value = ''
      if (!mockDataString.value.trim()) {
        form.mock_data = {}
        return
      }

      try {
        form.mock_data = JSON.parse(mockDataString.value)
      } catch (error) {
        mockDataError.value = 'Mock数据格式错误，请输入有效的JSON格式'
      }
    }

    // 保存
    const handleSave = async () => {
      try {
        await formRef.value.validate()
        
        // 验证Mock数据
        if (form.mock && mockDataString.value.trim()) {
          validateMockData()
          if (mockDataError.value) {
            return
          }
        }

        saving.value = true
        
        const submitData = { ...form }
        
        // 处理参数数据
        if (submitData.parameters && submitData.parameters.length > 0) {
          // 过滤空参数
          submitData.parameters = submitData.parameters.filter(p => p.name.trim())
        }

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
        
        // 重新加载数据
        await loadData()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('发布失败: ' + error.message)
        }
      } finally {
        publishing.value = false
      }
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
      mockDataString,
      mockDataError,
      aiProviderOptions,
      formatTypeOptions,
      returnTypeOptions,
      rules,
      addParameter,
      removeParameter,
      validateMockData,
      handleSave,
      handlePublish,
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

.parameters-container {
  width: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 15px;
  background-color: #fafafa;
}

.parameters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  font-weight: 500;
}

.empty-parameters {
  text-align: center;
  color: #909399;
  padding: 20px;
}

.parameters-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.parameter-item {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: white;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
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
}
</style>