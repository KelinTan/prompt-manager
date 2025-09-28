# 登录认证系统使用说明

## 🔐 认证流程

### 1. 后端接口格式
```bash
# 请求
POST /admin/api/login
Content-Type: application/json

{
    "username": "kelin.tan",
    "password": "tanzhuchao"
}

# 响应格式
{
    "meta": {
        "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9..."
    }
}
```

### 2. 前端处理
- 从 `response.data.meta.accessToken` 获取 token
- 自动保存到 localStorage
- 后续请求自动添加 `Authorization: Bearer <token>` 头

### 3. 开发便利功能
- 开发环境自动预填测试账号
- 详细的错误处理和用户提示
- 网络错误、认证错误分类处理

## 🚀 使用步骤

### 启动开发服务器
```bash
npm run dev
```

### 访问登录页面
- 直接访问：`http://localhost:3000/#/login`
- 或访问任意需要认证的页面会自动跳转

### 测试登录
- 用户名：`kelin.tan`
- 密码：`tanzhuchao`
- 开发环境已自动预填

## 📋 功能特性

### ✅ 已实现
- [x] 登录页面UI
- [x] 后端API集成
- [x] Token管理
- [x] 路由保护
- [x] 自动重定向
- [x] 前端登出功能（无需后端接口）
- [x] 错误处理
- [x] 开发便利功能

### 🔧 技术要点
- **状态管理**: 使用 Vue 3 Composition API + reactive
- **持久化**: localStorage 存储 token 和用户信息
- **请求拦截**: axios 自动添加认证头
- **错误处理**: 401 自动跳转登录页
- **路由守卫**: 未认证自动重定向

## 🛠️ 开发调试

### 测试登录API
使用 `test-login.html` 文件可以直接测试后端登录接口：
```bash
# 在项目根目录打开
open test-login.html
```

### 清除认证信息
```javascript
// 在浏览器控制台执行
localStorage.removeItem('auth_token')
localStorage.removeItem('auth_user')
location.reload()
```

### 检查认证状态
```javascript
// 在浏览器控制台执行
console.log('Token:', localStorage.getItem('auth_token'))
console.log('User:', localStorage.getItem('auth_user'))
```

## 🚨 注意事项

1. **CORS设置**: 确保后端已配置CORS允许前端域名
2. **Token过期**: 系统会自动检测401状态码并跳转登录页
3. **网络错误**: 提供用户友好的错误提示
4. **安全性**: Token存储在localStorage，刷新页面后保持登录状态

## 🔄 登出机制

### 前端登出处理
- **无需后端接口**：登出操作完全由前端处理
- **清除本地数据**：删除 localStorage 中的 token 和用户信息
- **自动跳转**：清除认证信息后跳转到登录页
- **即时生效**：无网络依赖，登出立即生效

### 登出流程
1. 用户点击登出按钮
2. 显示确认对话框
3. 用户确认后直接清除本地认证信息
4. 显示成功提示并跳转到登录页
5. 后续请求由于无 token 会被拦截器处理

## 🎯 部署配置

### 环境变量
```bash
# .env.development
VITE_API_BASE_URL=http://localhost:8080

# .env.production  
VITE_API_BASE_URL=https://your-production-api.com
```

### 构建部署
```bash
# 测试环境
npm run build:beta

# 生产环境
npm run build:prod
```