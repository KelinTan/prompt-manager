module.exports = {
  // 基础配置
  printWidth: 100,              // 每行最大字符数
  tabWidth: 2,                  // 缩进空格数
  useTabs: false,               // 使用空格而非 tab
  semi: false,                  // 不使用分号
  singleQuote: true,            // 使用单引号
  quoteProps: 'as-needed',      // 对象属性仅在需要时加引号
  
  // JSX 配置
  jsxSingleQuote: false,        // JSX 使用双引号
  
  // 尾随逗号
  trailingComma: 'none',        // 不使用尾随逗号
  
  // 括号空格
  bracketSpacing: true,         // 对象括号内添加空格 { foo: bar }
  bracketSameLine: false,       // 多行元素的 > 另起一行
  
  // 箭头函数括号
  arrowParens: 'avoid',         // 单参数箭头函数省略括号
  
  // Vue 配置
  vueIndentScriptAndStyle: false, // Vue 文件中 script 和 style 标签内不缩进
  
  // 换行符
  endOfLine: 'lf',              // 使用 LF 换行符
  
  // HTML 空格敏感度
  htmlWhitespaceSensitivity: 'ignore',
  
  // 其他
  embeddedLanguageFormatting: 'auto',
  singleAttributePerLine: false
}
