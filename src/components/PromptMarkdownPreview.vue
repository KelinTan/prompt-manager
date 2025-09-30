<template>
  <div class="markdown-preview">
    <div v-if="!content || !content.trim()" class="empty">预览区域（暂无内容）</div>
    <div v-else v-html="sanitizedHtml" class="markdown-body"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  content: { type: String, default: '' },
  highlight: { type: Boolean, default: true }
})

const mdRef = ref(null)
const dompurifyRef = ref(null)
const hljsRef = ref(null)
const libsLoaded = ref(false)

onMounted(async () => {
  try {
    const [mdModule, dompurifyModule, hljsModule] = await Promise.all([
      import('markdown-it'),
      import('dompurify'),
      import('highlight.js'),
      // also import the highlight.js stylesheet so highlighted blocks are styled
      import('highlight.js/styles/github.css')
    ])

    const MarkdownIt = mdModule.default || mdModule
    const DOMPurify = dompurifyModule.default || dompurifyModule
    const hljs = hljsModule.default || hljsModule

    // Ensure common languages like json are registered (some highlight.js builds require explicit registration)
    try {
      if (hljs && typeof hljs.getLanguage === 'function' && !hljs.getLanguage('json')) {
        const jsonLangModule = await import('highlight.js/lib/languages/json')
        const jsonLang = jsonLangModule.default || jsonLangModule
        if (jsonLang && typeof hljs.registerLanguage === 'function') {
          hljs.registerLanguage('json', jsonLang)
        }
      }
    } catch (e) {
      // ignore registration errors
    }

    mdRef.value = new MarkdownIt({
      html: true,
      linkify: true,
      typographer: true,
      highlight: (str, lang) => {
        if (!props.highlight) return ''
        if (lang && hljs.getLanguage && hljs.getLanguage(lang)) {
          try {
            return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang }).value}</code></pre>`
          } catch (__) {}
        }
        try {
          return `<pre class="hljs"><code>${hljs.highlightAuto(str).value}</code></pre>`
        } catch (__) {
          return `<pre class="hljs"><code>${MarkdownIt.utils.escapeHtml(str)}</code></pre>`
        }
      }
    })

    dompurifyRef.value = DOMPurify
    hljsRef.value = hljs
    libsLoaded.value = true
  } catch (e) {
    // If imports fail (packages not installed), we'll fall back to a simple renderer.
    libsLoaded.value = false
    // console.warn('Markdown preview libs not available, using fallback renderer.')
  }
})

const rawHtml = computed(() => {
  if (libsLoaded.value && mdRef.value) {
    return mdRef.value.render(props.content || '')
  }

  // Fallback: basic escaping + minimal markdown handling
  const text = props.content || ''
  const escapeHtml = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  const escaped = escapeHtml(text)
  // code fences ``` -> <pre><code>
  const withCode = escaped.replace(/```([\s\S]*?)```/g, (_m, p1) => `<pre><code>${p1}</code></pre>`)
  // convert double newlines to paragraphs and single newlines to <br>
  const paragraphs = withCode.split(/\n\s*\n/).map(s => `<p>${s.replace(/\n/g, '<br/>')}</p>`).join('')
  return paragraphs
})

const sanitizedHtml = computed(() => {
  if (libsLoaded.value && dompurifyRef.value) {
    return dompurifyRef.value.sanitize(rawHtml.value, { SAFE_FOR_TEMPLATES: true })
  }
  return rawHtml.value
})
</script>

<style scoped>
.markdown-preview {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  padding: 12px;
  border-radius: 8px;
  min-height: 120px;
  overflow: auto;
}

.markdown-body h1 { font-size: 1.6em; margin: 0.5em 0; }
.markdown-body h2 { font-size: 1.4em; margin: 0.45em 0; }
.markdown-body p { margin: 0.5em 0; color: var(--text-secondary); }
.markdown-body pre { background: #0b0b0b; padding: 10px; border-radius: 6px; overflow: auto; }
.markdown-body code { background: rgba(0,0,0,0.04); padding: 2px 6px; border-radius: 4px; font-family: 'SF Mono', monospace; }
.empty { color: var(--text-muted); padding: 20px; text-align: center; }
</style>
