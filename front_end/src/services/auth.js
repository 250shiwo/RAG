const ACCESS_TOKEN_KEY = 'rag_access_token'
const REFRESH_TOKEN_KEY = 'rag_refresh_token'

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY) || ''
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY) || ''
}

export function hasAccessToken() {
  return Boolean(getAccessToken())
}

export function setTokens({ access, refresh }) {
  if (typeof access === 'string') localStorage.setItem(ACCESS_TOKEN_KEY, access)
  if (typeof refresh === 'string') localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

