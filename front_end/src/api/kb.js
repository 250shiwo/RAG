import { api } from '../services/api'

export async function listKbs() {
  const resp = await api.get('/api/kb/list')
  return resp.data?.items || []
}

export async function createKb({ name, description }) {
  const resp = await api.post('/api/kb/create', { name, description })
  return resp.data
}

export async function deleteKb(kbId) {
  await api.delete(`/api/kb/${kbId}`)
}

