import { ref } from 'vue'

const ACCESS_TOKEN_KEY = 'rag_access_token'
const REFRESH_TOKEN_KEY = 'rag_refresh_token'
const CURRENT_USER_KEY = 'rag_current_user'

function readStorage(key) {
  if (typeof localStorage === 'undefined') return ''
  return localStorage.getItem(key) || ''
}

function readCurrentUserFromStorage() {
  if (typeof localStorage === 'undefined') return null

  const raw = localStorage.getItem(CURRENT_USER_KEY)
  if (!raw) return null

  try {
    return JSON.parse(raw)
  } catch {
    localStorage.removeItem(CURRENT_USER_KEY)
    return null
  }
}

// 用响应式状态保存当前用户，便于菜单按角色实时切换。
export const currentUserState = ref(readCurrentUserFromStorage())

export function getAccessToken() {
  return readStorage(ACCESS_TOKEN_KEY)
}

export function getRefreshToken() {
  return readStorage(REFRESH_TOKEN_KEY)
}

export function hasAccessToken() {
  return Boolean(getAccessToken())
}

export function setTokens({ access, refresh }) {
  if (typeof access === 'string') localStorage.setItem(ACCESS_TOKEN_KEY, access)
  if (typeof refresh === 'string') localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
}

export function getCurrentUser() {
  return currentUserState.value
}

export function setCurrentUser(user) {
  if (!user || typeof user !== 'object') return

  currentUserState.value = user
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(user))
  }
}

export function isAdminUser() {
  return Boolean(currentUserState.value?.is_staff)
}

export function clearCurrentUser() {
  currentUserState.value = null
  if (typeof localStorage !== 'undefined') {
    localStorage.removeItem(CURRENT_USER_KEY)
  }
}

export function clearTokens() {
  if (typeof localStorage !== 'undefined') {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
  }
  clearCurrentUser()
}
