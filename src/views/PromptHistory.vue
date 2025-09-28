<template>
  <div class="prompt-history">
    <div class="page-header">
      <h2>{{ promptName }} - 历史版本</h2>
      <el-button @click="handleBack">返回列表</el-button>
    </div>

    <el-card shadow="never">
      <div class="history-info">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="当前版本">{{ currentVersion }}</el-descriptions-item>
          <el-descriptions-item label="总版本数">{{ historyList.length }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(createdAt) }}</el-descriptions-item>
          <el-descriptions-item label="最后更新">{{ formatDate(updatedAt) }}</el-descriptions-item>
        </el-descriptions>
      </div>

      <div class="history-list">
        <h3>版本历史</h3>
        <el-timeline>
          <el-timeline-item
            v-for="version in historyList"
            :key="version.version"
            :timestamp="formatDate(version.created_at)"
            :type="version.version === currentVersion ? 'primary' : 'info'"
            placement="top"
          >
            <el-card class="version-card" :class="{ 'current-version': version.version === currentVersion }">
              <div class="version-header">
                <div class="version-info">
                  <h4>版本 {{ version.version }}</h4>
                  <el-tag 
                    v-if="version.version === currentVersion" 
                    type="success" 
                    size="small"
                  >
                    当前版本
                  </el-tag>
                </div>
                <div class="version-actions">
                  <el-button 
                    size="small" 
                    @click="handleViewVersion(version)"
                  >
                    查看详情
                  </el-button>
                  <el-button 
                    v-if="version.version !== currentVersion"
                    size="small" 
                    type="warning"
                    @click="handleCompareVersion(version)"
                  >
                    与当前版本对比
                  </el-button>
                </div>
              </div>
              
              <div class="version-content">
                <div class="version-changes">
                  <p><strong>模板预览:</strong></p>
                  <div class="template-preview">
                    {{ version.template.substring(0, 200) }}{{ version.template.length > 200 ? '...' : '' }}
                  </div>
                </div>
                
                <div class="version-meta">
                  <el-row :gutter="20">
                    <el-col :span="6">
                      <span class="meta-label">类型:</span>
                      <span>{{ version.type || '-' }}</span>
                    </el-col>
                    <el-col :span="6">
                      <span class="meta-label">模型:</span>
                      <span>{{ version.model || '-' }}</span>
                    </el-col>
                    <el-col :span="6">
                      <span class="meta-label">AI提供商:</span>
                      <span>{{ version.ai_provider || '-' }}</span>
                    </el-col>
                    <el-col :span="6">
                      <span class="meta-label">格式:</span>
                      <span>{{ getFormatTypeLabel(version.format_type) }}</span>
                    </el-col>
                  </el-row>
                </div>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-card>

    <!-- 版本详情对话框 -->
    <el-dialog
      v-model="versionDialogVisible"
      :title="`版本 ${selectedVersion?.version} 详情`"
      width="80%"
      top="5vh"
    >
      <div v-if="selectedVersion" class="version-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="版本号">{{ selectedVersion.version }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(selectedVersion.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="标题">{{ selectedVersion.title }}</el-descriptions-item>
          <el-descriptions-item label="标识">{{ selectedVersion.name }}</el-descriptions-item>
          <el-descriptions-item label="类型">{{ selectedVersion.type || '-' }}</el-descriptions-item>
          <el-descriptions-item label="模型">{{ selectedVersion.model || '-' }}</el-descriptions-item>
          <el-descriptions-item label="返回类型">{{ selectedVersion.return_type || '-' }}</el-descriptions-item>
          <el-descriptions-item label="AI提供商">{{ selectedVersion.ai_provider || '-' }}</el-descriptions-item>
          <el-descriptions-item label="格式类型">{{ getFormatTypeLabel(selectedVersion.format_type) }}</el-descriptions-item>
          <el-descriptions-item label="Mock">{{ selectedVersion.mock ? '启用' : '禁用' }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ selectedVersion.remark || '-' }}</el-descriptions-item>
        </el-descriptions>

        <div class="template-section">
          <h4>模板内容</h4>
          <el-input
            :model-value="selectedVersion.template"
            type="textarea"
            :rows="10"
            readonly
          />
        </div>

        <div v-if="selectedVersion.parameters && selectedVersion.parameters.length > 0" class="parameters-section">
          <h4>参数列表</h4>
          <el-table :data="selectedVersion.parameters" border>
            <el-table-column prop="name" label="参数名" width="150" />
            <el-table-column prop="type" label="类型" width="120" />
            <el-table-column prop="description" label="描述" />
          </el-table>
        </div>

        <div v-if="selectedVersion.mock && selectedVersion.mock_data" class="mock-section">
          <h4>Mock 数据</h4>
          <el-input
            :model-value="formatMockData(selectedVersion.mock_data)"
            type="textarea"
            :rows="6"
            readonly
          />
        </div>
      </div>
    </el-dialog>

    <!-- 版本对比对话框 -->
    <el-dialog
      v-model="compareDialogVisible"
      title="版本对比"
      width="90%"
      top="5vh"
    >
      <div v-if="compareVersion" class="version-compare">
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="compare-section">
              <h4>版本 {{ compareVersion.version }}</h4>
              <el-card>
                <div class="compare-content">
                  <p><strong>模板:</strong></p>
                  <el-input
                    :model-value="compareVersion.template"
                    type="textarea"
                    :rows="8"
                    readonly
                  />
                </div>
              </el-card>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="compare-section">
              <h4>当前版本 {{ currentVersion }}</h4>
              <el-card>
                <div class="compare-content">
                  <p><strong>模板:</strong></p>
                  <el-input
                    :model-value="currentVersionData?.template || ''"
                    type="textarea"
                    :rows="8"
                    readonly
                  />
                </div>
              </el-card>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { promptApi } from '@/api/prompt'
import { FORMAT_TYPE_OPTIONS } from '@/models/prompt'

export default {
  name: 'PromptHistory',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)
    const historyList = ref([])
    const promptName = ref('')
    const currentVersion = ref(1)
    const createdAt = ref('')
    const updatedAt = ref('')
    
    // 对话框状态
    const versionDialogVisible = ref(false)
    const compareDialogVisible = ref(false)
    const selectedVersion = ref(null)
    const compareVersion = ref(null)
    const currentVersionData = ref(null)

    const promptId = route.params.id

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

    // 格式化Mock数据
    const formatMockData = (data) => {
      if (!data) return ''
      return typeof data === 'string' ? data : JSON.stringify(data, null, 2)
    }

    // 加载历史数据
    const loadHistory = async () => {
      loading.value = true
      try {
        // 获取当前prompt信息
        const currentPrompt = await promptApi.getPrompt(promptId)
        promptName.value = currentPrompt.title || currentPrompt.name
        currentVersion.value = currentPrompt.version || 1
        createdAt.value = currentPrompt.created_at
        updatedAt.value = currentPrompt.updated_at
        currentVersionData.value = currentPrompt

        // 获取历史版本
        const historyResponse = await promptApi.getPromptHistory(promptId)
        historyList.value = historyResponse.items || []
        
        // 按版本号降序排序
        historyList.value.sort((a, b) => b.version - a.version)
      } catch (error) {
        ElMessage.error('加载历史数据失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    // 查看版本详情
    const handleViewVersion = async (version) => {
      try {
        const versionData = await promptApi.getPromptVersion(promptId, version.version)
        selectedVersion.value = versionData
        versionDialogVisible.value = true
      } catch (error) {
        ElMessage.error('加载版本详情失败: ' + error.message)
      }
    }

    // 对比版本
    const handleCompareVersion = async (version) => {
      try {
        const versionData = await promptApi.getPromptVersion(promptId, version.version)
        compareVersion.value = versionData
        compareDialogVisible.value = true
      } catch (error) {
        ElMessage.error('加载版本数据失败: ' + error.message)
      }
    }

    // 返回
    const handleBack = () => {
      router.push('/prompts')
    }

    onMounted(() => {
      loadHistory()
    })

    return {
      loading,
      historyList,
      promptName,
      currentVersion,
      createdAt,
      updatedAt,
      versionDialogVisible,
      compareDialogVisible,
      selectedVersion,
      compareVersion,
      currentVersionData,
      getFormatTypeLabel,
      formatDate,
      formatMockData,
      handleViewVersion,
      handleCompareVersion,
      handleBack
    }
  }
}
</script>

<style scoped>
.prompt-history {
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

.history-info {
  margin-bottom: 30px;
}

.history-list h3 {
  color: #303133;
  margin-bottom: 20px;
}

.version-card {
  margin-bottom: 10px;
}

.version-card.current-version {
  border-color: #409EFF;
  box-shadow: 0 2px 12px 0 rgba(64, 158, 255, 0.1);
}

.version-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.version-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.version-info h4 {
  margin: 0;
  color: #303133;
}

.version-actions {
  display: flex;
  gap: 10px;
}

.version-content {
  margin-top: 15px;
}

.template-preview {
  background-color: #f5f5f5;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 10px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 12px;
  line-height: 1.4;
  color: #606266;
  white-space: pre-wrap;
  word-break: break-all;
}

.version-meta {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #ebeef5;
}

.meta-label {
  font-weight: 500;
  color: #909399;
  margin-right: 8px;
}

.version-detail .template-section,
.version-detail .parameters-section,
.version-detail .mock-section {
  margin-top: 20px;
}

.version-detail h4 {
  color: #303133;
  margin-bottom: 10px;
}

.compare-section h4 {
  color: #303133;
  margin-bottom: 10px;
  text-align: center;
}

.compare-content p {
  margin-bottom: 10px;
  font-weight: 500;
}

:deep(.el-timeline-item__timestamp) {
  font-size: 12px;
  color: #909399;
}

:deep(.el-descriptions__label) {
  font-weight: 500;
}

:deep(.el-textarea__inner) {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}
</style>