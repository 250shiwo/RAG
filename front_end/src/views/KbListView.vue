<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Document, ChatDotRound, Delete, Refresh, FolderOpened } from '@element-plus/icons-vue'

import { createKb, deleteKb, listKbs } from '../api/kb'

const router = useRouter()

const loading = ref(false)
const items = ref([])

const createDialogOpen = ref(false)
const createFormRef = ref()
const createLoading = ref(false)

const createForm = reactive({
  name: '',
  description: '',
})

const createRules = {
  name: [{ required: true, message: '请输入知识库名称', trigger: 'blur' }],
}

async function refresh() {
  loading.value = true
  try {
    items.value = await listKbs()
  } catch (e) {
    ElMessage.error('加载知识库列表失败')
  } finally {
    loading.value = false
  }
}

function openCreate() {
  createDialogOpen.value = true
}

async function submitCreate() {
  if (!createFormRef.value) return
  await createFormRef.value.validate()

  createLoading.value = true
  try {
    await createKb({ name: createForm.name, description: createForm.description })
    ElMessage.success('创建成功')
    createDialogOpen.value = false
    createForm.name = ''
    createForm.description = ''
    await refresh()
  } catch (e) {
    const msg = e?.response?.data?.detail || '创建失败'
    ElMessage.error(msg)
  } finally {
    createLoading.value = false
  }
}

async function onDelete(row) {
  try {
    await ElMessageBox.confirm(`确认删除知识库 “${row.name}” 吗？删除后无法恢复。`, '危险操作', {
      type: 'error',
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      confirmButtonClass: 'el-button--danger'
    })
  } catch {
    return
  }

  try {
    await deleteKb(row.id)
    ElMessage.success('删除成功')
    await refresh()
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

function toDocuments(row) {
  router.push(`/kb/${row.id}/documents`)
}

function toChat(row) {
  router.push(`/kb/${row.id}/chat`)
}

// 格式化日期
function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  refresh()
})
</script>

<template>
  <div class="page-container">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="header-left">
        <h1 class="page-title">知识库空间</h1>
        <p class="page-subtitle">管理您的私有数据，构建专属 AI 知识大脑</p>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" circle @click="refresh" :loading="loading" />
        <el-button type="primary" :icon="Plus" @click="openCreate">新建知识库</el-button>
      </div>
    </header>

    <!-- 知识库列表 -->
    <main class="page-content" v-loading="loading">
      <div v-if="items.length === 0 && !loading" class="empty-state">
        <el-icon class="empty-icon"><FolderOpened /></el-icon>
        <h3>暂无知识库</h3>
        <p>创建一个知识库并上传文档，即可开始智能问答</p>
        <el-button type="primary" :icon="Plus" @click="openCreate">立即创建</el-button>
      </div>

      <div v-else class="kb-grid">
        <div v-for="item in items" :key="item.id" class="kb-card">
          <div class="kb-card-header">
            <h3 class="kb-name">{{ item.name }}</h3>
            <el-dropdown trigger="click">
              <span class="more-btn">•••</span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="onDelete(item)" class="danger-text">
                    <el-icon><Delete /></el-icon>删除知识库
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          
          <div class="kb-card-body">
            <p class="kb-desc">{{ item.description || '暂无描述' }}</p>
            <div class="kb-meta">
              <span>创建于 {{ formatDate(item.created_at) }}</span>
            </div>
          </div>
          
          <div class="kb-card-footer">
            <el-button class="action-btn" plain @click="toDocuments(item)">
              <el-icon><Document /></el-icon>文档管理
            </el-button>
            <el-button class="action-btn primary-btn" type="primary" @click="toChat(item)">
              <el-icon><ChatDotRound /></el-icon>智能问答
            </el-button>
          </div>
        </div>
      </div>
    </main>

    <!-- 创建弹窗 -->
    <el-dialog v-model="createDialogOpen" title="新建知识库" width="520px" class="custom-dialog">
      <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-width="80px" label-position="top">
        <el-form-item label="知识库名称" prop="name">
          <el-input v-model="createForm.name" placeholder="例如：产品操作手册、公司规章制度" />
        </el-form-item>
        <el-form-item label="描述 (可选)" prop="description">
          <el-input v-model="createForm.description" type="textarea" :rows="4" placeholder="简要描述该知识库的用途和内容范围..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="createDialogOpen = false">取消</el-button>
          <el-button type="primary" :loading="createLoading" @click="submitCreate">确认创建</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.page-container {
  padding: 32px 40px;
  height: 100%;
  box-sizing: border-box;
  overflow-y: auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: var(--text-primary);
}

.page-subtitle {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.header-right {
  display: flex;
  gap: 12px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  background-color: white;
  border-radius: 16px;
  border: 1px dashed var(--border-color);
}

.empty-icon {
  font-size: 64px;
  color: #dcdfe6;
  margin-bottom: 24px;
}

.empty-state h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  color: var(--text-primary);
}

.empty-state p {
  margin: 0 0 24px 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.kb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.kb-card {
  background-color: white;
  border-radius: 16px;
  border: 1px solid var(--border-color);
  padding: 24px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.kb-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  border-color: #c6e2ff;
  transform: translateY(-2px);
}

.kb-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.kb-name {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.more-btn {
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  line-height: 1;
}

.more-btn:hover {
  background-color: var(--bg-color);
  color: var(--text-primary);
}

.kb-card-body {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.kb-desc {
  margin: 0 0 16px 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 44px; /* 固定高度保持对齐 */
}

.kb-meta {
  font-size: 12px;
  color: #a8abb2;
  margin-bottom: 20px;
}

.kb-card-footer {
  display: flex;
  gap: 12px;
  border-top: 1px solid var(--bg-color);
  padding-top: 16px;
}

.action-btn {
  flex: 1;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.danger-text {
  color: #f56c6c;
}
.danger-text:hover {
  background-color: #fef0f0 !important;
  color: #f56c6c !important;
}

/* 弹窗自定义样式覆盖 */
:deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
}
:deep(.el-dialog__header) {
  margin: 0;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
}
:deep(.el-dialog__body) {
  padding: 24px;
}
:deep(.el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid var(--border-color);
}
</style>

