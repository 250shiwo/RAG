<script setup>
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

import { fetchCurrentUserProfile, loginUser } from '../api/users'
import { clearCurrentUser, setCurrentUser, setTokens } from '../services/auth'

const router = useRouter()
const route = useRoute()

const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function submit() {
  if (!formRef.value) return
  await formRef.value.validate()

  loading.value = true
  try {
    const data = await loginUser({ username: form.username, password: form.password })
    setTokens({ access: data.access, refresh: data.refresh })
    try {
      // 登录成功后立即拉取用户信息，供菜单和路由做角色判断。
      const profile = await fetchCurrentUserProfile()
      setCurrentUser(profile)
    } catch (profileError) {
      clearCurrentUser()
      console.error(profileError)
    }
    ElMessage.success('登录成功')
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/kb'
    router.replace(redirect)
  } catch (e) {
    const msg = e?.response?.data?.detail || '登录失败，请检查用户名或密码'
    ElMessage.error(msg)
  } finally {
    loading.value = false
  }
}

function toRegister() {
  router.push('/register')
}
</script>

<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <div class="logo-icon">R</div>
        <h2>欢迎使用 RAG 智能助手</h2>
        <p>登录以访问您的专属知识大脑</p>
      </div>

      <el-form 
        ref="formRef" 
        :model="form" 
        :rules="rules" 
        @keyup.enter="submit"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input 
            v-model="form.username" 
            placeholder="请输入用户名" 
            autocomplete="username"
            :prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="请输入密码" 
            show-password 
            autocomplete="current-password"
            :prefix-icon="Lock"
            size="large"
          />
        </el-form-item>
        
        <el-button 
          type="primary" 
          :loading="loading" 
          @click="submit" 
          class="submit-btn"
          size="large"
        >
          立即登录
        </el-button>
        
        <div class="register-link">
          还没有账号？
          <el-button link type="primary" :disabled="loading" @click="toRegister">
            免费注册
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
}

.login-box {
  width: 420px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  padding: 40px;
  box-sizing: border-box;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #0066cc, #004499);
  color: white;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: bold;
  margin: 0 auto 20px;
}

.login-header h2 {
  margin: 0 0 8px;
  font-size: 24px;
  color: var(--text-primary);
}

.login-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.login-form {
  margin-top: 20px;
}

.submit-btn {
  width: 100%;
  margin-top: 12px;
  font-weight: 600;
  border-radius: 8px;
}

.register-link {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: var(--text-secondary);
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 0 0 1px var(--border-color) inset;
}
</style>
