// 演示数据 - 用于开发测试
export const mockPrompts = [
  {
    id: 1,
    name: '代码审查助手',
    type: '代码审查',
    model: 'gpt-4',
    return_type: 'markdown',
    template: `请对以下代码进行详细审查：

代码：
{code}

请从以下几个方面进行评估：
1. 代码质量和可读性
2. 潜在的bug和安全问题
3. 性能优化建议
4. 最佳实践建议

请以markdown格式返回审查结果。`,
    parameters: [
      {
        name: 'code',
        type: 'string',
        description: '要审查的代码',
        required: true
      }
    ],
    mock: true,
    mock_data: {
      review: '代码审查结果示例',
      score: 85,
      suggestions: ['建议1', '建议2']
    },
    remark: '用于代码质量审查的AI助手',
    format_type: 'braces',
    ai_provider: 'openai',
    version: 3,
    created_at: '2024-01-15T10:30:00Z',
    updated_at: '2024-01-20T14:20:00Z'
  },
  {
    id: 2,
    name: '文档生成器',
    type: '文档生成',
    model: 'claude-3',
    return_type: 'markdown',
    template: `根据以下API接口信息生成技术文档：

接口名称：{api_name}
请求方法：{method}
请求路径：{path}
参数说明：{parameters}

请生成包含以下内容的完整API文档：
- 接口描述
- 请求示例
- 响应示例
- 错误码说明`,
    parameters: [
      {
        name: 'api_name',
        type: 'string',
        description: 'API接口名称',
        required: true
      },
      {
        name: 'method',
        type: 'string',
        description: 'HTTP方法',
        required: true
      },
      {
        name: 'path',
        type: 'string',
        description: '请求路径',
        required: true
      },
      {
        name: 'parameters',
        type: 'string',
        description: '参数说明',
        required: false
      }
    ],
    mock: true,
    mock_data: {
      title: 'API文档示例',
      content: '这是生成的API文档内容...'
    },
    remark: '自动生成API技术文档',
    format_type: 'braces',
    ai_provider: 'claude',
    version: 1,
    created_at: '2024-01-10T09:15:00Z',
    updated_at: '2024-01-10T09:15:00Z'
  },
  {
    id: 3,
    name: 'SQL查询优化',
    type: '数据库优化',
    model: 'gpt-3.5-turbo',
    return_type: 'text',
    template: `请分析并优化以下SQL查询：

原始查询：
[sql_query]

数据库类型：[db_type]
表结构信息：[table_info]

请提供：
1. 查询性能分析
2. 优化建议
3. 优化后的SQL语句
4. 索引建议`,
    parameters: [
      {
        name: 'sql_query',
        type: 'text',
        description: '需要优化的SQL查询语句',
        required: true
      },
      {
        name: 'db_type',
        type: 'string',
        description: '数据库类型（MySQL、PostgreSQL等）',
        required: true
      },
      {
        name: 'table_info',
        type: 'text',
        description: '相关表结构信息',
        required: false
      }
    ],
    mock: false,
    mock_data: {},
    remark: '数据库查询性能优化助手',
    format_type: 'square_brackets',
    ai_provider: 'openai',
    version: 2,
    created_at: '2024-01-12T16:45:00Z',
    updated_at: '2024-01-18T11:30:00Z'
  }
]

export const mockVersionHistory = {
  1: [
    {
      version: 3,
      name: '代码审查助手',
      template: '最新版本的模板内容...',
      created_at: '2024-01-20T14:20:00Z'
    },
    {
      version: 2,
      name: '代码审查助手',
      template: '第二版本的模板内容...',
      created_at: '2024-01-18T10:15:00Z'
    },
    {
      version: 1,
      name: '代码审查助手',
      template: '初始版本的模板内容...',
      created_at: '2024-01-15T10:30:00Z'
    }
  ]
}
