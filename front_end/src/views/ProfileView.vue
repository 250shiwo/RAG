<script setup<script setup>
import { reactive, ref, onMount<script setup>
import { reactive, ref, onMounted } from 'vue'
import { use<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Edit, Save } from '@element<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Edit, Save } from '@element-plus/icons-vue'

import { getUserProfile, updateUserProfile } from '../api/users<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Edit, Save } from '@element-plus/icons-vue'

import { getUserProfile, updateUserProfile } from '../api/users'

const router = useRouter()
const loading = ref(false)
const saving<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Edit, Save } from '@element-plus/icons-vue'

import { getUserProfile, updateUserProfile } from '../api/users'

const router = useRouter()
const loading = ref(false)
const saving = ref(false)

const form = reactive({
  username: '',
<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Edit, Save } from '@element-plus/icons-vue'

import { getUserProfile, updateUserProfile } from '../api/users'

const router = useRouter()
const loading = ref(false)
const saving = ref(false)

const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: ''
})

const rules = {
  username:<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Edit, Save } from '@element-plus/icons-vue'

import { getUserProfile, updateUserProfile } from '../api/users'

const router = useRouter()
const loading = ref(false)
const saving = ref(false)

const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: ''
})

const rules = {
  username: [{ required: true, message: '请输入<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Edit, Save } from '@element-plus/icons-vue'

import { getUserProfile, updateUserProfile } from '../api/users'

const router = useRouter()
const loading = ref(false)
const saving = ref(false)

const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    {<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Edit, Save } from '@element-plus/icons-vue'

import { getUserProfile, updateUserProfile } from '../api/users'

const router = useRouter()
const loading = ref(false)
const saving = ref(false)

const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Edit, Save } from '@element-plus/icons-vue'

import { getUserProfile, updateUserProfile } from '../api/users'

const router = useRouter()
const loading = ref(false)
const saving = ref(false)

const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'bl