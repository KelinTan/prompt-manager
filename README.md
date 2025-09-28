# Prompt Manager

基于 Vue3 + Vite + Element Plus 构建的 Prompt 管理系统，用于公司内部的 AI Prompt 模板管理。

## 功能特性

- ✅ **Prompt 管理**: 支持 Prompt 的增删改查操作
- ✅ **版本控制**: 支持 Prompt 版本管理，发布时自动版本号+1
- ✅ **历史记录**: 可查看 Prompt 的历史版本和变更记录
- ✅ **版本对比**: 支持不同版本之间的内容对比
- ✅ **搜索过滤**: 支持按名称、类型、AI提供商等条件搜索
- ✅ **Mock 数据**: 支持配置和管理 Mock 数据
- ✅ **参数管理**: 支持动态参数配置和管理
- ✅ **响应式设计**: 适配不同屏幕尺寸

## 技术栈

- **前端框架**: Vue 3.x (Composition API)
- **构建工具**: Vite 5.x
- **UI 组件库**: Element Plus 2.x
- **路由管理**: Vue Router 4.x
- **HTTP 客户端**: Axios
- **图标**: Element Plus Icons

## 数据库结构

基于以下数据库表结构设计：

```sql
CREATE TABLE `prompt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `type` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `model` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `return_type` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `template` text COLLATE utf8mb4_bin,
  `parameters` json DEFAULT NULL,
  `mock` tinyint(1) DEFAULT '1',
  `mock_data` json DEFAULT NULL,
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `format_type` enum('square_brackets','braces','none') COLLATE utf8mb4_bin NOT NULL DEFAULT 'braces',
  `ai_provider` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
# 开发环境
npm run dev

# 测试环境
npm run dev:test
```

项目将在 `http://localhost:3000` 启动。

### 构建不同环境版本

```bash
# 构建生产环境
npm run build

# 构建测试环境
npm run build:test

# 构建开发环境
npm run build:dev
```

### 预览构建结果

```bash
# 预览生产环境构建
npm run preview

# 预览测试环境构建
npm run preview:test
```

## 项目结构

```
prompt-manager/
├── public/                 # 静态资源
├── src/
│   ├── api/               # API 接口定义
│   │   └── prompt.js      # Prompt 相关 API
│   ├── models/            # 数据模型
│   │   └── prompt.js      # Prompt 数据模型
│   ├── router/            # 路由配置
│   │   └── index.js       # 路由定义
│   ├── utils/             # 工具函数
│   │   └── request.js     # HTTP 请求封装
│   ├── views/             # 页面组件
│   │   ├── PromptList.vue     # Prompt 列表页
│   │   ├── PromptEdit.vue     # Prompt 编辑页
│   │   ├── PromptHistory.vue  # 历史版本页
│   │   └── PromptVersion.vue  # 版本详情页
│   ├── App.vue            # 根组件
│   └── main.js            # 应用入口
├── index.html             # HTML 模板
├── package.json           # 项目配置
├── vite.config.js         # Vite 配置
└── README.md              # 项目说明
```

## 页面说明

### 1. Prompt 列表页 (`/prompts`)
- 显示所有 Prompt 的列表
- 支持按名称、类型、AI提供商搜索
- 支持分页显示
- 提供编辑、发布、查看历史、删除等操作

### 2. Prompt 编辑页 (`/prompts/create` | `/prompts/:id/edit`)
- 创建新的 Prompt 或编辑现有 Prompt
- 包含所有字段的表单：名称、类型、模型、模板等
- 支持动态添加/删除参数
- 支持 Mock 数据配置
- 提供保存和发布功能

### 3. 历史版本页 (`/prompts/:id/history`)
- 显示 Prompt 的所有历史版本
- 时间线形式展示版本变更
- 支持查看版本详情和版本对比
- 显示当前版本状态

### 4. 版本详情页 (`/prompts/:id/versions/:version`)
- 显示特定版本的完整信息
- 支持复制模板内容和 Mock 数据
- 支持恢复历史版本
- 提供全屏查看模式

## API 接口说明

项目通过代理配置连接后端 API，默认代理到 `http://localhost:8080`。

主要接口：
- `GET /api/prompts` - 获取 Prompt 列表
- `GET /api/prompts/:id` - 获取单个 Prompt
- `POST /api/prompts` - 创建 Prompt
- `PUT /api/prompts/:id` - 更新 Prompt
- `DELETE /api/prompts/:id` - 删除 Prompt
- `POST /api/prompts/:id/publish` - 发布 Prompt
- `GET /api/prompts/:id/history` - 获取历史版本
- `GET /api/prompts/:id/versions/:version` - 获取特定版本

## 开发说明

### 代码规范
- 使用 Vue 3 Composition API
- 采用 ES6+ 语法
- 组件命名使用 PascalCase
- 文件命名使用 PascalCase

### 样式规范
- 使用 Element Plus 组件库样式
- 自定义样式采用 scoped
- 响应式设计，适配移动端

### 状态管理
- 使用 Vue 3 的 reactive/ref 进行状态管理
- 暂未集成 Vuex/Pinia，可根据需求添加

## 环境配置

项目支持多环境配置，通过环境变量文件来管理不同环境的配置：

### 环境变量文件

- `.env.development` - 开发环境配置
- `.env.test` - 测试环境配置  
- `.env.production` - 生产环境配置

### 可配置变量

- `VITE_API_BASE_URL` - 后端API基础地址（包含/api路径）
- `VITE_APP_TITLE` - 应用标题

### 环境切换

```bash
# 开发环境（直接访问 localhost:8080/api）
npm run dev

# 测试环境
npm run dev:test

# 生产环境构建
npm run build

# 测试环境构建
npm run build:test
```

## 部署说明

1. 根据目标环境构建项目：
   ```bash
   # 生产环境
   npm run build
   
   # 测试环境
   npm run build:test
   ```

2. 将 `dist` 目录部署到 Web 服务器

3. 配置 nginx 或其他 Web 服务器的路由重写规则，支持 SPA 路由

4. 确保 `.env.production` 或 `.env.test` 中的 `VITE_API_BASE_URL` 指向正确的后端服务地址（包含/api路径）

### API接口地址说明

前端将直接访问以下格式的接口：
- 开发环境: `http://localhost:8080/api/prompts`
- 生产环境: `https://api.yourcompany.com/api/prompts`

确保后端服务提供以下接口：
- `GET /api/prompts` - 获取Prompt列表
- `GET /api/prompts/:id` - 获取单个Prompt
- `POST /api/prompts` - 创建Prompt
- `PUT /api/prompts/:id` - 更新Prompt
- `DELETE /api/prompts/:id` - 删除Prompt
- `POST /api/prompts/:id/publish` - 发布Prompt
- `GET /api/prompts/:id/history` - 获取历史版本
- `GET /api/prompts/:id/versions/:version` - 获取特定版本

## 注意事项

- 本项目暂未接入登录系统，无权限校验
- Mock 数据需要符合 JSON 格式
- 参数配置支持动态添加，建议定义参数类型和描述
- 版本管理采用递增策略，发布后版本号自动+1
- 建议配置适当的错误处理和加载状态

## 后续扩展

- [ ] 用户登录和权限管理
- [ ] Prompt 分类和标签系统
- [ ] 更丰富的版本对比功能
- [ ] 导入/导出功能
- [ ] API 文档生成
- [ ] 单元测试覆盖
- [ ] Docker 容器化部署

## 许可证

MIT License