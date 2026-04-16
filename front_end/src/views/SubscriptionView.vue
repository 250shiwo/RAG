<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getSubscriptionPlans, getUserSubscription, getUserUsage, subscribeToPlan } from '../api/users'

const plans = ref([])
const userSubscription = ref(null)
const userUsage = ref(null)
const loading = ref(false)
const subscribing = ref(false)

async function loadData() {
  loading.value = true
  try {
    const [plansData, subscriptionData, usageData] = await Promise.all([
      getSubscriptionPlans(),
      getUserSubscription(),
      getUserUsage()
    ])
    plans.value = plansData
    userSubscription.value = subscriptionData
    userUsage.value = usageData
  } catch (error) {
    ElMessage.error('获取订阅信息失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function handleSubscribe(planId) {
  subscribing.value = true
  try {
    await subscribeToPlan(planId)
    ElMessage.success('订阅成功')
    await loadData()
  } catch (error) {
    ElMessage.error('订阅失败，请重试')
    console.error(error)
  } finally {
    subscribing.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="subscription-container">
    <el-card class="subscription-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <h2>订阅管理</h2>
          <div class="current-usage" v-if="userUsage">
            <el-tag size="small" :type="userUsage.remaining > 0 ? 'success' : 'danger'">
              今日剩余: {{ userUsage.remaining }}/{{ userUsage.daily_limit }}次
            </el-tag>
          </div>
        </div>
      </template>

      <div class="current-subscription" v-if="userSubscription">
        <h3>当前订阅</h3>
        <el-empty v-if="!userSubscription.plan" description="您当前使用的是免费版">
          <template #description>
            <p>免费版限制：每日5次问答，最多1个知识库</p>
          </template>
        </el-empty>
        <el-card v-else class="current-plan-card">
          <div class="plan-info">
            <h4>{{ userSubscription.plan.name }}</h4>
            <p class="plan-price">¥{{ userSubscription.plan.price }}/月</p>
            <div class="plan-features">
              <el-descriptions :column="2" border>
                <el-descriptions-item label="每日问答次数">{{ userSubscription.plan.daily_chat_limit }}次</el-descriptions-item>
                <el-descriptions-item label="最大知识库数">{{ userSubscription.plan.max_knowledge_bases }}个</el-descriptions-item>
                <el-descriptions-item label="订阅状态" :span="2">
                  <el-tag type="success" v-if="userSubscription.is_active">已激活</el-tag>
                  <el-tag type="warning" v-else>已过期</el-tag>
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </el-card>
      </div>

      <div class="subscription-plans" v-if="plans.length > 0">
        <h3 class="plans-title">订阅计划</h3>
        <div class="plans-grid">
          <el-card 
            v-for="plan in plans" 
            :key="plan.id"
            class="plan-card"
            :class="{ 'current-plan': userSubscription?.plan?.id === plan.id }"
          >
            <div class="plan-header">
              <h4>{{ plan.name }}</h4>
              <p class="plan-price">¥{{ plan.price }}/月</p>
            </div>
            <div class="plan-features">
              <el-descriptions :column="1" border>
                <el-descriptions-item label="每日问答次数">{{ plan.daily_chat_limit }}次</el-descriptions-item>
                <el-descriptions-item label="最大知识库数">{{ plan.max_knowledge_bases }}个</el-descriptions-item>
              </el-descriptions>
            </div>
            <div class="plan-actions">
              <el-button 
                type="primary" 
                :disabled="userSubscription?.plan?.id === plan.id && userSubscription.is_active"
                @click="handleSubscribe(plan.id)"
                :loading="subscribing"
              >
                {{ userSubscription?.plan?.id === plan.id && userSubscription.is_active ? '当前计划' : '立即订阅' }}
              </el-button>
            </div>
          </el-card>
        </div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.subscription-container {
  padding: 24px;
  min-height: 100vh;
  background-color: var(--bg-color);
}

.subscription-card {
  max-width: 1000px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 24px;
  color: var(--text-primary);
}

.current-usage {
  display: flex;
  align-items: center;
}

.current-subscription {
  margin-bottom: 32px;
}

.current-subscription h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
  color: var(--text-primary);
}

.current-plan-card {
  border: 1px solid #e6f0fa;
  border-radius: 8px;
  background-color: #f8faff;
}

.plan-info h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: var(--text-primary);
}

.plan-price {
  margin: 0 0 16px 0;
  font-size: 20px;
  font-weight: bold;
  color: var(--primary-color);
}

.plans-title {
  margin: 0 0 16px 0;
  font-size: 18px;
  color: var(--text-primary);
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.plan-card {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.plan-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.plan-card.current-plan {
  border: 2px solid var(--primary-color);
  box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.1);
}

.plan-header {
  margin-bottom: 16px;
}

.plan-header h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: var(--text-primary);
}

.plan-features {
  margin-bottom: 24px;
}

.plan-actions {
  text-align: center;
}

.plan-actions .el-button {
  width: 100%;
}
</style>