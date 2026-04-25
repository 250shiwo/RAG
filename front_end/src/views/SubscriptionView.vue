<script setup>
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { getSubscriptionPlans, getUserSubscription, getUserUsage, createAlipayOrder } from '../api/users'

const route = useRoute()
const router = useRouter()
const plans = ref([])
const userSubscription = ref(null)
const userUsage = ref(null)
const loading = ref(false)
const subscribingPlanId = ref(null)

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
  subscribingPlanId.value = planId
  try {
    const result = await createAlipayOrder(planId)

    if (!result?.pay_url || typeof result.pay_url !== 'string') {
      throw new Error('未获取到支付链接')
    }

    // 使用 assign 直接跳转当前页，避免部分浏览器对 href 赋值场景处理不稳定。
    window.location.assign(result.pay_url)
  } catch (error) {
    ElMessage.error('创建支付订单失败，请重试')
    console.error(error)
  } finally {
    subscribingPlanId.value = null
  }
}

async function handleReturnResult() {
  const paid = route.query.paid
  const orderId = route.query.order_id

  if (paid !== '1') return

  // 支付回跳后主动刷新一次订阅数据，避免页面继续显示旧套餐。
  await loadData()
  ElMessage.success(orderId ? `支付成功，订单 ${orderId} 已更新` : '支付成功，订阅信息已更新')

  // 清理地址栏参数，避免刷新页面时重复提示。
  router.replace({ path: route.path })
}

onMounted(() => {
  loadData()
  handleReturnResult()
})

watch(
  () => route.query.paid,
  () => {
    handleReturnResult()
  }
)
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
                <el-descriptions-item label="剩余天数" :span="2">
                  <el-tag type="info" effect="plain">{{ userSubscription.remaining_days }}天</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="开始日期" :span="2">{{ userSubscription.start_date }}</el-descriptions-item>
                <el-descriptions-item label="结束日期" :span="2">{{ userSubscription.end_date }}</el-descriptions-item>
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
                :loading="subscribingPlanId === plan.id"
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
