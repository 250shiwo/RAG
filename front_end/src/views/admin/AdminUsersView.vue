<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Edit, Delete, Refresh } from '@element-plus/icons-vue'
import { listAdminUsers, createAdminUser, updateAdminUser, deleteAdminUser } from '../../api/admin'

const loading = ref(false)
const users = ref([])
const searchQ = ref('')

const dialogVisible = ref(false)
const dialogLoading = ref(false)
const formRef = ref()
const isEdit = ref(false)
const currentId = ref(null)

const form = reactive({
  username: '',
  password: '',
  email: '',
  is_active: true,
  is_staff: false
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { 
      required: true, 
      validator: (rule, value, callback) => {
        if (!isEdit.value && !value) {
          callback(new Error('创建用户时密码必填'))
        } else {
          callback()
        }
      },
      trigger: 'blur' 
    }
  ]
}

async function fetchUsers() {
  loading.value = true
  try {
    users.value = await listAdminUsers({ q: searchQ.value })
  } catch (e) {
    if (e?.response?.status === 403) {
      ElMessage.error('无管理员权限，请联系管理员')
    } else {
      ElMessage.error('获取用户列表失败')
    }
  } finally {
    loading.value = false
  }
}

function openCreate() {
  isEdit.value = false
  currentId.value = null
  Object.assign(form, { username: '', password: '', email: '', is_active: true, is_staff: false })
  dialogVisible.value = true
}

function openEdit(row) {
  isEdit.value = true
  currentId.value = row.id
  Object.assign(form, { 
    username: row.username, 
    password: '', // 留空表示不修改
    email: row.email || '', 
    is_active: row.is_active, 
    is_staff: row.is_staff 
  })
  dialogVisible.value = true
}

async function submit() {
  if (!formRef.value) return
  await formRef.value.validate()

  dialogLoading.value = true
  try {
    const payload = { ...form }
    if (isEdit.value && !payload.password) {
      delete payload.password
    }
    
    if (isEdit.value) {
      await updateAdminUser(currentId.value, payload)
      ElMessage.success('更新成功')
    } else {
      await createAdminUser(payload)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    await fetchUsers()
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || (isEdit.value ? '更新失败' : '创建失败'))
  } finally {
    dialogLoading.value = false
  }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确认删除用户 "${row.username}" 吗？`, '危险操作', {
      type: 'error',
      confirmButtonText: '删除',
      cancelButtonText: '取消'
    })
    await deleteAdminUser(row.id)
    ElMessage.success('删除成功')
    await fetchUsers()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString()
}

onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <div class="page-container">
    <header class="page-header">
      <div>
        <h1 class="page-title">用户管理</h1>
        <p class="page-subtitle">系统全局用户管理 (管理员专区)</p>
      </div>
      <div class="header-actions">
        <el-input 
          v-model="searchQ" 
          placeholder="搜索用户名/邮箱" 
          :prefix-icon="Search"
          clearable
          @keyup.enter="fetchUsers"
          @clear="fetchUsers"
          style="width: 240px"
        />
        <el-button :icon="Refresh" @click="fetchUsers" circle />
        <el-button type="primary" :icon="Plus" @click="openCreate">新建用户</el-button>
      </div>
    </header>

    <main class="page-content">
      <el-table :data="users" v-loading="loading" border style="width: 100%; border-radius: 8px">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_staff ? 'warning' : 'info'">
              {{ row.is_staff ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="注册时间" min-width="180">
          <template #default="{ row }">{{ formatDate(row.date_joined) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" :icon="Edit" @click="openEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" plain :icon="Delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </main>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑用户' : '新建用户'" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" show-password :placeholder="isEdit ? '留空表示不修改密码' : ''" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="form.is_active" active-text="启用" inactive-text="禁用" />
        </el-form-item>
        <el-form-item label="角色" prop="is_staff">
          <el-switch v-model="form.is_staff" active-text="管理员" inactive-text="普通用户" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="dialogLoading" @click="submit">确认</el-button>
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
