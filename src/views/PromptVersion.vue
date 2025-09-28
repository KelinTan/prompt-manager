<template>
  <div class="prompt-version">
    <div class="page-header">
      <h2>{{ promptData?.title || promptData?.name }} - 版本 {{ version }}</h2>
      <div class="header-actions">
        <el-button @click="handleBack">返回历史</el-button>
        <el-button 
          v-if="!isCurrentVersion"
          type="warning" 
          @click="handleRestoreVersion"
        >
          恢复此版本
        </el-button>
      </div>
    </div>

    <el-card v-loading="loading" shadow="never">
      <div v-if="promptData" class="version-content">
        <!-- 版本信息 -->
        <div class="version-info">
          <el-descriptions :column="3" border>
            <el-descriptions-item label="版本号">
              <el-tag :type="isCurrentVersion ? 'success' : 'info'">
                版本 {{ version }}
                <span v-if="isCurrentVersion">(当前版本)</span>
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ formatDate(promptData.created_at) }}</el-descriptions-item>
            <el-descriptions-item label="更新时间">{{ formatDate(promptData.updated_at) }}</el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 基本信息 -->
        <div class="basic-info">
          <h3>基本信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="标题">{{ promptData.title }}</el-descriptions-item>
            <el-descriptions-item label="标识">{{ promptData.name }}</el-descriptions-item>
            <el-descriptions-item label="类型">{{ promptData.type || '-' }}</el-descriptions-item>
            <el-descriptions-item label="模型">{{ promptData.model || '-' }}</el-descriptions-item>
            <el-descriptions-item label="返回类型">{{ promptData.return_type || '-' }}</el-descriptions-item>
            <el-descriptions-item label="AI提供商">{{ promptData.ai_provider || '-' }}</el-descriptions-item>
            <el-descriptions-item label="格式类型">{{ getFormatTypeLabel(promptData.format_type) }}</el-descriptions-item>
            <el-descriptions-item label="Mock状态">
              <el-tag :type="promptData.mock ? 'success' : 'danger'" size="small">
                {{ promptData.mock ? '启用' : '禁用' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="备注">{{ promptData.remark || '-' }}</el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 模板内容 -->
        <div class="template-section">
          <h3>模板内容</h3>
          <div class="template-container">
            <div class="template-toolbar">
              <el-button 
                size="small" 
                @click="copyTemplate"
              >
                <el-icon><DocumentCopy /></el-icon>
                复制模板
              </el-button>
              <el-button 
                size="small" 
                @click="toggleFullscreen"
              >
                <el-icon><FullScreen /></el-icon>
                全屏查看
              </el-button>
            </div>
            <el-input
              v-model="promptData.template"
              type="textarea"
              :rows="12"
              readonly
              class="template-input"
            />
          </div>
        </div>

        <!-- 参数列表 -->


        <!-- Mock数据 -->
        <div v-if="promptData.mock && promptData.mock_data" class="mock-section">
          <h3>Mock 数据</h3>
          <div class="mock-container">
            <div class="mock-toolbar">
              <el-button 
                size="small" 
                @click="copyMockData"
              >
                <el-icon><DocumentCopy /></el-icon>
                复制Mock数据
              </el-button>
              <el-button 
                size="small" 
                @click="formatMockDataDisplay"
              >
                <el-icon><Edit /></el-icon>
                格式化
              </el-button>
            </div>
            <el-input
              v-model="mockDataDisplay"
              type="textarea"
              :rows="8"
              readonly
              class="mock-input"
            />
          </div>
        </div>
      </div>
    </el-card>

    <!-- 全屏模板查看对话框 -->
    <el-dialog
      v-model="fullscreenVisible"
      title="模板内容 - 全屏查看"
      width="95%"
      top="2vh"
      :close-on-click-modal="false"
    >
      <el-input
        v-model="promptData.template"
        type="textarea"
        :rows="25"
        readonly
        style="font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { promptApi } from '@/api/prompt'
import { FORMAT_TYPE_OPTIONS } from '@/models/prompt'

export default {
  name: 'PromptVersion',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)
    const promptData = ref(null)
    const mockDataDisplay = ref('')
    const fullscreenVisible = ref(false)

    const promptId = route.params.id
    const version = route.params.version

    // 是否为当前版本
    const isCurrentVersion = computed(() => {
      return promptData.value && promptData.value.version == version
    })

    // 获取格式类型标签
    const getFormatTypeLabel = (value) => {
      const option = FORMAT_TYPE_OPTIONS.find(item => item.value === value)
      return option ? option.label : value
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString('zh-CN')
    }

    // 加载版本数据
    const loadVersionData = async () => {
      loading.value = true
      try {
        const data = await promptApi.getPromptVersion(promptId, version)
        promptData.value = data
        


        // 处理Mock数据显示
        if (promptData.value.mock_data) {
          mockDataDisplay.value = typeof promptData.value.mock_data === 'string' 
            ? promptData.value.mock_data 
            : JSON.stringify(promptData.value.mock_data, null, 2)
        }
      } catch (error) {
        ElMessage.error('加载版本数据失败: ' + error.message)
        router.push(`/prompts/${promptId}/history`)
      } finally {
        loading.value = false
      }
    }

    // 复制模板
    const copyTemplate = async () => {
      try {
        await navigator.clipboard.writeText(promptData.value.template)
        ElMessage.success('模板内容已复制到剪贴板')
      } catch (error) {
        ElMessage.error('复制失败，请手动复制')
      }
    }

    // 复制Mock数据
    const copyMockData = async () => {
      try {
        await navigator.clipboard.writeText(mockDataDisplay.value)
        ElMessage.success('Mock数据已复制到剪贴板')
      } catch (error) {
        ElMessage.error('复制失败，请手动复制')
      }
    }

    // 格式化Mock数据显示
    const formatMockDataDisplay = () => {
      try {
        const parsed = JSON.parse(mockDataDisplay.value)
        mockDataDisplay.value = JSON.stringify(parsed, null, 2)
      } catch (error) {
        ElMessage.warning('Mock数据格式化失败，可能不是有效的JSON格式')
      }
    }

    // 切换全屏
    const toggleFullscreen = () => {
      fullscreenVisible.value = true
    }

    // 恢复版本
    const handleRestoreVersion = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要将版本 ${version} 恢复为当前版本吗？这将创建一个新的版本。`,
          '确认恢复版本',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        // 复制当前版本数据并更新
        const restoreData = { ...promptData.value }
        delete restoreData.id
        delete restoreData.version
        delete restoreData.created_at
        delete restoreData.updated_at

        await promptApi.updatePrompt(promptId, restoreData)
        ElMessage.success('版本恢复成功')
        
        // 跳转到编辑页面
        router.push(`/prompts/${promptId}/edit`)
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('恢复版本失败: ' + error.message)
        }
      }
    }

    // 返回历史页面
    const handleBack = () => {
      router.push(`/prompts/${promptId}/history`)
    }

    onMounted(() => {
      loadVersionData()
    })

    return {
      loading,
      promptData,
      version,
      isCurrentVersion,
      mockDataDisplay,
      fullscreenVisible,
      getFormatTypeLabel,
      formatDate,
      copyTemplate,
      copyMockData,
      formatMockDataDisplay,
      toggleFullscreen,
      handleRestoreVersion,
      handleBack
    }
  }
}
</script>

<style scoped>
.prompt-version {
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

.version-content > div {
  margin-bottom: 30px;
}

.version-content h3 {
  color: #303133;
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: 600;
}

.version-info {
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.template-container,
.mock-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.template-toolbar,
.mock-toolbar {
  background-color: #f5f7fa;
  padding: 10px 15px;
  border-bottom: 1px solid #dcdfe6;
  display: flex;
  gap: 10px;
}

.template-input,
.mock-input {
  border: none;
  border-radius: 0;
}

:deep(.template-input .el-textarea__inner),
:deep(.mock-input .el-textarea__inner) {
  border: none;
  border-radius: 0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.5;
  resize: none;
}

.mock-section :deep(.el-table) {
  font-size: 13px;
}

:deep(.el-descriptions__label) {
  font-weight: 500;
  width: 120px;
}

:deep(.el-dialog__body) {
  padding: 20px;
}
</style>