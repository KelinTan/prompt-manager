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
            <el-input 
              v-model="searchForm.title" 
              placeholder="搜索 Prompt..."
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
                <span class="version-badge">{{ prompt.version ? `v${prompt.version}` : 'latest' }}</span>
              </div>
            </div>
            <div class="card-status">
              <el-tag 
                :type="prompt.mock ? 'success' : 'info'" 
                size="small"
                class="status-tag"
              >
                {{ prompt.mock ? 'Mock' : 'Live' }}
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
              <el-button 
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { promptApi } from '@/api/prompt'
import { FORMAT_TYPE_OPTIONS } from '@/models/prompt'

export default {
  name: 'PromptList',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const prompts = ref([])
    const publishingIds = ref(new Set())

    // 搜索表单
    const searchForm = reactive({
      title: ''
    })

    // 分页
    const pagination = reactive({
      page: 1,
      size: 12,
      total: 0
    })

    // AI提供商选项


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
      searchForm.title = ''
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
      ElMessage.info('发布功能暂未开发，敬请期待')
      // try {
      //   await ElMessageBox.confirm(
      //     `确定要发布Prompt "${row.title || row.name}" 吗？发布后版本号将+1。`,
      //     '确认发布',
      //     {
      //       confirmButtonText: '确定',
      //       cancelButtonText: '取消',
      //       type: 'warning'
      //     }
      //   )

      //   publishingIds.value.add(row.id)
      //   await promptApi.publishPrompt(row.id)
      //   ElMessage.success('发布成功')
      //   loadData() // 重新加载数据
      // } catch (error) {
      //   if (error !== 'cancel') {
      //     ElMessage.error('发布失败: ' + error.message)
      //   }
      // } finally {
      //   publishingIds.value.delete(row.id)
      // }
    }

    // 查看历史
    const handleHistory = (row) => {
      ElMessage.info('历史版本功能暂未开发，敬请期待')
      // router.push(`/prompts/${row.id}/history`)
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



    onMounted(() => {
      loadData()
    })

    return {
      loading,
      prompts,
      searchForm,
      pagination,

      publishingIds,
      getFormatTypeLabel,
      formatDate,
      handleSearch,
      handleReset,
      handleSizeChange,
      handleCurrentChange,
      handleRowClick,
      handleEdit,
      handlePublish,
      handleHistory,
      handleDelete
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
  max-width: 400px;
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
  color: var(--primary-color);
  background: rgba(99, 102, 241, 0.1);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-family: 'SF Mono', 'Monaco', monospace;
}

.card-status {
  flex-shrink: 0;
}

.status-tag {
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 11px;
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