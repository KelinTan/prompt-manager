<template>
  <pre>{{ displayedText }}<span v-if="isTyping" class="cursor">|</span></pre>
</template>

<script>
import { ref, watch, onUnmounted } from 'vue'

export default {
  name: 'TypewriterText',
  props: {
    fullText: {
      type: String,
      default: ''
    },
    speed: {
      type: Number,
      default: 50 // 每个字符的延迟时间（毫秒）
    }
  },
  setup(props) {
    const displayedText = ref('')
    const isTyping = ref(false)
    const currentIndex = ref(0)
    let timer = null

    const startTyping = () => {
      if (timer) {
        clearInterval(timer)
      }
      
      displayedText.value = ''
      currentIndex.value = 0
      isTyping.value = true
      
      timer = setInterval(() => {
        if (currentIndex.value < props.fullText.length) {
          displayedText.value += props.fullText[currentIndex.value]
          currentIndex.value++
          console.log('打字机效果显示:', displayedText.value) // 调试日志
        } else {
          isTyping.value = false
          clearInterval(timer)
          timer = null
        }
      }, props.speed)
    }

    // 监听全文变化
    watch(() => props.fullText, (newText) => {
      if (newText && newText !== displayedText.value) {
        console.log('开始打字机效果，全文长度:', newText.length) // 调试日志
        startTyping()
      }
    }, { immediate: true })

    onUnmounted(() => {
      if (timer) {
        clearInterval(timer)
      }
    })

    return {
      displayedText,
      isTyping
    }
  }
}
</script>

<style scoped>
.cursor {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
</style>