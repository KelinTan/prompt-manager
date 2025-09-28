# API 配置说明

## 接口地址配置

前端应用现在配置为直接访问后端API，不使用代理。

### 环境配置

| 环境 | API基础地址 | 完整接口示例 |
|------|-------------|--------------|
| 开发环境 | `http://localhost:8080/api` | `http://localhost:8080/api/prompts` |
| 测试环境 | `http://test-api.yourcompany.com/api` | `http://test-api.yourcompany.com/api/prompts` |
| 生产环境 | `https://api.yourcompany.com/api` | `https://api.yourcompany.com/api/prompts` |

### 配置文件

```bash
# .env.development
VITE_API_BASE_URL=http://localhost:8080/api
VITE_APP_TITLE=Prompt Manager (Development)

# .env.production  
VITE_API_BASE_URL=https://api.yourcompany.com/api
VITE_APP_TITLE=Prompt Manager

# .env.test
VITE_API_BASE_URL=http://test-api.yourcompany.com/api
VITE_APP_TITLE=Prompt Manager (Test)
```

### 后端接口要求

确保你的后端服务提供以下接口：

#### Prompt 管理接口
- `GET /api/prompts` - 获取Prompt列表
  - 查询参数: `page`, `size`, `name`, `type`, `ai_provider`
  - 返回: `{ total: number, page: number, size: number, items: [] }`

- `GET /api/prompts/:id` - 获取单个Prompt详情
  - 返回: Prompt对象

- `POST /api/prompts` - 创建新Prompt
  - 请求体: Prompt对象
  - 返回: 创建的Prompt对象

- `PUT /api/prompts/:id` - 更新Prompt
  - 请求体: 更新的Prompt对象
  - 返回: 更新后的Prompt对象

- `DELETE /api/prompts/:id` - 删除Prompt
  - 返回: 删除确认

#### 版本管理接口
- `POST /api/prompts/:id/publish` - 发布Prompt（版本号+1）
  - 返回: 发布后的Prompt对象

- `GET /api/prompts/:id/history` - 获取历史版本列表
  - 返回: `{ total: number, page: number, size: number, items: [历史版本列表] }`

- `GET /api/prompts/:id/versions/:version` - 获取特定版本详情
  - 返回: 特定版本的Prompt对象

### CORS 配置

由于前端直接访问后端API，需要确保后端正确配置CORS：

```javascript
// 后端CORS配置示例（Node.js/Express）
app.use(cors({
  origin: [
    'http://localhost:3000',  // 开发环境
    'https://your-frontend-domain.com'  // 生产环境
  ],
  credentials: true
}))
```

## API 响应格式

### 分页响应格式

所有列表接口统一使用 `ApiPageResponse` 格式返回分页数据：

```python
class ApiPageResponse(BaseModel):
    total: int      # 总记录数
    page: int       # 当前页码（从1开始）
    size: int       # 每页记录数
    items: list     # 数据列表
```

#### 适用接口：
- `GET /api/prompts` - 获取prompt列表
- `GET /api/prompts/{id}/history` - 获取prompt历史版本

### 单个资源响应格式

单个资源接口直接返回对象数据：

#### 适用接口：
- `GET /api/prompts/{id}` - 获取单个prompt详情
- `GET /api/prompts/{id}/versions/{version}` - 获取特定版本的prompt
- `POST /api/prompts` - 创建prompt（返回创建的对象）
- `PUT /api/prompts/{id}` - 更新prompt（返回更新后的对象）

### 操作响应格式

操作类接口返回简单状态：

#### 适用接口：
- `DELETE /api/prompts/{id}` - 删除prompt（返回成功状态）
- `POST /api/prompts/{id}/publish` - 发布prompt（返回发布后的对象）

### 前端处理示例

```javascript
// 1. 分页接口处理
const listResponse = await promptApi.getPrompts({ page: 1, size: 20 })
console.log('总数:', listResponse.total)
console.log('数据列表:', listResponse.items)

// 2. 单个资源接口处理
const prompt = await promptApi.getPrompt(123)
console.log('prompt标题:', prompt.title)

// 3. 历史版本接口处理（分页格式）
const historyResponse = await promptApi.getPromptHistory(123, { page: 1, size: 10 })
console.log('历史版本列表:', historyResponse.items)
```

#### Prompt 对象结构
```json
{
  "id": 1,
  "name": "Prompt名称",
  "type": "类型",
  "model": "模型名称",
  "return_type": "返回类型",
  "template": "模板内容",
  "parameters": [
    {
      "name": "参数名",
      "type": "参数类型", 
      "description": "参数描述",
      "required": true
    }
  ],
  "mock": true,
  "mock_data": {},
  "remark": "备注",
  "format_type": "braces",
  "ai_provider": "openai",
  "version": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 测试API连接

你可以使用以下命令测试API连接：

```bash
# 测试获取Prompt列表
curl http://localhost:8080/api/prompts

# 测试创建Prompt
curl -X POST http://localhost:8080/api/prompts \
  -H "Content-Type: application/json" \
  -d '{"name":"测试Prompt","template":"Hello {name}"}'
```

### 错误处理

前端会处理以下HTTP状态码：
- `200` - 成功
- `400` - 请求参数错误
- `401` - 未认证
- `403` - 无权限
- `404` - 资源不存在
- `500` - 服务器错误

确保后端返回适当的HTTP状态码和错误信息。