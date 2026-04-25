import { api } from '../services/api'

export async function listAdminUsers(params) {
  const resp = await api.get('/api/admin/users', { params })
  return resp.data.items || []
}

export async function createAdminUser(data) {
  const resp = await api.post('/api/admin/users', data)
  return resp.data
}

export async function updateAdminUser(id, data) {
  const resp = await api.patch(`/api/admin/users/${id}`, data)
  return resp.data
}

export async function deleteAdminUser(id) {
  await api.delete(`/api/admin/users/${id}`)
}

export async function listAdminKbs(params) {
  const resp = await api.get('/api/admin/kb', { params })
  return resp.data.items || []
}

export async function createAdminKb(data) {
  const resp = await api.post('/api/admin/kb', data)
  return resp.data
}

export async function updateAdminKb(id, data) {
  const resp = await api.patch(`/api/admin/kb/${id}`, data)
  return resp.data
}

export async function deleteAdminKb(id) {
  await api.delete(`/api/admin/kb/${id}`)
}

export async function listAdminKbDocuments(kbId) {
  const resp = await api.get(`/api/admin/kb/${kbId}/documents`)
  return resp.data.items || []
}

export async function deleteAdminDocument(id) {
  await api.delete(`/api/admin/document/${id}`)
}

export async function fetchAdminStats() {
  // 读取管理员统计看板的真实数据。
  const resp = await api.get('/api/admin/stats')
  return resp.data
}
