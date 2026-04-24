<template>
  <div class="chat-history-view">
    <el-card shadow="never" class="card">
      <template #header>
        <div class="card-header">
          <span>历史对话记录</span>
        </div>
      </template>
      
      <div v-if="loading" class="loading-container">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>加载中...</span>
      </div>
      
      <div v-else-if="error" class="error-container">
        <el-alert
          :title="error"
          type="error"
          show-icon
          :closable="false"
        />
      </div>
      
      <div v-else-if="historyList.length === 0" class="empty-container">
        <el-empty description="暂无历史对话" />
      </div>
      
      <div v-else class="history-list">
        <el-timeline>
          <el-timeline-item
            v-for="item in historyList"
            :key="item.id"
            :timestamp="formatDate(item.created_at)"
            type="primary"
            placement="top"
          >
            <el-card shadow="hover" class="history-item" @click="viewHistoryDetail(item.id)">
              <div class="history-item-header">
                <span class="knowledge-base">{{ item.knowledge_base_name || '默认知识库' }}</span>
                <el-button
                  size="small"
                  type="danger"
                  plain
                  @click.stop="deleteHistory(item.id)"
                >
                  <el-icon><Delete /></el-icon>
                  删除
                </el-button>
              </div>
              <div class="history-item-content">
                <div class="question">{{ item.question }}</div>
                <div class="answer">{{ truncateText(item.answer, 100) }}</div>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-card>
    
    <!-- 对话详情弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      title="对话详情"
      width="600px"
    >
      <div v-if="historyDetail" class="history-detail">
        <div class="detail-item">
          <span class="label">知识库：</span>
          <span class="value">{{ historyDetail.knowledge_base_name || '默认知识库' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">提问时间：</span>
          <span class="value">{{ formatDate(historyDetail.created_at) }}</span>
        </div>
        <div class="detail-item">
          <span class="label">问题：</span>
          <div class="value content">{{ historyDetail.question }}</div>
        </div>
        <div class="detail-item">
          <span class="label">回答：</span>
          <div class="value content">{{ historyDetail.answer }}</div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading, Delete } from '@element-plus/icons-vue'
import { getChatHistoryList, getChatHistoryDetail, deleteChatHistory } from '../api/rag'

const loading = ref(false)
const error = ref('')
const historyList = ref([])
const dialogVisible = ref(false)
const historyDetail = ref(null)

// 加载历史对话列表
const loadHistoryList = async () => {
  loading.value = true
  error.value = ''
  try {
    const data = await getChatHistoryList()
    historyList.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || '加载历史对话失败'
  } finally {
    loading.value = false
  }
}

// 查看对话详情
const viewHistoryDetail = async (historyId) => {
  try {
    const data = await getChatHistoryDetail(historyId)
    historyDetail.value = data
    dialogVisible.value = true
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '加载对话详情失败')
  }
}

// 删除对话
const deleteHistory = async (historyId) => {
  try {
    await deleteChatHistory(historyId)
    ElMessage.success('删除成功')
    loadHistoryList()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '删除失败')
  }
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 截断文本
const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

// 组件挂载时加载历史对话列表
onMounted(() => {
  loadHistoryList()
})
</script>

<style scoped>
.chat-history-view {
  padding: 20px;
}

.card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
  color: #606266;
}

.loading-container .el-icon {
  margin-right: 10px;
}

.error-container {
  margin: 20px 0;
}

.empty-container {
  padding: 40px 0;
}

.history-list {
  margin-top: 20px;
}

.history-item {
  cursor: pointer;
  transition: all 0.3s;
}

.history-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.history-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.knowledge-base {
  font-size: 14px;
  color: #409EFF;
  font-weight: 500;
}

.history-item-content {
  margin-top: 10px;
}

.question {
  font-weight: 500;
  margin-bottom: 8px;
  color: #303133;
}

.answer {
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
}

.history-detail {
  padding: 10px 0;
}

.detail-item {
  margin-bottom: 16px;
}

.label {
  font-weight: 500;
  color: #303133;
  margin-right: 10px;
}

.value {
  color: #606266;
}

.content {
  margin-top: 8px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  line-height: 1.5;
  white-space: pre-wrap;
}
</style>