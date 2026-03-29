<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'

import { registerUser } from '../api/users'

const router = useRouter()

const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  email: '',
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  email: [{ type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur', 'change'] }]
}

async function submit() {
  if (!formRef.value) return
  await formRef.value.validate()

  loading.value = true
  try {
    await registerUser({
      username: form.username,
      password: form.password,
      email: form.email || '',
    })
    ElMessage.success('注册成功，请登录')
    router.replace('/login')
  } catch (e) {
    const msg = e?.response?.data?.detail || '注册失败，请检查输入'
    ElMessage.error(msg)
  } finally {
    loading.value = false
  }
}

function toLogin() {
  router.push('/login')
}
</script>

<template>
  <div class="register-container">
    <div class="register-box">
      <div class="register-header">
        <div class="logo-icon">R</div>
        <h2>创建您的账号</h2>
        <p>加入 RAG 智能助手，开启知识管理新体验</p>
      </div>

      <el-form 
        ref="formRef" 
        :model="form" 
        :rules="rules" 
        @keyup.enter="submit"
        class="register-form"
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
            autocomplete="new-password"
            :prefix-icon="Lock"
            size="large"
          />
        </el-form-item>
        <el-form-item prop="email">
          <el-input 
            v-model="form.email" 
            placeholder="请输入邮箱 (可选)" 
            autocomplete="email"
            :prefix-icon="Message"
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
          立即注册
        </el-button>
        
        <div class="login-link">
          已有账号？
          <el-button link type="primary" :disabled="loading" @click="toLogin">
            直接登录
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
}

.register-box {
  width: 420px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  padding: 40px;
  box-sizing: border-box;
}

.register-header {
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

.register-header h2 {
  margin: 0 0 8px;
  font-size: 24px;
  color: var(--text-primary);
}

.register-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.register-form {
  margin-top: 20px;
}

.submit-btn {
  width: 100%;
  margin-top: 12px;
  font-weight: 600;
  border-radius: 8px;
}

.login-link {
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

