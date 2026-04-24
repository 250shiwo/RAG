<template>
  <div class="admin-stats-view">
    <el-card shadow="never" class="card">
      <template #header>
        <div class="card-header">
          <span>系统统计</span>
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
      
      <div v-else class="stats-container">
        <!-- 概览卡片 -->
        <div class="stats-overview">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-item">
              <div class="stat-value">{{ stats.users.total }}</div>
              <div class="stat-label">总用户数</div>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="stat-card">
            <div class="stat-item">
              <div class="stat-value">{{ stats.users.active }}</div>
              <div class="stat-label">活跃用户</div>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="stat-card">
            <div class="stat-item">
              <div class="stat-value">{{ stats.knowledge_bases.total }}</div>
              <div class="stat-label">知识库数</div>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="stat-card">
            <div class="stat-item">
              <div class="stat-value">{{ stats.documents.total }}</div>
              <div class="stat-label">文档数</div>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="stat-card">
            <div class="stat-item">
              <div class="stat-value">{{ stats.chats.total }}</div>
              <div class="stat-label">总对话数</div>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="stat-card">
            <div class="stat-item">
              <div class="stat-value">{{ stats.chats.today }}</div>
              <div class="stat-label">今日对话数</div>
            </div>
          </el-card>
        </div>
        
        <!-- 订阅统计 -->
        <div class="stats-section">
          <h3 class="section-title">订阅统计</h3>
          <el-card shadow="hover" class="section-card">
            <div v-if="stats.subscriptions.length === 0" class="empty-stats">
              <el-empty description="暂无订阅数据" />
            </div>
            <el-table
              v-else
              :data="stats.subscriptions"
              style="width: 100%"
            >
              <el-table-column prop="plan" label="订阅计划" width="180" />
              <el-table-column prop="user_count" label="用户数" width="180" />
            </el-table>
          </el-card>
        </div>
        
        <!-- 今日使用统计 -->
        <div class="stats-section">
          <h3 class="section-title">今日使用统计</h3>
          <el-card shadow="hover" class="section-card">
            <div class="today-stats">
              <div class="today-stat-item">
                <div class="today-stat-value">{{ stats.usage.today.total_users }}</div>
                <div class="today-stat-label">活跃用户</div>
              </div>
              <div class="today-stat-item">
                <div class="today-stat-value">{{ stats.usage.today.total_chats }}</div>
                <div class="today-stat-label">对话次数</div>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading, DataAnalysis, Users, Document, ChatLineRound, Subscription } from '@element-plus/icons-vue'

// 模拟数据，实际应该从API获取
const loading = ref(false)
const error = ref('')
const stats = ref({
  users: {
    total: 0,
    active: 0
  },
  knowledge_bases: {
    total: 0
  },
  documents: {
    total: 0
  },
  chats: {
    total: 0,
    today: 0
  },
  subscriptions: [],
  usage: {
    today: {
      total_users: 0,
      total_chats: 0
    }
  }
})

// 加载统计数据
const loadStats = async () => {
  loading.value = true
  error.value = ''
  try {
    // 实际项目中，这里应该调用API获取统计数据
    // const response = await api.get('/api/admin/stats')
    // stats.value = response.data
    
    // 模拟数据
    setTimeout(() => {
      stats.value = {
        users: {
          total: 100,
          active: 85
        },
        knowledge_bases: {
          total: 150
        },
        documents: {
          total: 500
        },
        chats: {
          total: 2000,
          today: 50
        },
        subscriptions: [
          { plan: '免费版', user_count: 80 },
          { plan: '¥9.9/月', user_count: 15 },
          { plan: '¥29.9/月', user_count: 5 }
        ],
        usage: {
          today: {
            total_users: 30,
            total_chats: 50
          }
        }
      }
      loading.value = false
    }, 1000)
  } catch (err) {
    error.value = err.response?.data?.detail || '加载统计数据失败'
    loading.value = false
  }
}

// 组件挂载时加载统计数据
onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.admin-stats-view {
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

.stats-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-card {
  border-radius: 8px;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.stats-section {
  margin-top: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.section-card {
  border-radius: 8px;
  padding: 20px;
}

.empty-stats {
  padding: 40px 0;
}

.today-stats {
  display: flex;
  gap: 40px;
}

.today-stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.today-stat-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 8px;
}

.today-stat-label {
  font-size: 14px;
  color: #606266;
}
</style>