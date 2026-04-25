<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getMe, updateUserInfo, changePassword } from '../api/users'

const router = useRouter()
const userInfo = ref({})
const loading = ref(false)
const activeTab = ref('profile')

// 个人信息表单
const profileForm = ref({
  username: '',
  email: ''
})

// 密码修改表单
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const profileRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }]
}

const passwordRules = {
  oldPassword: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  newPassword: [{ required: true, message: '请输入新密码', trigger: 'blur' }, { min: 6, message: '密码长度至少为6位', trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

async function loadUserInfo() {
  loading.value = true
  try {
    const data = await getMe()
    userInfo.value = data
    profileForm.value.username = data.username
    profileForm.value.email = data.email
  } catch (error) {
    ElMessage.error('获取用户信息失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function handleUpdateProfile() {
  loading.value = true
  try {
    await updateUserInfo(profileForm.value)
    ElMessage.success('个人信息更新成功')
    await loadUserInfo()
  } catch (error) {
    ElMessage.error('个人信息更新失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function handleChangePassword() {
  loading.value = true
  try {
    await changePassword(passwordForm.value.oldPassword, passwordForm.value.newPassword)
    ElMessage.success('密码修改成功')
    // 清空表单
    passwordForm.value = {
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (error) {
    ElMessage.error('密码修改失败，请检查旧密码是否正确')
    console.error(error)
  } finally {
    loading.value = false
  }
}

function goToSubscription() {
  router.push('/subscription')
}

onMounted(() => {
  loadUserInfo()
})
</script>

<template>
  <div class="user-profile-container">
    <el-card class="user-profile-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <h2>个人信息管理</h2>
          <el-button type="primary" plain @click="goToSubscription">订阅套餐</el-button>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本信息" name="profile">
          <el-form :model="profileForm" :rules="profileRules" label-width="100px" class="profile-form">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="profileForm.username" placeholder="请输入用户名" />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="profileForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleUpdateProfile" :loading="loading">保存修改</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="修改密码" name="password">
          <el-form :model="passwordForm" :rules="passwordRules" label-width="120px" class="password-form">
            <el-form-item label="旧密码" prop="oldPassword">
              <el-input v-model="passwordForm.oldPassword" type="password" placeholder="请输入旧密码" show-password />
            </el-form-item>
            <el-form-item label="新密码" prop="newPassword">
              <el-input v-model="passwordForm.newPassword" type="password" placeholder="请输入新密码" show-password />
            </el-form-item>
            <el-form-item label="确认新密码" prop="confirmPassword">
              <el-input v-model="passwordForm.confirmPassword" type="password" placeholder="请确认新密码" show-password />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleChangePassword" :loading="loading">修改密码</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<style scoped>
.user-profile-container {
  padding: 24px;
  min-height: 100vh;
  background-color: var(--bg-color);
}

.user-profile-card {
  max-width: 600px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 24px;
  color: var(--text-primary);
}

.profile-form,
.password-form {
  margin-top: 24px;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-button {
  margin-top: 12px;
}
</style>
