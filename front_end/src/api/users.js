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

