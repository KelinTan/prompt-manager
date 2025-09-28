// 环境配置工具
export const config = {
  // API基础URL
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api',
  
  // 应用标题
  appTitle: import.meta.env.VITE_APP_TITLE || 'Prompt Manager',
  
  // 是否为开发环境
  isDev: import.meta.env.DEV,
  
  // 是否为生产环境
  isProd: import.meta.env.PROD,
  
  // 当前模式
  mode: import.meta.env.MODE,
  
  // 获取完整的API URL
  getApiUrl: (path = '') => {
    const baseUrl = config.apiBaseUrl
    return path ? `${baseUrl}${path.startsWith('/') ? '' : '/'}${path}` : baseUrl
  },
  
  // 日志输出（仅开发环境）
  log: (...args) => {
    if (config.isDev) {
      console.log('[Prompt Manager]', ...args)
    }
  },
  
  // 错误日志
  error: (...args) => {
    if (config.isDev) {
      console.error('[Prompt Manager Error]', ...args)
    }
  },
  
  // 警告日志
  warn: (...args) => {
    if (config.isDev) {
      console.warn('[Prompt Manager Warning]', ...args)
    }
  }
}

// 在开发环境下输出配置信息
if (config.isDev) {
  config.log('Environment Config:', {
    mode: config.mode,
    apiBaseUrl: config.apiBaseUrl,
    appTitle: config.appTitle,
    isDev: config.isDev,
    isProd: config.isProd
  })
}

export default config