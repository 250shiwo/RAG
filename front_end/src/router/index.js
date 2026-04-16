import { createRouter, createWebHistory } from 'vue-router'

import ChatView from '../views/ChatView.vue'
import KbDocumentsView from '../views/KbDocumentsView.vue'
import KbListView from '../views/KbListView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import SubscriptionView from '../views/SubscriptionView.vue'
import AdminUsersView from '../views/admin/AdminUsersView.vue'
import AdminKbsView from '../views/admin/AdminKbsView.vue'
import { hasAccessToken } from '../services/auth'

const routes = [
  { path: '/', redirect: '/kb' },
  { path: '/login', component: LoginView, meta: { requiresAuth: false, title: '登录' } },
  { path: '/register', component: RegisterView, meta: { requiresAuth: false, title: '注册' } },
  { path: '/kb', component: KbListView, meta: { requiresAuth: true, title: '知识库' } },
  { path: '/kb/:kbId/documents', component: KbDocumentsView, meta: { requiresAuth: true, title: '文档' } },
  { path: '/kb/:kbId/chat', component: ChatView, meta: { requiresAuth: true, title: '问答' } },
  { path: '/subscription', component: SubscriptionView, meta: { requiresAuth: true, title: '订阅管理' } },
  { path: '/admin/users', component: AdminUsersView, meta: { requiresAuth: true, title: '用户管理' } },
  { path: '/admin/kbs', component: AdminKbsView, meta: { requiresAuth: true, title: '全局知识库' } },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  if (to.meta?.requiresAuth && !hasAccessToken()) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
  if ((to.path === '/login' || to.path === '/register') && hasAccessToken()) {
    return { path: '/kb' }
  }
  return true
})

export default router
