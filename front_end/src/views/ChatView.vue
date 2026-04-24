<script setup>
import { computed, ref, nextTick, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Promotion, Service, Timer, Collection, DataAnalysis } from '@element-plus/icons-vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import 'github-markdown-css/github-markdown-light.css'

import { ragChat } from '../api/rag'
import { getUserUsage } from '../api/users'

const route = useRoute()
const kbId = Number(route.params.kbId)

const question = ref('')
const loading = ref(false)
const messages = ref([])
const chatContainer = ref(null)
const userUsage = ref(null)
const usageLoading = ref(false)
const sessionId = ref(null)

const canSend = computed(() => {
  const hasQuestion = Boolean(question.value.trim())
  const notLoading = !loading.value
  const hasRemaining = userUsage.value?.remaining > 0
  return hasQuestion && notLoading && hasRemaining
})

async function loadUserUsage() {
  usageLoading.value = true
  try {
    const data = await getUserUsage()
    userUsage.value = data
  } catch (error) {
    console.error('获取使用次数失败', error)
  } finally {
    usageLoading.value = false
  }
}

onMounted(() => {
  loadUserUsage()
})

// 安全地渲染 Markdown
function renderMarkdown(content) {
  if (!content) return ''
  // marked.parse 返回的可能是一个 Promise (如果配置了 async)，但默认是同步的字符串
  const rawHtml = marked.parse(content)
  return DOMPurify.sanitize(rawHtml)
}

// 统一处理问答错误信息（包含超时等网络异常）
function getChatErrorMessage(e) {
  const status = e?.response?.status
  const detail = e?.response?.data?.detail
  if (typeof detail === 'string' && detail) return detail
  if (status === 403) return '无权限访问该知识库，请联系管理员'
  if (status === 404) return '知识库不存在或无权限访问'
  if (status === 408 || status === 504) return '请求超时，模型生成耗时较长，请稍后重试'
  if (e?.code === 'ECONNABORTED' || String(e?.message || '').toLowerCase().includes('timeout')) {
    return '请求超时，模型生成耗时较长，请稍后重试'
  }
  return '问答失败'
}

// 滚动到聊天底部
const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

async function send() {
  const q = question.value.trim()
  if (!q || loading.value) return

  // 添加用户问题
  messages.value.push({ role: 'user', content: q })
  question.value = ''
  loading.value = true
  scrollToBottom()

  // 添加一个占位的 AI 回复
  const placeholderIndex = messages.value.length
  messages.value.push({ role: 'assistant', content: '正在检索并生成回答...', loading: true })
  scrollToBottom()

  try {
    const data = await ragChat({ kbId, question: q, session_id: sessionId.value })
    const answer = typeof data?.answer === 'string' ? data.answer : ''
    // 更新session_id
    sessionId.value = data.session_id
    messages.value[placeholderIndex] = { 
      role: 'assistant', 
      content: answer || '（无回答）', 
      loading: false,
      metrics: {
        elapsed_ms: data.elapsed_ms,
        token_usage: data.token_usage
      }
    }
    // 重新加载使用次数
    await loadUserUsage()
  } catch (e) {
    const msg = getChatErrorMessage(e)
    ElMessage.error(msg)
    messages.value[placeholderIndex] = { role: 'assistant', content: `错误：${msg}`, loading: false, error: true }
    // 即使出错也重新加载使用次数，因为可能已经消耗了次数
    await loadUserUsage()
  } finally {
    loading.value = false
    scrollToBottom()
  }
}
</script>

<template>
  <div class="chat-layout">
    <!-- 顶部标题栏 -->
    <header class="chat-header">
      <div class="header-title">智能问答 (KB {{ kbId }})</div>
      <div class="header-actions">
        <el-tag 
          v-if="userUsage" 
          :type="userUsage.remaining > 0 ? 'success' : 'danger'" 
          effect="plain"
          size="small"
          class="usage-tag"
        >
          <el-icon><DataAnalysis /></el-icon>
          今日剩余: {{ userUsage.remaining }}/{{ userUsage.daily_limit }}次
        </el-tag>
        <el-skeleton v-else :loading="usageLoading" animated>
          <template #template>
            <el-tag size="small">加载中...</el-tag>
          </template>
        </el-skeleton>
      </div>
    </header>

    <!-- 聊天内容区域 -->
    <main class="chat-body" ref="chatContainer">
      <div class="chat-content">
        <div v-if="messages.length === 0" class="empty-state">
          <el-icon class="empty-icon"><Service /></el-icon>
          <div class="empty-text">我是你的 RAG 智能助手，请输入问题开始对话。</div>
        </div>

        <div v-else class="message-list">
          <div 
            v-for="(m, i) in messages" 
            :key="i" 
            class="message-item"
            :class="m.role === 'user' ? 'message-user' : 'message-assistant'"
          >
            <!-- 头像 -->
            <div class="avatar">
              <el-icon v-if="m.role === 'user'"><User /></el-icon>
              <el-icon v-else><Service /></el-icon>
            </div>
            
            <!-- 气泡 -->
            <div class="bubble-wrapper">
              <div class="bubble" :class="{ 'is-loading': m.loading, 'is-error': m.error }">
                <div v-if="m.role === 'user'" class="user-content">{{ m.content }}</div>
                <div v-else-if="m.loading" class="loading-content">
                  {{ m.content }}
                  <span class="typing-indicator">
                    <span>.</span><span>.</span><span>.</span>
                  </span>
                </div>
                <div v-else-if="m.error" class="error-content">{{ m.content }}</div>
                <div v-else class="markdown-body custom-markdown" v-html="renderMarkdown(m.content)"></div>
              </div>
              
              <!-- 性能指标 -->
              <div v-if="m.metrics" class="message-metrics">
                <el-tag size="small" type="info" effect="plain" class="metric-tag">
                  <el-icon><Timer /></el-icon>
                  {{ (m.metrics.elapsed_ms / 1000).toFixed(2) }}s
                </el-tag>
                <el-tag v-if="m.metrics.token_usage?.total_tokens" size="small" type="info" effect="plain" class="metric-tag">
                  <el-icon><Collection /></el-icon>
                  {{ m.metrics.token_usage.total_tokens }} tokens
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 底部输入区域 -->
    <footer class="chat-footer">
      <div class="input-container">
        <el-input
          v-model="question"
          type="textarea"
          :rows="3"
          placeholder="给智能助手发送消息... (Ctrl + Enter 发送)"
          resize="none"
          class="custom-input"
          @keydown.ctrl.enter.prevent="send"
        />
        <div class="input-actions">
          <el-button 
            type="primary" 
            circle 
            :loading="loading" 
            :disabled="!canSend" 
            @click="send"
            class="send-btn"
          >
            <el-icon v-if="!loading"><Promotion /></el-icon>
          </el-button>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.chat-layout {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: var(--bg-color);
}

.chat-header {
  height: 60px;
  min-height: 60px;
  padding: 0 24px;
  background-color: var(--bg-sidebar);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.header-actions {
  display: flex;
  align-items: center;
}

.usage-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  border-radius: 12px;
}

.chat-body {
  flex-grow: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  scroll-behavior: smooth;
}

.chat-content {
  width: 100%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 100px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  color: #c0c4cc;
}

.empty-text {
  font-size: 15px;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-bottom: 20px;
}

.message-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.message-user {
  flex-direction: row-reverse;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.message-user .avatar {
  background-color: var(--primary-color);
  color: white;
}

.message-assistant .avatar {
  background-color: white;
  color: var(--primary-color);
  border: 1px solid var(--border-color);
}

.bubble-wrapper {
  max-width: 85%; /* 放宽 AI 消息宽度，适配复杂 Markdown */
  display: flex;
  flex-direction: column;
}

.bubble {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 15px;
  line-height: 1.6;
  word-break: break-word;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.message-user .bubble {
  background-color: var(--chat-user-bg);
  color: var(--chat-user-text);
  border-top-right-radius: 2px;
}

.user-content {
  white-space: pre-wrap;
}

.message-assistant .bubble {
  background-color: var(--chat-assistant-bg);
  color: var(--chat-assistant-text);
  border-top-left-radius: 2px;
  border: 1px solid var(--border-color);
  padding: 16px; /* AI 回复由于可能有代码块等，内边距加大 */
}

/* 覆盖 github-markdown-css 默认样式，使其融入聊天气泡 */
.custom-markdown {
  background-color: transparent !important;
  font-size: 15px !important;
}
.custom-markdown :deep(p:last-child) {
  margin-bottom: 0;
}

.bubble.is-loading {
  color: var(--text-secondary);
  font-style: italic;
}

.bubble.is-error {
  background-color: #fef0f0;
  color: #f56c6c;
  border-color: #fde2e2;
}

.message-metrics {
  margin-top: 8px;
  display: flex;
  gap: 8px;
}

.metric-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  border-radius: 6px;
  background-color: transparent;
}

.typing-indicator span {
  animation: blink 1.4s infinite both;
  font-size: 20px;
  line-height: 1;
}
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes blink {
  0% { opacity: 0.2; }
  20% { opacity: 1; }
  100% { opacity: 0.2; }
}

.chat-footer {
  padding: 16px 24px 24px;
  display: flex;
  justify-content: center;
  background: linear-gradient(to top, var(--bg-color) 80%, transparent);
}

.input-container {
  width: 100%;
  max-width: 800px;
  position: relative;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border-color);
  transition: box-shadow 0.3s ease;
}

.input-container:focus-within {
  box-shadow: 0 4px 20px rgba(0, 102, 204, 0.15);
  border-color: #b3d4f5;
}

.custom-input :deep(.el-textarea__inner) {
  border: none !important;
  box-shadow: none !important;
  padding: 16px 60px 16px 16px;
  background-color: transparent;
  font-size: 15px;
  line-height: 1.5;
}

.input-actions {
  position: absolute;
  right: 12px;
  bottom: 12px;
}

.send-btn {
  width: 36px;
  height: 36px;
}
</style>
