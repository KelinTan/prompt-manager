# AIGC Admin

企业级 AIGC 管理平台，基于 Vue3 + Vite + Element Plus 构建，支持 Prompt 模板管理和 AI 任务管理。

## 功能特性

### Prompt 管理模块
- ✅ **Prompt 管理**：增删改查、模板内容、Mock 数据配置
- ✅ **搜索与筛选**：按标题、供应商等条件搜索
- ✅ **版本控制**：每次发布/回滚自动生成新版本，支持历史版本查看
- ✅ **历史记录**：时间线展示所有历史版本，支持版本详情、对比、回滚
- ✅ **回滚功能**：可一键回滚到任意历史版本
- ✅ **发布功能**：支持草稿/已发布状态切换
- ✅ **AI 助手**：智能对话助手

### Task 管理模块
- ✅ **任务列表**：卡片式展示所有 AI 生成任务
- ✅ **任务筛选**：按类型、状态、时间等条件筛选
- ✅ **任务详情**：查看任务参数、结果、执行日志
- ✅ **任务重试**：失败任务重试
- ✅ **实时状态**：任务状态实时更新

### 通用功能
- ✅ **统一登录**：支持多模块共享登录状态
- ✅ **响应式设计**：适配多端，现代化 UI
- ✅ **模块化架构**：清晰的代码组织，便于维护和扩展

## 技术栈

- Vue 3.x (Composition API)
- Vite 5.x
- Element Plus 2.x
- Vue Router 4.x
- Axios

## 快速开始

```bash
npm install
npm run dev
# 访问 http://localhost:3000
```

## 构建与预览

```bash
npm run build      # 生产环境构建
npm run preview    # 预览生产环境
```

## 主要页面

### Prompt 模块
- **Prompt 列表页**：卡片式展示，支持搜索、分页、发布、历史、删除
- **Prompt 编辑页**：新建/编辑，支持所有字段和 Mock 数据
- **历史版本页**：时间线展示，支持版本详情、对比、回滚
- **版本详情页**：查看特定版本内容，支持恢复
- **AI 助手页**：智能对话助手

#### 版本与回滚说明

- 每次发布或回滚都会生成一个新版本，历史记录完整保留
- 当前版本以绿色标签标识，历史版本可随时回滚
- 回滚后自动刷新页面，当前版本标签始终准确

### Task 模块
- **任务列表页**：表格式展示，支持筛选、分页、查看详情
- **任务详情页**：查看任务完整信息、参数、结果

## API 接口

### Prompt API
- `GET /api/prompts`：获取列表
- `GET /api/prompts/:id`：获取详情
- `POST /api/prompts`：新建
- `PUT /api/prompts/:id`：更新
- `DELETE /api/prompts/:id`：删除
- `POST /api/prompts/:id/publish`：发布
- `GET /api/prompts/:id/history`：历史版本
- `POST /api/prompts/:id/rollback`：回滚到历史版本

### Task API
- `GET /api/tasks`：获取任务列表
- `POST /api/tasks/:uuid/retry`：重试任务
- `GET /api/tasks/type`：获取任务类型列表

### Auth API
- `POST /api/auth/login`：用户登录

## 项目结构

```
src/
  modules/
    prompt/      # Prompt 模块
      api/       # Prompt API
      models/    # Prompt 数据模型
      views/     # Prompt 页面
      components/ # Prompt 组件
      config/    # Prompt 配置
    task/        # Task 模块
      api/       # Task API
      models/    # Task 数据模型
      views/     # Task 页面
      components/ # Task 组件
    common/      # 公共模块
      api/       # 公共 API (auth, request)
      stores/    # 状态管理
      utils/     # 工具函数
      views/     # 公共页面 (Login)
  router/        # 路由配置
  style/         # 全局样式
  App.vue        # 根组件
  main.js        # 入口
```

## 环境变量

- `.env.development` - 开发环境
- `.env.production` - 生产环境