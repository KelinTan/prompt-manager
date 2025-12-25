# Prompt Manager

一个功能完整的 Prompt 管理系统，提供 Prompt 的创建、编辑、版本控制、发布和调试等全套功能。

## 📋 项目简介

Prompt Manager 是一个企业级的提示词(Prompt)管理平台，专为 AI 应用开发团队设计。它提供了一套完整的工具来管理、版本控制和优化 AI 提示词，支持多种 AI 服务商(OpenAI、阿里云 DashScope 等)的集成。

### 主要功能

- **Prompt 管理**
  <img width="1764" height="806" alt="image" src="https://github.com/user-attachments/assets/d044abff-4292-4058-a1a5-428a78e19e64" />
  - 创建、编辑、预览、删除 Prompt
  - 版本管理和历史记录
  - Prompt 发布和生效管理
  - 启用/禁用 Prompt 状态控制
  
- **Prompt 调试**

  - 实时 Prompt 测试
  - 支持多种 AI 提供商
  - 支持多模态输入(文本、图片、文档)
  - 流式响应输出
  - 自定义返回类型和大小

- **版本管理**
  <img width="1166" height="958" alt="image" src="https://github.com/user-attachments/assets/f112ae20-3761-4ff1-ba70-dbed17d0b1ca" />

  - 完整的版本历史记录
  - 版本回滚功能
  - 变更追踪

- **AI 助手**
  <img width="1154" height="987" alt="image" src="https://github.com/user-attachments/assets/0b4ccb10-9ace-41a8-8533-8b980b541f4e" />

  - 实时 AI 对话助手
  - 支持多个 AI 提供商

- **权限管理**
  - JWT 认证机制
  - 管理员权限验证
  - 用户身份追踪

## 🛠 技术栈

### 后端

- **框架**: FastAPI 0.110.0
- **Python**: 3.11+
- **数据库**: MySQL (使用 SQLModel ORM)
- **异步**: asyncio、aiomysql
- **认证**: JWT (PyJWT)
- **AI 集成**:
  - OpenAI API
  - 阿里云 DashScope
- **其他**:
  - Pydantic (数据验证)
  - Alembic (数据库迁移)
  - Uvicorn (ASGI 服务器)

### 前端

- **框架**: Vue.js 3.4.29
- **UI 框架**: Element Plus 2.7.6
- **构建工具**: Vite 5.3.1
- **路由**: Vue Router 4.3.3
- **HTTP 客户端**: Axios 1.7.2
- **编辑功能**:
  - Markdown 编辑和预览 (markdown-it)
  - 代码高亮 (highlight.js)
  - Diff 对比显示

## 🚀 快速开始

### 前置要求

- Python 3.11+
- Node.js 16+
- MySQL 5.7+
- Poetry (Python 依赖管理)

### 后端安装

```bash
cd backend

# 复制环境配置文件
cp .env.example .env
# 编辑 .env 文件，配置数据库和 API 密钥等

# 编辑数据库配置
vim alembic.ini
# 修改 sqlalchemy.url 为你的数据库连接字符串

# 安装依赖
pip install poetry==1.8.2
poetry install

# 数据库迁移
poetry run alembic upgrade head

# 启动服务
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端安装

```bash
cd frontend

# 安装依赖
npm install

# 开发模式运行
npm run dev

# 构建生产版本
npm run build:prod

# 构建测试版本
npm run build:beta
```

### 使用 Docker 启动

```bash
cd backend

# 构建镜像
docker build -t prompt-manager:latest .

# 运行容器
docker run -p 8000:8000 --env-file .env prompt-manager:latest
```

## 📁 项目结构

```
prompt-manager/
├── backend/                    # 后端应用
│   ├── src/
│   │   ├── main.py            # 应用入口
│   │   ├── apis/              # API 路由
│   │   │   ├── prompt_admin_api.py    # Prompt 管理 API
│   │   │   └── login_admin_api.py     # 登录 API
│   │   ├── models/            # 数据模型
│   │   │   └── prompt.py      # Prompt 数据模型
│   │   ├── services/          # 业务逻辑层
│   │   │   └── prompt_admin_service.py
│   │   ├── repository/        # 数据访问层
│   │   │   └── prompt_repository.py
│   │   ├── aigc/              # AI 集成模块
│   │   │   ├── aigc.py
│   │   │   ├── openai_proxy.py
│   │   │   └── multi_modal.py
│   │   └── core/              # 核心功能
│   │       ├── config.py      # 配置管理
│   │       ├── db.py          # 数据库连接
│   │       └── jwt_verify.py  # JWT 验证
│   ├── alembic/               # 数据库迁移
│   ├── pyproject.toml         # Poetry 依赖配置
│   └── Dockerfile             # Docker 镜像配置
│
└── frontend/                   # 前端应用
    ├── src/
    │   ├── main.js            # 应用入口
    │   ├── App.vue            # 根组件
    │   ├── router/            # 路由配置
    │   ├── modules/           # 功能模块
    │   │   ├── prompt/        # Prompt 模块
    │   │   │   ├── views/     # 页面
    │   │   │   ├── components/ # 组件
    │   │   │   └── api/       # API 请求
    │   │   └── common/        # 公共模块
    │   └── style/             # 样式文件
    ├── package.json           # NPM 依赖配置
    ├── vite.config.js         # Vite 构建配置
    └── index.html             # HTML 入口
```

## 🔑 核心 API

### Prompt 管理

- `POST /admin/api/prompts` - 创建 Prompt
- `PUT /admin/api/prompts/{prompt_id}` - 更新 Prompt
- `GET /admin/api/prompts/{prompt_id}` - 获取 Prompt 详情
- `GET /admin/api/prompts` - 列表查询
- `POST /admin/api/prompts/{prompt_id}/publish` - 发布 Prompt
- `POST /admin/api/prompts/{prompt_id}/enable` - 启用 Prompt
- `POST /admin/api/prompts/{prompt_id}/disable` - 禁用 Prompt
- `GET /admin/api/prompts/{prompt_id}/history` - 获取版本历史
- `POST /admin/api/prompts/{prompt_id}/rollback` - 版本回滚

### Prompt 调试

- `POST /admin/api/prompts/{prompt_id}/debug` - 调试 Prompt
- `POST /admin/api/prompts/{prompt_id}/synthesis` - 合成 Prompt

### 认证

- `POST /admin/api/login` - 用户登录

## ⚙️ 配置说明

### 环境变量配置 (.env)

```env
# 应用配置
APP_ENV=development
APP_PORT=8000

# 数据库配置
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/prompt_manager

# JWT 配置
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24

# OpenAI 配置
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1

# DashScope 配置
DASHSCOPE_API_KEY=sk-...

# 日志配置
LOG_LEVEL=INFO
```

## 🧪 测试

### 后端测试

```bash
cd backend

# 运行所有测试
poetry run pytest

# 运行带覆盖率的测试
poetry run pytest --cov=src

# 运行特定测试文件
poetry run pytest tests/test_prompt.py
```

### 前端测试

```bash
cd frontend

# 运行 ESLint 检查
npm run lint

# 自动修复 ESLint 问题
npm run lint:fix

# 代码格式化
npm run format

# 检查代码格式
npm run format:check
```

## 📝 数据库迁移

使用 Alembic 管理数据库版本:

```bash
cd backend

# 生成新的迁移文件
poetry run alembic revision --autogenerate -m "description"

# 应用所有待迁移的版本
poetry run alembic upgrade head

# 回滚到上一个版本
poetry run alembic downgrade -1
```

## 🐳 Docker 部署

项目包含 Docker 支持:

```bash
# 构建镜像
docker build -t prompt-manager:latest .

# 运行容器
docker run -d \
  --name prompt-manager \
  -p 8000:8000 \
  -e DATABASE_URL=mysql+aiomysql://user:password@db:3306/prompt_manager \
  -e OPENAI_API_KEY=your-key \
  prompt-manager:latest

# 使用 Docker Compose
docker-compose up -d
```

## 📚 API 文档

启动后端服务后，可以访问 OpenAPI 文档:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👥 作者

- Kelin Tan

## 🎯 项目路线图

- [ ] 支持更多 AI 提供商(Google, Claude 等)
- [ ] 增强的版本对比功能
- [ ] Prompt 模板库
- [ ] 性能监控和统计分析
- [ ] 团队协作功能
- [ ] 导入/导出功能

## 📧 联系方式

如有问题或建议，欢迎通过以下方式联系:

- GitHub Issues: [提交问题](../../issues)
- Email: kelin.tan@hotmail.com

---

**最后更新**: 2024年12月
