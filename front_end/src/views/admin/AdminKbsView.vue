<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Edit, Delete, Refresh, Document } from '@element-plus/icons-vue'
import { listAdminKbs, createAdminKb, updateAdminKb, deleteAdminKb, listAdminKbDocuments, deleteAdminDocument } from '../../api/admin'

const loading = ref(false)
const kbs = ref([])
const searchUserId = ref('')

const dialogVisible = ref(false)
const dialogLoading = ref(false)
const formRef = ref()
const isEdit = ref(false)
const currentId = ref(null)

const form = reactive({
  user_id: null,
  name: '',
  description: ''
})

const rules = {
  user_id: [{ required: true, message: '请输入归属用户ID', trigger: 'blur' }],
  name: [{ required: true, message: '请输入知识库名称', trigger: 'blur' }]
}

// Docs Dialog
const docsVisible = ref(false)
const docsLoading = ref(false)
const currentKbDocs = ref([])
const currentKbId = ref(null)

async function fetchKbs() {
  loading.value = true
  try {
    const params = searchUserId.value ? { user_id: searchUserId.value } : {}
    kbs.value = await listAdminKbs(params)
  } catch (e) {
    if (e?.response?.status === 403) {
      ElMessage.error('无管理员权限，请联系管理员')
    } else {
      ElMessage.error('获取知识库列表失败')
    }
  } finally {
    loading.value = false
  }
}

function openCreate() {
  isEdit.value = false
  currentId.value = null
  Object.assign(form, { user_id: null, name: '', description: '' })
  dialogVisible.value = true
}

function openEdit(row) {
  isEdit.value = true
  currentId.value = row.id
  Object.assign(form, { 
    user_id: row.user_id, 
    name: row.name, 
    description: row.description || '' 
  })
  dialogVisible.value = true
}

async function submit() {
  if (!formRef.value) return
  await formRef.value.validate()

  dialogLoading.value = true
  try {
    if (isEdit.value) {
      await updateAdminKb(currentId.value, { name: form.name, description: form.description })
      ElMessage.success('更新成功')
    } else {
      await createAdminKb({ user_id: Number(form.user_id), name: form.name, description: form.description })
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    await fetchKbs()
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || (isEdit.value ? '更新失败' : '创建失败'))
  } finally {
    dialogLoading.value = false
  }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确认删除知识库 "${row.name}" 吗？`, '危险操作', {
      type: 'error',
      confirmButtonText: '删除',
      cancelButtonText: '取消'
    })
    await deleteAdminKb(row.id)
    ElMessage.success('删除成功')
    await fetchKbs()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

async function openDocs(row) {
  currentKbId.value = row.id
  docsVisible.value = true
  await fetchDocs()
}

async function fetchDocs() {
  if (!currentKbId.value) return
  docsLoading.value = true
  try {
    currentKbDocs.value = await listAdminKbDocuments(currentKbId.value)
  } catch (e) {
    ElMessage.error('获取文档列表失败')
  } finally {
    docsLoading.value = false
  }
}

async function handleDeleteDoc(row) {
  try {
    await ElMessageBox.confirm(`确认删除文档 "${row.filename}" 吗？`, '危险操作', {
      type: 'error',
      confirmButtonText: '删除',
      cancelButtonText: '取消'
    })
    await deleteAdminDocument(row.id)
    ElMessage.success('删除文档成功')
    await fetchDocs()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除文档失败')
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString()
}

onMounted(() => {
  fetchKbs()
})
</script>

<template>
  <div class="page-container">
    <header class="page-header">
      <div>
        <h1 class="page-title">知识库管理</h1>
        <p class="page-subtitle">系统全局知识库与文档管理 (管理员专区)</p>
      </div>
      <div class="header-actions">
        <el-input 
          v-model="searchUserId" 
          placeholder="按 User ID 过滤" 
          :prefix-icon="Search"
          clearable
          @keyup.enter="fetchKbs"
          @clear="fetchKbs"
          style="width: 200px"
        />
        <el-button :icon="Refresh" @click="fetchKbs" circle />
        <el-button type="primary" :icon="Plus" @click="openCreate">新建知识库</el-button>
      </div>
    </header>

    <main class="page-content">
      <el-table :data="kbs" v-loading="loading" border style="width: 100%; border-radius: 8px">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="user_id" label="归属用户ID" width="120" />
        <el-table-column prop="name" label="知识库名称" min-width="150" />
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="260" fixed="right">
          <template #default="{ row }">
            <el-button size="small" :icon="Document" @click="openDocs(row)">文档</el-button>
            <el-button size="small" :icon="Edit" @click="openEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" plain :icon="Delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </main>

    <!-- 知识库编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑知识库' : '新建知识库'" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="归属用户ID" prop="user_id">
          <el-input-number v-model="form.user_id" :disabled="isEdit" style="width: 100%" placeholder="输入归属用户的ID" />
        </el-form-item>
        <el-form-item label="知识库名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="dialogLoading" @click="submit">确认</el-button>
      </template>
    </el-dialog>

    <!-- 文档管理弹窗 -->
    <el-dialog v-model="docsVisible" :title="`文档管理 (KB ID: ${currentKbId})`" width="800px">
      <el-table :data="currentKbDocs" v-loading="docsLoading" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="filename" label="文件名" min-width="150" show-overflow-tooltip />
        <el-table-column prop="chunk_count" label="分块数" width="100" />
        <el-table-column label="上传时间" width="180">
          <template #default="{ row }">{{ formatDate(row.uploaded_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="danger" plain :icon="Delete" @click="handleDeleteDoc(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <el-button @click="docsVisible = false">关闭</el-button>
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
  margin-bottom: 24px;
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

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.page-content {
  background: white;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}
</style>
