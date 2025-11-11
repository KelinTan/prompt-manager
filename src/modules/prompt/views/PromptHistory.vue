<template>
  <div class="prompt-history">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h2>{{ promptName }} - 历史版本</h2>
          <p class="version-note">显示最近 10 个版本记录</p>
        </div>
        <el-button @click="handleBack">返回列表</el-button>
      </div>
    </div>

    <el-card shadow="never">
      <div class="history-info">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="当前版本">{{ currentVersion }}</el-descriptions-item>
          <el-descriptions-item label="显示版本数">{{ historyList.length }} / 最近10个</el-descriptions-item>
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
            :type="version.is_latest ? 'primary' : 'info'"
            placement="top"
          >
            <el-card class="version-card" :class="{ 'current-version': version.is_latest }">
              <div class="version-header">
                <div class="version-info">
                  <h4>版本 {{ version.version }}</h4>
                  <div class="version-tags">
                    <el-tag 
                      v-if="version.is_latest" 
                      type="success" 
                      size="small"
                    >
                      当前版本
                    </el-tag>
                    <el-tag 
                      :type="getStatusInfo(version.status).type" 
                      size="small"
                      class="status-tag"
                    >
                      {{ getStatusInfo(version.status).label }}
                    </el-tag>
                  </div>
                </div>
                <div class="version-actions">
                  <el-button 
                    size="small" 
                    @click="handleViewVersion(version)"
                  >
                    查看详情
                  </el-button>
                  <el-button 
                    v-if="!version.is_latest"
                    size="small" 
                    type="warning"
                    @click="handleCompareVersion(version)"
                  >
                    与当前版本对比
                  </el-button>
                  <el-button 
                    v-if="!version.is_latest"
                    size="small" 
                    type="danger"
                    @click="handleRollback(version)"
                    :loading="rollbackingIds.has(version.id)"
                  >
                    回滚到此版本
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
                      <span class="meta-label">模版参数格式:</span>
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
          <el-descriptions-item label="状态">
            <el-tag 
              :type="getStatusInfo(selectedVersion.status).type" 
              size="small"
            >
              {{ getStatusInfo(selectedVersion.status).label }}
            </el-tag>
          </el-descriptions-item>
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
      :title="`版本对比: ${compareVersion?.version} vs 当前版本 ${currentVersion}`"
      width="90%"
      top="5vh"
    >
      <div v-if="compareVersion" class="version-compare">
        <div class="diff-section">
          <h4>模板差异对比</h4>
          <el-card>
            <div class="diff-content">
              <pre class="diff-display">
                <span
                  v-for="(part, index) in templateDiffs"
                  :key="index"
                  :class="{
                    'diff-added': part.added,
                    'diff-removed': part.removed,
                    'diff-unchanged': !part.added && !part.removed
                  }"
                >
                  {{ part.value }}
                </span>
              </pre>
            </div>
          </el-card>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { promptApi } from '@/modules/prompt/api/prompt'
import { FORMAT_TYPE_OPTIONS, PROMPT_STATUS_OPTIONS } from '@/modules/prompt/models/prompt'
import * as Diff from 'diff'

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
    const rollbackingIds = ref(new Set())
    const currentPromptId = ref(null)
    const templateDiffs = ref([])

    const promptId = route.params.id

    // 获取格式类型标签
    const getFormatTypeLabel = (value) => {
      const option = FORMAT_TYPE_OPTIONS.find(item => item.value === value)
      return option ? option.label : value
    }

    // 获取状态信息
    const getStatusInfo = (status) => {
      const statusMap = {
        draft: { label: '草稿', type: 'info', color: '#909399' },
        published: { label: '已发布', type: 'success', color: '#67c23a' },
        archived: { label: '已归档', type: 'warning', color: '#e6a23c' }
      }
      return statusMap[status] || { label: '草稿', type: 'info', color: '#909399' }
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
        // 清空之前的数据
        historyList.value = []
        
        // 获取当前prompt信息
        const currentPrompt = await promptApi.getPrompt(promptId)
        promptName.value = currentPrompt.title || currentPrompt.name
        currentVersion.value = currentPrompt.version || 1
        createdAt.value = currentPrompt.created_at
        updatedAt.value = currentPrompt.updated_at
        currentVersionData.value = currentPrompt
        currentPromptId.value = currentPrompt.id

        // 获取历史版本（最近10个版本）
        const historyResponse = await promptApi.getPromptHistory(promptId, { size: 10 })
        historyList.value = historyResponse.items || []
        
        // 按版本号降序排序，确保最新版本显示在前面
        historyList.value.sort((a, b) => b.version - a.version)
        
        // 从历史列表中找到当前版本（is_latest = true）
        if (historyList.value.length > 0) {
          const latestVersion = historyList.value.find(v => v.is_latest) || historyList.value[0]
          currentVersion.value = latestVersion.version
          currentPromptId.value = latestVersion.id
          // 更新当前版本的详细信息
          currentVersionData.value = latestVersion
        }
      } catch (error) {
        ElMessage.error('加载历史数据失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    // 查看版本详情
    const handleViewVersion = async (version) => {
      try {
        const versionData = await promptApi.getPrompt(version.id)
        selectedVersion.value = versionData
        versionDialogVisible.value = true
      } catch (error) {
        ElMessage.error('加载版本详情失败: ' + error.message)
      }
    }

    // 对比版本
    const handleCompareVersion = async (version) => {
      try {
        const versionData = await promptApi.getPrompt(version.id)
        compareVersion.value = versionData
        
        // 计算模板差异
        const oldTemplate = versionData.template || ''
        const newTemplate = currentVersionData.value?.template || ''
        templateDiffs.value = Diff.diffLines(oldTemplate, newTemplate)
        
        compareDialogVisible.value = true
      } catch (error) {
        ElMessage.error('加载版本数据失败: ' + error.message)
      }
    }

    // 回滚版本
    const handleRollback = async (version) => {
      try {
        await ElMessageBox.confirm(
          `确定要回滚到版本 ${version.version} 吗？这将会创建一个新的版本，内容与版本 ${version.version} 相同。`,
          '确认回滚',
          {
            confirmButtonText: '确定回滚',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        rollbackingIds.value.add(version.id)
        await promptApi.rollbackPrompt(promptId, { 
          target_version: version.version,
          target_id: version.id 
        })
        ElMessage.success('回滚成功')
        
        // 延迟一下确保后端数据已更新，然后重新加载历史数据
        setTimeout(async () => {
          await loadHistory()
        }, 500)
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('回滚失败: ' + error.message)
        }
      } finally {
        rollbackingIds.value.delete(version.id)
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
      rollbackingIds,
      currentPromptId,
      templateDiffs,
      getFormatTypeLabel,
      getStatusInfo,
      formatDate,
      formatMockData,
      handleViewVersion,
      handleCompareVersion,
      handleRollback,
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
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-section {
  flex: 1;
}

.page-header h2 {
  margin: 0 0 4px 0;
  color: #303133;
  font-size: 24px;
  font-weight: 700;
}

.version-note {
  margin: 0;
  color: #909399;
  font-size: 14px;
  font-style: italic;
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

.version-tags {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-tag {
  font-weight: 500;
}

.version-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.version-actions .el-button {
  font-size: 12px;
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

.version-detail .mock-section {
  margin-top: 20px;
}

.version-detail h4 {
  color: #303133;
  margin-bottom: 10px;
}

.diff-section {
  margin-top: 0;
}

.diff-section h4 {
  color: #303133;
  margin-bottom: 10px;
}

.diff-content {
  max-height: 500px;
  overflow-y: auto;
}

.diff-display {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 12px;
  line-height: 1.4;
  white-space: pre-wrap;
  word-break: break-all;
  margin: 0;
  padding: 15px;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
}

.diff-added {
  background-color: #d4edda;
  color: #155724;
  border-left: 3px solid #28a745;
  padding-left: 8px;
  margin-left: -3px;
  display: block;
}

.diff-removed {
  background-color: #f8d7da;
  color: #721c24;
  border-left: 3px solid #dc3545;
  padding-left: 8px;
  margin-left: -3px;
  text-decoration: line-through;
  display: block;
}

.diff-unchanged {
  color: #6c757d;
  display: block;
}
</style>