# Prompt Manager

企业级 AI Prompt 管理平台，基于 Vue3 + Vite + Element Plus 构建，支持多模型、多版本、协作与回滚。

## 功能特性

- ✅ **Prompt 管理**：增删改查、模板内容、Mock 数据配置
- ✅ **搜索与筛选**：按标题、供应商等条件搜索
- ✅ **版本控制**：每次发布/回滚自动生成新版本，支持历史版本查看
- ✅ **历史记录**：时间线展示所有历史版本，支持版本详情、对比、回滚
- ✅ **回滚功能**：可一键回滚到任意历史版本
- ✅ **发布功能**：支持草稿/已发布状态切换
- ✅ **响应式设计**：适配多端，现代化 UI

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

- **Prompt 列表页**：卡片式展示，支持搜索、分页、发布、历史、删除
- **Prompt 编辑页**：新建/编辑，支持所有字段和 Mock 数据
- **历史版本页**：时间线展示，支持版本详情、对比、回滚
- **版本详情页**：查看特定版本内容，支持恢复

## 版本与回滚说明

- 每次发布或回滚都会生成一个新版本，历史记录完整保留
- 当前版本以绿色标签标识，历史版本可随时回滚
- 回滚后自动刷新页面，当前版本标签始终准确

## API 接口

- `GET /api/prompts`：获取列表
- `GET /api/prompts/:id`：获取详情
- `POST /api/prompts`：新建
- `PUT /api/prompts/:id`：更新
- `DELETE /api/prompts/:id`：删除
- `POST /api/prompts/:id/publish`：发布
- `GET /api/prompts/:id/history`：历史版本
- `POST /api/prompts/:id/rollback`：回滚到历史版本

## 项目结构

```
src/
  api/           # API接口
  models/        # 数据模型
  router/        # 路由
  views/         # 页面组件
  App.vue        # 根组件
  main.js        # 入口
```

## 环境变量

- `.env.development` - 开发环境
- `.env.production` - 生产环境