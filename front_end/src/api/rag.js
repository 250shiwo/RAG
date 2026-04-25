import { api } from '../services/api'
import { getAccessToken } from '../services/auth'

export async function ragChat({ kbId, question, session_id }) {
  // 问答可能耗时较长（检索 + 大模型生成），单独提高超时时间，避免 20s 默认超时导致前端误判失败
  const payload = { kb_id: kbId, question }
  // 首轮对话不传 session_id，让后端使用默认值生成会话。
  if (session_id) payload.session_id = session_id
  const resp = await api.post('/api/rag/chat', payload, { timeout: 120000 })
  return resp.data
}

export async function ragChatStream({ kbId, question, session_id, onDelta }) {
  const baseURL = import.meta.env.VITE_API_BASE_URL || ''
  const token = getAccessToken()
  const payload = { kb_id: kbId, question }
  // 首轮对话不传 session_id，让后端使用默认值生成会话。
  if (session_id) payload.session_id = session_id

  const resp = await fetch(`${baseURL}/api/rag/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(payload),
  })

  if (!resp.ok) {
    let detail = '问答失败'
    try {
      const data = await resp.json()
      if (typeof data?.detail === 'string') detail = data.detail
    } catch {}
    const err = new Error(detail)
    err.response = { data: { detail }, status: resp.status }
    throw err
  }

  if (!resp.body) {
    return { answer: '', session_id: resp.headers.get('X-Session-ID') }
  }

  const reader = resp.body.getReader()
  const decoder = new TextDecoder('utf-8')
  let answer = ''

  while (true) {
    const { value, done } = await reader.read()
    if (done) break
    const chunk = decoder.decode(value, { stream: true })
    if (chunk) {
      answer += chunk
      if (typeof onDelta === 'function') onDelta(chunk, answer)
    }
  }

  return { answer, session_id: resp.headers.get('X-Session-ID') }
}

export async function getChatHistoryList() {
  const resp = await api.get('/api/rag/history')
  return resp.data
}

export async function getChatHistoryDetail(historyId) {
  const resp = await api.get(`/api/rag/history/${historyId}`)
  return resp.data
}

export async function deleteChatHistory(historyId) {
  const resp = await api.delete(`/api/rag/history/${historyId}`)
  return resp.data
}
