import { api } from '../services/api'

export async function listDocuments(kbId) {
  const resp = await api.get(`/api/knowledge/${kbId}/documents`)
  return resp.data?.items || []
}

export async function uploadDocument({ kbId, file, onConflict }) {
  const form = new FormData()
  form.append('kb_id', String(kbId))
  form.append('file', file)
  if (onConflict) form.append('on_conflict', onConflict)

  const resp = await api.post('/api/knowledge/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return resp.data
}

export async function deleteDocument(docId) {
  await api.delete(`/api/knowledge/document/${docId}`)
}

export async function previewDocument(docId) {
  const resp = await api.get(`/api/knowledge/document/${docId}/preview`)
  return resp.data
}

