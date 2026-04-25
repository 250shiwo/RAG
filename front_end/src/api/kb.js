import { api } from '../services/api'

export async function listKbs() {
  const resp = await api.get('/api/knowledge/list')
  return resp.data?.items || []
}

export async function createKb({ name, description }) {
  const resp = await api.post('/api/knowledge/create', { name, description })
  return resp.data
}

export async function deleteKb(kbId) {
  await api.delete(`/api/knowledge/${kbId}`)
}

