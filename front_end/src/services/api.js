import axios from 'axios'

import { clearTokens, getAccessToken, getRefreshToken, setTokens } from './auth'

const baseURL = import.meta.env.VITE_API_BASE_URL || ''

export const api = axios.create({
  baseURL,
  timeout: 20000,
})

api.interceptors.request.use((config) => {
  const token = getAccessToken()
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

let refreshPromise = null

async function refreshAccessToken() {
  if (refreshPromise) return refreshPromise

  const refresh = getRefreshToken()
  if (!refresh) return null

  refreshPromise = axios
    .post(
      `${baseURL}/api/users/refresh`,
      { refresh },
      { timeout: 20000 }
    )
    .then((resp) => {
      const access = resp?.data?.access
      if (typeof access === 'string' && access) {
        setTokens({ access })
        return access
      }
      return null
    })
    .catch(() => null)
    .finally(() => {
      refreshPromise = null
    })

  return refreshPromise
}

api.interceptors.response.use(
  (resp) => resp,
  async (error) => {
    const status = error?.response?.status
    const original = error?.config

    if (status === 401 && original && !original.__isRetryRequest) {
      original.__isRetryRequest = true
      const newAccess = await refreshAccessToken()
      if (newAccess) {
        original.headers = original.headers || {}
        original.headers.Authorization = `Bearer ${newAccess}`
        return api.request(original)
      }

      clearTokens()
      if (window.location.pathname !== '/login') {
        window.location.assign('/login')
      }
    }

    return Promise.reject(error)
  }
)

