import { api } from '../services/api'

export async function registerUser({ username, password, email }) {
  const resp = await api.post('/api/users/register', { username, password, email })
  return resp.data
}

export async function loginUser({ username, password }) {
  const resp = await api.post('/api/users/login', { username, password })
  return resp.data
}

export async function refreshAccess({ refresh }) {
  const resp = await api.post('/api/users/refresh', { refresh })
  return resp.data
}

export async function getMe() {
  const resp = await api.get('/api/users/me')
  return resp.data
}

export async function fetchCurrentUserProfile() {
  const resp = await api.get('/api/users/me')
  return resp.data
}

// 订阅相关API
export async function getSubscriptionPlans() {
  const resp = await api.get('/api/users/subscriptions/plans')
  return resp.data
}

export async function getUserSubscription() {
  const resp = await api.get('/api/users/subscriptions/me')
  return resp.data
}

export async function getUserUsage() {
  const resp = await api.get('/api/users/subscriptions/usage')
  return resp.data
}

export async function subscribeToPlan(planId) {
  const resp = await api.post('/api/users/subscriptions/subscribe', { plan_id: planId })
  return resp.data
}

// 支付相关API
export async function createAlipayOrder(planId) {
  const resp = await api.post('/api/payment/alipay', { plan_id: planId })
  return resp.data
}

// 用户信息管理API
export async function updateUserInfo(userData) {
  const resp = await api.put('/api/users/me', userData)
  return resp.data
}

export async function changePassword(oldPassword, newPassword) {
  const resp = await api.post('/api/users/change-password', { old_password: oldPassword, new_password: newPassword })
  return resp.data
}

