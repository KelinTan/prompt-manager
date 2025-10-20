<template>
  <div class="prompt-list">
    <!-- 优化后的页面头部 -->
    <div class="page-header">
      <div class="header-container">
        <!-- 左侧标题区域 -->
        <div class="header-left">
          <div class="title-section">
            <h1 class="page-title">Prompt 管理</h1>
            <p class="page-subtitle">管理和组织你的 AI Prompt 模板</p>
          </div>
        </div>
        
        <!-- 中间搜索区域 -->
        <div class="header-center">
          <div class="search-container">
            <div class="search-row">
              <el-input 
                v-model="searchForm.keyword" 
                placeholder="搜索名称或标题..."
                class="search-input"
                size="large"
                clearable
                @clear="handleSearch"
                @keyup.enter="handleSearch"
              >
                <template #prefix>
                  <el-icon class="search-icon"><Search /></el-icon>
                </template>
              </el-input>
              <el-select
                v-model="searchForm.ai_provider"
                placeholder="选择供应商"
                class="provider-select"
                size="large"
                clearable
                @change="handleSearch"
                @clear="handleSearch"
              >
                <el-option
                  v-for="option in aiProviderOptions"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                />
              </el-select>
              <el-select
                v-model="searchForm.enabled"
                placeholder="启用状态"
                class="enabled-select"
                size="large"
                clearable
                @change="handleSearch"
                @clear="handleSearch"
              >
                <el-option label="已启用" :value="true" />
                <el-option label="已禁用" :value="false" />
              </el-select>
              <el-button 
                size="large" 
                @click="handleReset"
                class="reset-btn"
              >
                重置
              </el-button>
            </div>
          </div>
        </div>
        
        <!-- 右侧操作区域 -->
        <div class="header-right">
          <div class="action-section">
            <el-button type="primary" size="large" class="create-btn" @click="$router.push('/prompts/create')">
              <el-icon><Plus /></el-icon>
              新建 Prompt
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 现代卡片网格布局 -->
    <div class="prompts-grid" v-loading="loading">
      <div v-if="prompts.length === 0" class="empty-state">
        <div class="empty-icon">
          <el-icon><Document /></el-icon>
        </div>
        <h3>暂无 Prompt</h3>
        <p>创建你的第一个 Prompt 模板</p>
        <el-button type="primary" @click="$router.push('/prompts/create')">
          <el-icon><Plus /></el-icon>
          创建 Prompt
        </el-button>
      </div>
      
      <div v-else class="cards-container">
        <div 
          v-for="prompt in prompts" 
          :key="prompt.id"
          class="prompt-card"
          @click="handleRowClick(prompt)"
        >
          <div class="card-header">
            <div class="card-title-section">
              <h3 class="card-title">{{ prompt.title || prompt.name }}</h3>
              <div class="card-subtitle">{{ prompt.name }}</div>
              <div class="card-meta">
                <span class="prompt-type">{{ prompt.type || '未分类' }}</span>
                <span 
                  class="version-badge"
                  :class="{ 'draft-version': prompt.status === 'draft', 'published-version': prompt.status === 'published' }"
                >
                  {{ getVersionLabel(prompt) }}
                </span>
                <span class="meta-divider">•</span>
                <span 
                  class="enabled-indicator"
                  :class="{ 'is-enabled': prompt.enabled, 'is-disabled': !prompt.enabled }"
                >
                  {{ prompt.enabled ? '已启用' : '已禁用' }}
                </span>
              </div>
            </div>
            <div class="card-status">
              <el-tag 
                :type="getStatusInfo(prompt.status).type" 
                size="small"
                class="status-tag"
              >
                {{ getStatusInfo(prompt.status).label }}
              </el-tag>
            </div>
          </div>
          
          <div class="card-content">
            <p class="template-preview">
              {{ prompt.template ? prompt.template.substring(0, 120) + (prompt.template.length > 120 ? '...' : '') : '暂无模板内容' }}
            </p>
            
            <div class="card-tags">
              <el-tag v-if="prompt.ai_provider" size="small" class="provider-tag">
                {{ prompt.ai_provider }}
              </el-tag>
              <el-tag v-if="prompt.model" size="small" type="info" class="model-tag">
                {{ prompt.model }}
              </el-tag>
              <el-tag v-if="prompt.return_type" size="small" type="warning" class="return-type-tag">
                {{ prompt.return_type }}
              </el-tag>
            </div>
          </div>
          
          <div class="card-footer">
            <div class="card-info">
              <span class="created-time">{{ formatDate(prompt.created_at) }}</span>
            </div>
            <div class="card-actions" @click.stop>
              <el-button 
                size="small" 
                type="primary"
                link
                @click="handleEdit(prompt)"
              >
                <el-icon><Edit /></el-icon>
              </el-button>
              <el-tooltip v-if="prompt.status === 'published'" content="当前已发布，无法再次发布" placement="top">
                <el-button 
                  size="small" 
                  type="success"
                  link
                  disabled
                >
                  <el-icon><Upload /></el-icon>
                </el-button>
              </el-tooltip>
              <el-button 
                v-else
                size="small" 
                type="success"
                link
                @click="handlePublish(prompt)"
                :loading="publishingIds.has(prompt.id)"
              >
                <el-icon><Upload /></el-icon>
              </el-button>
              <el-button 
                size="small" 
                type="info"
                link
                @click="handleHistory(prompt)"
              >
                <el-icon><Clock /></el-icon>
              </el-button>
              <el-tooltip :content="prompt.enabled ? '禁用' : '启用'" placement="top">
                <el-button 
                  size="small" 
                  :type="prompt.enabled ? 'warning' : 'success'"
                  link
                  @click="handleToggleEnabled(prompt)"
                  :loading="togglingIds.has(prompt.id)"
                >
                  <el-icon>
                    <component :is="prompt.enabled ? 'CircleClose' : 'CircleCheck'" />
                  </el-icon>
                </el-button>
              </el-tooltip>
              <el-popconfirm
                title="确定要删除这个Prompt吗？"
                @confirm="handleDelete(prompt)"
              >
                <template #reference>
                  <el-button 
                    size="small" 
                    type="danger"
                    link
                  >
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </template>
              </el-popconfirm>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="prompts.length > 0" class="pagination-section">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.size"
        :page-sizes="[12, 24, 48]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        class="modern-pagination"
      />
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { promptApi } from '@/api/prompt'
import { FORMAT_TYPE_OPTIONS, PROMPT_STATUS_OPTIONS } from '@/models/prompt'
import { AI_PROVIDER_OPTIONS } from '@/config/ai'

const SEARCH_STORAGE_KEY = 'promptListSearchState'
const PAGINATION_STORAGE_KEY = 'promptListPaginationState'

export default {
  name: 'PromptList',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const prompts = ref([])
    const publishingIds = ref(new Set())
    const togglingIds = ref(new Set())

    // 从 sessionStorage 恢复搜索条件
    const savedSearchState = sessionStorage.getItem(SEARCH_STORAGE_KEY)
    const initialSearchState = savedSearchState ? JSON.parse(savedSearchState) : {
      keyword: '',
      ai_provider: '',
      enabled: undefined
    }

    // 从 sessionStorage 恢复分页状态
    const savedPaginationState = sessionStorage.getItem(PAGINATION_STORAGE_KEY)
    const initialPaginationState = savedPaginationState ? JSON.parse(savedPaginationState) : {
      page: 1,
      size: 12,
      total: 0
    }

    // 搜索表单
    const searchForm = reactive(initialSearchState)

    // 分页
    const pagination = reactive(initialPaginationState)

    // AI提供商选项
    const aiProviderOptions = AI_PROVIDER_OPTIONS

    // 获取格式类型标签
    const getFormatTypeLabel = (value) => {
      const option = FORMAT_TYPE_OPTIONS.find(item => item.value === value)
      return option ? option.label : value
    }

    // 获取状态标签和类型
    const getStatusInfo = (status) => {
      const statusMap = {
        draft: { label: '草稿', type: 'info' },
        published: { label: '已发布', type: 'success' }
      }
      return statusMap[status] || { label: '草稿', type: 'info' }
    }

    // 获取版本描述
    const getVersionLabel = (prompt) => {
      if (!prompt.version) return '初始版本'
      if (prompt.status === 'published') {
        return `第${prompt.version}版`
      } else {
        return `第${prompt.version}版·草稿`
      }
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString('zh-CN')
    }

    // 加载数据
    const loadData = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.page,
          size: pagination.size,
          ...searchForm
        }
        
        // 过滤空值
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })

        const response = await promptApi.getPrompts(params)
        prompts.value = response.items || []
        pagination.total = response.total || 0
      } catch (error) {
        ElMessage.error('加载数据失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.page = 1
      loadData()
    }

    // 重置搜索
    const handleReset = () => {
      searchForm.keyword = ''
      searchForm.ai_provider = ''
      searchForm.enabled = undefined
      pagination.page = 1
      // 清除存储的状态
      sessionStorage.removeItem(SEARCH_STORAGE_KEY)
      sessionStorage.removeItem(PAGINATION_STORAGE_KEY)
      handleSearch()
    }

    // 页面大小改变
    const handleSizeChange = (size) => {
      pagination.size = size
      loadData()
    }

    // 当前页改变
    const handleCurrentChange = (page) => {
      pagination.page = page
      loadData()
    }

    // 行点击
    const handleRowClick = (row) => {
      router.push(`/prompts/${row.id}/edit`)
    }

    // 编辑
    const handleEdit = (row) => {
      router.push(`/prompts/${row.id}/edit`)
    }

    // 发布
    const handlePublish = async (row) => {
      // 如果已经是已发布状态，不允许再次发布
      if (row.status === 'published') {
        ElMessage.info('该 Prompt 已是已发布状态，无法重复发布')
        return
      }
      try {
        await ElMessageBox.confirm(
          `确定要发布Prompt "${row.title || row.name}" 吗？发布后版本号将+1。`,
          '确认发布',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        publishingIds.value.add(row.id)
        await promptApi.publishPrompt(row.id)
        ElMessage.success('发布成功')
        loadData() // 重新加载数据
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('发布失败: ' + error.message)
        }
      } finally {
        publishingIds.value.delete(row.id)
      }
    }

    // 查看历史
    const handleHistory = (row) => {
      router.push(`/prompts/${row.id}/history`)
    }

    // 删除
    const handleDelete = async (row) => {
      try {
        await promptApi.deletePrompt(row.id)
        ElMessage.success('删除成功')
        loadData()
      } catch (error) {
        ElMessage.error('删除失败: ' + error.message)
      }
    }

    // 切换启用/禁用状态
    const handleToggleEnabled = async (row) => {
      const action = row.enabled ? '禁用' : '启用'
      try {
        await ElMessageBox.confirm(
          `确定要${action}Prompt "${row.title || row.name}" 吗？`,
          `确认${action}`,
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        togglingIds.value.add(row.id)
        // 根据当前状态调用不同的接口
        if (row.enabled) {
          await promptApi.disablePrompt(row.id)
        } else {
          await promptApi.enablePrompt(row.id)
        }
        ElMessage.success(`${action}成功`)
        loadData() // 重新加载数据
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error(`${action}失败: ` + error.message)
        }
      } finally {
        togglingIds.value.delete(row.id)
      }
    }

    // 监听搜索条件变化，保存到 sessionStorage
    watch(searchForm, (newVal) => {
      sessionStorage.setItem(SEARCH_STORAGE_KEY, JSON.stringify(newVal))
    }, { deep: true })

    // 监听分页状态变化，保存到 sessionStorage
    watch(pagination, (newVal) => {
      sessionStorage.setItem(PAGINATION_STORAGE_KEY, JSON.stringify(newVal))
    }, { deep: true })

    // 组件卸载前清理（可选，如果希望关闭标签页后清除状态）
    // onBeforeUnmount(() => {
    //   sessionStorage.removeItem(SEARCH_STORAGE_KEY)
    //   sessionStorage.removeItem(PAGINATION_STORAGE_KEY)
    // })

    onMounted(() => {
      loadData()
    })

    return {
      loading,
      prompts,
      searchForm,
      pagination,

      publishingIds,
      togglingIds,
      aiProviderOptions,
      getFormatTypeLabel,
      getStatusInfo,
      getVersionLabel,
      formatDate,
      handleSearch,
      handleReset,
      handleSizeChange,
      handleCurrentChange,
      handleRowClick,
      handleEdit,
      handlePublish,
      handleHistory,
      handleDelete,
      handleToggleEnabled
    }
  }
}
</script>

<style scoped>
.prompt-list {
  max-width: none;
  width: 100%;
}

/* 优化后的页面头部 */
.page-header {
  margin-bottom: var(--spacing-xl);
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

.header-container {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg) var(--spacing-xl);
}

/* 左侧标题区域 */
.header-left {
  display: flex;
  align-items: center;
}

.title-section {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 4px;
  letter-spacing: -0.025em;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.4;
}

/* 中间搜索区域 */
.header-center {
  display: flex;
  justify-content: center;
}

.search-container {
  width: 100%;
  max-width: 600px;
}

.search-row {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.search-input {
  flex: 2;
  min-width: 200px;
}

.search-input :deep(.el-input__wrapper) {
  background: #f5f7fa;
  box-shadow: 0 0 0 1px var(--border-color) inset;
  border-radius: var(--radius-lg);
  transition: all 0.2s ease;
  height: 40px;
}

.search-input :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--primary-light) inset;
}

.search-input :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--el-color-primary) inset;
  background: #ffffff;
}

.provider-select {
  flex: 1;
  min-width: 150px;
}

.provider-select :deep(.el-input__wrapper) {
  background: #f5f7fa;
  box-shadow: 0 0 0 1px var(--border-color) inset;
  border-radius: var(--radius-lg);
  height: 40px;
}

.provider-select :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--primary-light) inset;
}

.enabled-select {
  flex: 1;
  min-width: 120px;
}

.enabled-select :deep(.el-input__wrapper) {
  background: #f5f7fa;
  box-shadow: 0 0 0 1px var(--border-color) inset;
  border-radius: var(--radius-lg);
  height: 40px;
}

.enabled-select :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--primary-light) inset;
}

.reset-btn {
  flex-shrink: 0;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  border-radius: var(--radius-lg);
  transition: all 0.2s ease;
}

.reset-btn:hover {
  background: var(--bg-tertiary);
  border-color: var(--primary-light);
  color: var(--text-primary);
}

/* 右侧操作区域 */
.header-right {
  display: flex;
  justify-content: flex-end;
}

.action-section {
  display: flex;
  align-items: center;
}

.create-btn {
  background: var(--primary-gradient);
  border: none;
  border-radius: var(--radius-lg);
  padding: var(--spacing-sm) var(--spacing-lg);
  font-weight: 600;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
  font-size: 15px;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.create-btn:active {
  transform: translateY(0);
}





/* 搜索区域优化 */
:deep(.search-input .el-input__wrapper) {
  border-radius: var(--radius-xl);
  border: 2px solid var(--border-color);
  background: var(--bg-secondary);
  padding: 0 var(--spacing-md);
  height: 48px;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

:deep(.search-input .el-input__wrapper:hover) {
  border-color: var(--primary-color);
  background: var(--bg-primary);
  box-shadow: var(--shadow-md);
}

:deep(.search-input .el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  background: var(--bg-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  transform: translateY(-1px);
}

:deep(.search-input .el-input__inner) {
  border: none;
  background: transparent;
  box-shadow: none;
  font-size: 16px;
  color: var(--text-primary);
  height: 100%;
  line-height: 1.5;
}

:deep(.search-input .el-input__inner::placeholder) {
  color: var(--text-muted);
  font-size: 15px;
}

.search-icon {
  color: var(--text-secondary);
  font-size: 18px;
}

/* 供应商选择器样式 */
:deep(.provider-select .el-input__wrapper) {
  border-radius: var(--radius-xl);
  border: 2px solid var(--border-color);
  background: var(--bg-secondary);
  padding: 0 var(--spacing-md);
  height: 48px;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

:deep(.provider-select .el-input__wrapper:hover) {
  border-color: var(--primary-color);
  background: var(--bg-primary);
  box-shadow: var(--shadow-md);
}

:deep(.provider-select .el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  background: var(--bg-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  transform: translateY(-1px);
}

:deep(.provider-select .el-input__inner) {
  border: none;
  background: transparent;
  box-shadow: none;
  font-size: 16px;
  color: var(--text-primary);
  height: 100%;
  line-height: 1.5;
}

:deep(.provider-select .el-input__inner::placeholder) {
  color: var(--text-muted);
  font-size: 15px;
}



.filter-select {
  min-width: 140px;
}

:deep(.filter-select .el-input__inner) {
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  height: 36px;
}

.reset-btn {
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  color: var(--text-secondary);
}

/* 卡片网格布局 */
.prompts-grid {
  min-height: 400px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl);
  text-align: center;
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  border: 2px dashed var(--border-color);
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
  font-size: 64px;
  color: var(--text-muted);
}

.empty-state h3 {
  font-size: 20px;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-xs);
}

.empty-state p {
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-lg);
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: var(--spacing-lg);
}

.prompt-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-xl);
  padding: var(--spacing-lg);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}

.prompt-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
  border-color: var(--primary-light);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-md);
  gap: var(--spacing-sm);
}

.card-title-section {
  flex: 1;
  min-width: 0;
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 2px;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.card-subtitle {
  font-size: 12px;
  color: var(--text-muted);
  margin: 0 0 var(--spacing-xs);
  font-family: 'Monaco', 'Consolas', monospace;
  background: rgba(99, 102, 241, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  display: inline-block;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  flex-wrap: wrap;
}

.prompt-type {
  font-size: 12px;
  color: var(--text-secondary);
  background: var(--bg-tertiary);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-weight: 500;
}

.version-badge {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-family: 'SF Mono', 'Monaco', monospace;
  border: 1px solid;
}

.version-badge.draft-version {
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.1);
  border-color: rgba(245, 158, 11, 0.2);
}

.version-badge.published-version {
  color: var(--primary-color);
  background: rgba(99, 102, 241, 0.1);
  border-color: rgba(99, 102, 241, 0.2);
}

.meta-divider {
  font-size: 10px;
  color: var(--text-muted);
  opacity: 0.5;
}

.mode-indicator {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
}

.mode-indicator.mode-mock {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.mode-indicator.mode-live {
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.1);
}

.enabled-indicator {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
}

.enabled-indicator.is-enabled {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.enabled-indicator.is-disabled {
  color: #6b7280;
  background: rgba(107, 114, 128, 0.1);
}

.card-status {
  flex-shrink: 0;
}

.status-tag {
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 12px;
  padding: 4px 10px;
}

.card-content {
  margin-bottom: var(--spacing-md);
}

.template-preview {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0 0 var(--spacing-md);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  background: var(--bg-secondary);
  padding: var(--spacing-sm);
  border-radius: var(--radius-md);
  font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
  font-size: 13px;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
}

.card-tags .el-tag {
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 500;
  border: none;
}

.provider-tag {
  background: rgba(16, 185, 129, 0.1);
  color: #059669;
}

.model-tag {
  background: rgba(107, 114, 128, 0.1);
  color: #374151;
}

.return-type-tag {
  background: rgba(245, 158, 11, 0.1);
  color: #d97706;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-sm);
  border-top: 1px solid var(--border-light);
}

.card-info {
  flex: 1;
}

.created-time {
  font-size: 12px;
  color: var(--text-muted);
}

.card-actions {
  display: flex;
  gap: var(--spacing-xs);
}

.card-actions .el-button {
  padding: 4px;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.card-actions .el-button:hover {
  transform: scale(1.1);
}

/* 分页 */
.pagination-section {
  margin-top: var(--spacing-xl);
  display: flex;
  justify-content: center;
}

.modern-pagination {
  background: var(--bg-primary);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .cards-container {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: var(--spacing-md);
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-md);
  }
  
  .page-title {
    font-size: 28px;
  }
  
  .filters-section {
    padding: var(--spacing-md);
  }
  
  .filter-tabs {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-sm);
  }
  
  .cards-container {
    grid-template-columns: 1fr;
  }
  
  .search-input-wrapper {
    max-width: none;
  }
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .header-container {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
    text-align: center;
  }
  
  .header-center {
    order: -1;
  }
  
  .search-container {
    max-width: 500px;
  }
  
  .search-row {
    flex-direction: column;
    gap: var(--spacing-sm);
  }
  
  .search-input,
  .provider-select {
    flex: none;
    width: 100%;
  }
  
  .header-left,
  .header-right {
    justify-content: center;
  }
  
  .title-section {
    text-align: center;
  }
}

@media (max-width: 768px) {
  .header-container {
    padding: var(--spacing-md) var(--spacing-lg);
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .page-subtitle {
    font-size: 13px;
  }
  
  .create-btn {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: 14px;
  }
  
  :deep(.search-input .el-input__wrapper) {
    height: 44px;
  }
}

@media (max-width: 480px) {
  .header-container {
    padding: var(--spacing-sm) var(--spacing-md);
  }
  
  .page-title {
    font-size: 20px;
  }
  
  .page-subtitle {
    font-size: 12px;
  }
  
  .prompt-card {
    padding: var(--spacing-md);
  }
  
  .card-title {
    font-size: 16px;
  }
  
  .create-btn span {
    display: none;
  }
}
</style>