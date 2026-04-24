<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, ElDialog } from 'element-plus'
import { UploadFilled, Back, Refresh, Delete, Document, View } from '@element-plus/icons-vue'

import { deleteDocument, listDocuments, uploadDocument, previewDocument } from '../api/documents'

const route = useRoute()
const router = useRouter()
const kbId = Number(route.params.kbId)

const loading = ref(false)
const items = ref([])

const selectedFile = ref(null)
const onConflict = ref('keep')
const uploading = ref(false)
const uploadRef = ref(null)

// 文档预览相关
const previewDialogVisible = ref(false)
const previewLoading = ref(false)
const previewContent = ref('')
const previewFilename = ref('')

// 允许上传的文件类型（前端校验仅做体验优化，后端仍会做兜底校验）
const ALLOWED_SUFFIXES = ['.txt', '.md', '.pdf']

function isAllowedFile(file) {
  const name = (file?.name || '').toLowerCase()
  return ALLOWED_SUFFIXES.some((suf) => name.endsWith(suf))
}

async function refresh() {
  loading.value = true
  try {
    items.value = await listDocuments(kbId)
  } catch (e) {
    ElMessage.error('加载文档列表失败')
  } finally {
    loading.value = false
  }
}

function onFileChange(uploadFile) {
  const raw = uploadFile?.raw || null
  if (!raw) {
    selectedFile.value = null
    return
  }
  if (!isAllowedFile(raw)) {
    ElMessage.error('仅支持上传 .txt / .md / .pdf 文件')
    selectedFile.value = null
    uploadRef.value?.clearFiles?.()
    return
  }
  selectedFile.value = raw
}

async function doUpload() {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }

  uploading.value = true
  try {
    await uploadDocument({ kbId, file: selectedFile.value, onConflict: onConflict.value })
    ElMessage.success('上传成功')
    selectedFile.value = null
    await refresh()
  } catch (e) {
    const msg = e?.response?.data?.detail || '上传失败'
    ElMessage.error(msg)
  } finally {
    uploading.value = false
  }
}

async function onDelete(row) {
  try {
    await ElMessageBox.confirm(`确认删除文档 “${row.filename}” 吗？删除后将影响该文档的问答功能。`, '危险操作', {
      type: 'error',
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      confirmButtonClass: 'el-button--danger'
    })
  } catch {
    return
  }

  try {
    await deleteDocument(row.id)
    ElMessage.success('删除成功')
    await refresh()
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

// 预览文档
async function onPreview(row) {
  previewLoading.value = true
  previewContent.value = ''
  previewFilename.value = row.filename
  try {
    const data = await previewDocument(row.id)
    previewContent.value = data.content
    previewDialogVisible.value = true
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '预览失败')
  } finally {
    previewLoading.value = false
  }
}

function goBack() {
  router.push('/kb')
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
        <el-button :icon="Back" circle plain @click="goBack" class="back-btn" />
        <div>
          <h1 class="page-title">文档管理 (KB {{ kbId }})</h1>
          <p class="page-subtitle">上传文档并自动解析，丰富知识库内容</p>
        </div>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" plain @click="refresh" :loading="loading">刷新列表</el-button>
      </div>
    </header>

    <!-- 上传区域 -->
    <section class="upload-section">
      <div class="upload-card">
        <el-upload 
          ref="uploadRef"
          class="custom-upload"
          drag
          :auto-upload="false" 
          :show-file-list="true" 
          :limit="1" 
          accept=".txt,.md,.pdf"
          :on-change="onFileChange"
        >
          <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
          <div class="el-upload__text">
            将文件拖到此处，或 <em>点击选择文件</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持 txt, md, pdf 等格式文件，单文件大小不超过 20MB
            </div>
          </template>
        </el-upload>
        
        <div class="upload-actions">
          <div class="action-group">
            <span class="action-label">重名策略：</span>
            <el-radio-group v-model="onConflict" class="custom-radio">
              <el-radio-button label="keep">保留两者</el-radio-button>
              <el-radio-button label="replace">覆盖原文件</el-radio-button>
            </el-radio-group>
          </div>
          <el-button 
            type="primary" 
            size="large"
            :loading="uploading" 
            :disabled="!selectedFile"
            @click="doUpload"
            class="upload-btn"
          >
            开始上传入库
          </el-button>
        </div>
      </div>
    </section>

    <!-- 文档列表 -->
    <section class="list-section">
      <h3 class="section-title">已上传文档 ({{ items.length }})</h3>
      
      <el-table 
        :data="items" 
        v-loading="loading" 
        style="width: 100%" 
        class="custom-table"
        :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: '600' }"
      >
        <el-table-column label="文件名" min-width="300">
          <template #default="{ row }">
            <div class="file-name-cell">
              <el-icon class="file-icon"><Document /></el-icon>
              <span>{{ row.filename }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="chunk_count" label="分块数量" width="120" align="center">
          <template #default="{ row }">
            <el-tag size="small" type="info">{{ row.chunk_count }} 块</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="uploaded_at" label="上传时间" min-width="200">
          <template #default="{ row }">
            {{ formatDate(row.uploaded_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" plain :icon="View" @click="onPreview(row)">预览</el-button>
            <el-button size="small" type="danger" plain :icon="Delete" @click="onDelete(row)">删除</el-button>
          </template>
        </el-table-column>
        
        <template #empty>
          <el-empty description="暂无文档，请在上方上传" />
        </template>
      </el-table>
    </section>
    
    <!-- 文档预览弹窗 -->
    <el-dialog
      v-model="previewDialogVisible"
      :title="`文档预览 - ${previewFilename}`"
      width="800px"
      :fullscreen="false"
    >
      <div v-if="previewLoading" class="preview-loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>加载中...</span>
      </div>
      <div v-else class="preview-content">
        <pre>{{ previewContent }}</pre>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
.page-container {
  padding: 32px 40px;
  height: 100%;
  box-sizing: border-box;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  font-size: 18px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: var(--text-primary);
}

.page-subtitle {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.upload-section {
  width: 100%;
}

.upload-card {
  background-color: white;
  border-radius: 16px;
  border: 1px solid var(--border-color);
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.custom-upload :deep(.el-upload-dragger) {
  border-radius: 12px;
  background-color: #f8fafc;
  transition: all 0.3s ease;
}

.custom-upload :deep(.el-upload-dragger:hover) {
  background-color: #f0f5ff;
  border-color: var(--primary-color);
}

.upload-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px dashed var(--border-color);
}

.action-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.action-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.upload-btn {
  padding: 0 32px;
  font-weight: 600;
  border-radius: 8px;
}

.list-section {
  background-color: white;
  border-radius: 16px;
  border: 1px solid var(--border-color);
  padding: 24px;
  flex-grow: 1;
}

.section-title {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.custom-table {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.file-name-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 500;
  color: var(--text-primary);
}

.file-icon {
  font-size: 18px;
  color: #909399;
}

.preview-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
  color: #606266;
}

.preview-loading .el-icon {
  margin-right: 10px;
}

.preview-content {
  max-height: 600px;
  overflow-y: auto;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.preview-content pre {
  margin: 0;
  white-space: pre-wrap;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  color: #303133;
}
</style>
