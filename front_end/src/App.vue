<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterView } from 'vue-router'
import { DataAnalysis, DataBoard, Document, ChatLineRound, SwitchButton, User, Files, CreditCard } from '@element-plus/icons-vue'
import { fetchCurrentUserProfile } from './api/users'
import { clearCurrentUser, clearTokens, currentUserState, hasAccessToken, isAdminUser, setCurrentUser } from './services/auth'

const route = useRoute()
const router = useRouter()

const requiresAuth = computed(() => Boolean(route.meta?.requiresAuth))
const kbId = computed(() => route.params?.kbId)
const currentUser = computed(() => currentUserState.value)
const adminVisible = computed(() => isAdminUser())

// 退出登录函数
function logout() {
  clearTokens()
  router.push('/login')
}

onMounted(async () => {
  if (!hasAccessToken() || currentUser.value) return

  try {
    // 页面刷新后恢复当前用户信息，保证菜单按角色正确显示。
    const profile = await fetchCurrentUserProfile()
    setCurrentUser(profile)
  } catch (error) {
    clearCurrentUser()
    console.error(error)
  }
})
</script>

<template>
  <RouterView v-if="!requiresAuth" />
  <el-container v-else class="app-container">
    <!-- 左侧边栏 -->
    <el-aside width="260px" class="sidebar">
      <div class="logo-area">
        <div class="logo-icon">R</div>
        <span class="logo-text">RAG 智能助手</span>
      </div>
      <el-menu 
        :default-active="$route.path" 
        router 
        class="custom-menu"
        :collapse-transition="false"
      >
        <el-menu-item index="/kb">
          <el-icon><DataBoard /></el-icon>
          <span>知识库列表</span>
        </el-menu-item>
        <div v-if="kbId" class="menu-divider"></div>
        <el-menu-item v-if="kbId" :index="`/kb/${kbId}/documents`">
          <el-icon><Document /></el-icon>
          <span>文档管理</span>
        </el-menu-item>
        <el-menu-item v-if="kbId" :index="`/kb/${kbId}/chat`">
          <el-icon><ChatLineRound /></el-icon>
          <span>智能问答</span>
        </el-menu-item>

        <div class="menu-divider"></div>
        <el-menu-item index="/profile">
          <el-icon><User /></el-icon>
          <span>个人信息</span>
        </el-menu-item>
        <el-menu-item index="/subscription">
          <el-icon><CreditCard /></el-icon>
          <span>订阅套餐</span>
        </el-menu-item>
        <el-menu-item index="/chat-history">
          <el-icon><ChatLineRound /></el-icon>
          <span>历史对话</span>
        </el-menu-item>

        <template v-if="adminVisible">
          <div class="menu-divider"></div>
          <div class="menu-group-title">管理员专区</div>
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/kbs">
            <el-icon><Files /></el-icon>
            <span>全局知识库</span>
          </el-menu-item>
          <el-menu-item index="/admin/stats">
            <el-icon><DataAnalysis /></el-icon>
            <span>系统统计</span>
          </el-menu-item>
        </template>
      </el-menu>
      
      <!-- 底部用户信息或退出登录 -->
      <div class="sidebar-footer">
        <div v-if="currentUser" class="user-summary">
          <div class="user-name">{{ currentUser.username }}</div>
          <div class="user-role">{{ currentUser.is_staff ? '管理员' : '普通用户' }}</div>
        </div>
        <el-button v-if="hasAccessToken()" class="logout-btn" type="danger" text @click="logout">
          <el-icon><SwitchButton /></el-icon>
          退出登录
        </el-button>
      </div>
    </el-aside>
    
    <!-- 右侧主体内容 -->
    <el-container class="main-container">
      <!-- 隐藏原生 Header，在各个页面内部实现更定制化的 Header -->
      <el-main class="main-content">
        <RouterView />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.app-container {
  height: 100vh;
  width: 100vw;
  background-color: var(--bg-color);
}

.sidebar {
  background-color: var(--bg-sidebar);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.logo-area {
  padding: 24px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #0066cc, #004499);
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.custom-menu {
  border-right: none;
  background-color: transparent;
  flex-grow: 1;
  padding: 0 12px;
}

.custom-menu .el-menu-item {
  height: 48px;
  line-height: 48px;
  border-radius: 8px;
  margin-bottom: 8px;
  color: var(--text-secondary);
  font-weight: 500;
}

.custom-menu .el-menu-item:hover {
  background-color: var(--bg-color);
  color: var(--text-primary);
}

.custom-menu .el-menu-item.is-active {
  background-color: #e6f0fa;
  color: var(--primary-color);
  font-weight: 600;
}

.menu-divider {
  height: 1px;
  background-color: var(--border-color);
  margin: 16px 8px;
}

.menu-group-title {
  padding: 0 16px;
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 8px;
  margin-top: 16px;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--border-color);
}

.user-summary {
  margin-bottom: 12px;
  padding: 12px;
  border-radius: 8px;
  background-color: var(--bg-color);
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.user-role {
  margin-top: 4px;
  font-size: 12px;
  color: var(--text-secondary);
}

.logout-btn {
  width: 100%;
  justify-content: flex-start;
  padding-left: 12px;
  border-radius: 8px;
  height: 44px;
}

.main-container {
  background-color: var(--bg-color);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.main-content {
  padding: 0;
  height: 100%;
  overflow: hidden; /* 由子组件负责滚动 */
}
</style>
