<template>
  <div class="task-list">
    <div class="page-header">
      <div class="header-container">
        <div class="header-left">
          <h1 class="page-title">任务列表</h1>
          <p class="page-subtitle">管理和监控 AIGC 任务（共 {{ total }} 个）</p>
        </div>
        
        <div class="header-center">
          <div class="filter-container">
            <el-select
              v-model="taskTypeFilter"
              placeholder="所有类型"
              clearable
              @change="handleSearch"
              class="filter-select"
            >
              <el-option
                v-for="type in taskTypes"
                :key="type"
                :label="type"
                :value="type"
              />
            </el-select>
            
            <el-select
              v-model="statusFilter"
              placeholder="所有状态"
              clearable
              @change="handleSearch"
              class="filter-select"
            >
              <el-option
                v-for="option in statusOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
            
            <el-select
              v-model.number="pageSize"
              @change="handleSearch"
              class="filter-select"
            >
              <el-option :value="10" label="10 / 页" />
              <el-option :value="20" label="20 / 页" />
              <el-option :value="50" label="50 / 页" />
            </el-select>
            
            <el-button @click="loadTasks" :loading="loading">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <div class="task-content">
      <el-card shadow="never" :body-style="{ padding: '0' }">
        <div v-if="loading && tasks.length === 0" class="loading-state">
          <el-icon class="is-loading"><Loading /></el-icon>
          <p>加载中...</p>
        </div>
        
        <div v-else-if="error" class="error-state">
          <el-icon><Warning /></el-icon>
          <p>{{ error }}</p>
          <el-button @click="loadTasks">重试</el-button>
        </div>
        
        <div v-else-if="tasks.length === 0" class="empty-state">
          <el-empty description="暂无任务" />
        </div>
        
        <div v-else class="table-container">
          <table class="task-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>UUID</th>
                <th>类型</th>
                <th>状态</th>
                <th>重试次数</th>
                <th>耗时</th>
                <th>创建时间</th>
                <th>更新时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in tasks" :key="task.id" class="task-row">
                <td>{{ task.id }}</td>
                <td>
                  <code class="uuid-text">{{ task.uuid }}</code>
                </td>
                <td>
                  <el-tag size="small" type="info">{{ task.task_type }}</el-tag>
                </td>
                <td>
                  <el-tag 
                    size="small" 
                    :type="getStatusInfo(task.status).type"
                  >
                    {{ getStatusInfo(task.status).label }}
                  </el-tag>
                </td>
                <td>{{ task.retry_count }}</td>
                <td>{{ formatDuration(task.cost_time) }}</td>
                <td>
                  <span class="time-text">{{ formatDate(task.created_at) }}</span>
                </td>
                <td>
                  <span class="time-text">{{ formatDate(task.updated_at) }}</span>
                </td>
                <td>
                  <div class="action-buttons">
                    <el-button 
                      size="small" 
                      @click="handleViewTask(task)"
                    >
                      查看
                    </el-button>
                    <el-button 
                      size="small" 
                      type="warning"
                      @click="handleRetryTask(task)"
                      :loading="retrying && selectedTaskId === task.id"
                    >
                      重试
                    </el-button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-if="tasks.length > 0" class="table-footer">
          <div class="footer-info">
            第 {{ page }} 页，共 {{ totalPages }} 页（总计 {{ total }} 条）
          </div>
          <div class="footer-pagination">
            <el-button 
              size="small"
              @click="prevPage" 
              :disabled="page === 1"
            >
              上一页
            </el-button>
            <span class="page-info">{{ page }} / {{ totalPages }}</span>
            <el-button 
              size="small"
              @click="nextPage" 
              :disabled="page === totalPages"
            >
              下一页
            </el-button>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 任务详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="`任务详情 #${selectedTask?.id}`"
      width="60%"
      top="5vh"
    >
      <div v-if="selectedTask" class="task-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ selectedTask.id }}</el-descriptions-item>
          <el-descriptions-item label="UUID">
            <code>{{ selectedTask.uuid }}</code>
          </el-descriptions-item>
          <el-descriptions-item label="类型">{{ selectedTask.task_type }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusInfo(selectedTask.status).type">
              {{ getStatusInfo(selectedTask.status).label }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="重试次数">{{ selectedTask.retry_count }}</el-descriptions-item>
          <el-descriptions-item label="耗时">{{ formatDuration(selectedTask.cost_time) }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(selectedTask.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ formatDate(selectedTask.updated_at) }}</el-descriptions-item>
        </el-descriptions>

        <div class="detail-section">
          <h4>任务参数</h4>
          <pre class="json-display">{{ formatJson(selectedTask.params) }}</pre>
        </div>

        <div class="detail-section">
          <h4>执行结果</h4>
          <pre class="json-display">{{ formatJson(selectedTask.result) }}</pre>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { taskApi } from '../api/task'
import { 
  TASK_STATUS_OPTIONS, 
  getStatusInfo, 
  formatDuration, 
  formatDate, 
  formatJson 
} from '../models/task'
import { Refresh, Loading, Warning } from '@element-plus/icons-vue'

export default {
  name: 'TaskList',
  components: {
    Refresh,
    Loading,
    Warning
  },
  setup() {
    const loading = ref(false)
    const error = ref(null)
    const tasks = ref([])
    const taskTypes = ref([])
    const total = ref(0)
    const page = ref(1)
    const pageSize = ref(20)
    const taskTypeFilter = ref('')
    const statusFilter = ref('')
    const detailDialogVisible = ref(false)
    const selectedTask = ref(null)
    const retrying = ref(false)
    const selectedTaskId = ref(null)
    
    const statusOptions = TASK_STATUS_OPTIONS
    
    const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))
    
    // 加载任务类型列表
    const loadTaskTypes = async () => {
      try {
        taskTypes.value = await taskApi.getTaskTypes()
      } catch (e) {
        console.error('加载任务类型失败:', e)
      }
    }
    
    // 加载任务列表
    const loadTasks = async () => {
      loading.value = true
      error.value = null
      try {
        const params = {
          page: page.value,
          size: pageSize.value
        }
        if (taskTypeFilter.value) params.task_type = taskTypeFilter.value
        if (statusFilter.value) params.status = statusFilter.value
        
        const data = await taskApi.getTasks(params)
        tasks.value = data.items || []
        total.value = data.total || 0
      } catch (e) {
        console.error('加载任务列表失败:', e)
        error.value = e.message || '加载失败'
      } finally {
        loading.value = false
      }
    }
    
    // 搜索
    const handleSearch = () => {
      page.value = 1
      loadTasks()
    }
    
    // 上一页
    const prevPage = () => {
      if (page.value > 1) {
        page.value--
        loadTasks()
      }
    }
    
    // 下一页
    const nextPage = () => {
      if (page.value < totalPages.value) {
        page.value++
        loadTasks()
      }
    }
    
    // 查看任务详情
    const handleViewTask = (task) => {
      selectedTask.value = task
      detailDialogVisible.value = true
    }
    
    // 重试任务
    const handleRetryTask = async (task) => {
      try {
        await ElMessageBox.confirm(
          `确定要重试任务 #${task.id} (${task.uuid}) 吗？`,
          '确认重试',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        retrying.value = true
        selectedTaskId.value = task.id
        await taskApi.retryTask(task.uuid)
        ElMessage.success('任务已重新提交')
        await loadTasks()
      } catch (e) {
        if (e !== 'cancel') {
          ElMessage.error('重试失败: ' + (e.message || e))
        }
      } finally {
        retrying.value = false
        selectedTaskId.value = null
      }
    }
    
    onMounted(() => {
      loadTaskTypes()
      loadTasks()
    })
    
    return {
      loading,
      error,
      tasks,
      taskTypes,
      total,
      page,
      pageSize,
      taskTypeFilter,
      statusFilter,
      statusOptions,
      totalPages,
      detailDialogVisible,
      selectedTask,
      retrying,
      selectedTaskId,
      getStatusInfo,
      formatDuration,
      formatDate,
      formatJson,
      loadTasks,
      handleSearch,
      prevPage,
      nextPage,
      handleViewTask,
      handleRetryTask
    }
  }
}
</script>

<style scoped>
.task-list {
  max-width: none;
  width: 100%;
}

.page-header {
  margin-bottom: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  padding: 20px;
}

.header-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-left {
  flex: 0 0 auto;
}

.page-title {
  margin: 0 0 4px 0;
  font-size: 24px;
  font-weight: 700;
  color: #303133;
}

.page-subtitle {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.filter-container {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-select {
  width: 150px;
}

.task-content {
  width: 100%;
}

.loading-state,
.error-state,
.empty-state {
  padding: 60px 20px;
  text-align: center;
  color: #909399;
}

.loading-state .el-icon,
.error-state .el-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.loading-state p,
.error-state p {
  margin: 0 0 16px 0;
  font-size: 14px;
}

.table-container {
  overflow-x: auto;
}

.task-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.task-table thead {
  background-color: #f5f7fa;
}

.task-table th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #303133;
  border-bottom: 1px solid #ebeef5;
}

.task-table tbody tr {
  border-bottom: 1px solid #ebeef5;
  transition: background-color 0.2s;
}

.task-table tbody tr:hover {
  background-color: #f5f7fa;
}

.task-table td {
  padding: 12px 16px;
  color: #606266;
}

.uuid-text {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 12px;
  background-color: #f5f7fa;
  padding: 2px 6px;
  border-radius: 4px;
}

.time-text {
  font-size: 12px;
  color: #909399;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.table-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background-color: #f5f7fa;
  border-top: 1px solid #ebeef5;
}

.footer-info {
  font-size: 14px;
  color: #606266;
}

.footer-pagination {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-info {
  font-size: 14px;
  color: #606266;
  min-width: 60px;
  text-align: center;
}

.task-detail {
  margin-top: 20px;
}

.detail-section {
  margin-top: 24px;
}

.detail-section h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.json-display {
  background-color: #1e1e1e;
  color: #d4d4d4;
  padding: 16px;
  border-radius: 8px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 12px;
  line-height: 1.6;
  max-height: 400px;
  overflow-y: auto;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
}

:deep(.el-card) {
  border-radius: 12px;
}

:deep(.el-descriptions__label) {
  font-weight: 600;
}
</style>
