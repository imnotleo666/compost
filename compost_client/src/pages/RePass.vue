<template>
  <div class="password-container">
    <el-card class="box-card" header="修改密码">
      <el-form
          ref="passwordFormRef"
          :model="formData"
          :rules="formRules"
          label-position="right"
          label-width="120px"
          status-icon
      >
        <el-form-item label="原密码" prop="oldPassword">
          <el-input
              v-model="formData.oldPassword"
              :type="showOldPassword ? 'text' : 'password'"
              clearable
              placeholder="请输入原密码"
          >
            <template #suffix>
              <el-icon @click="showOldPassword = !showOldPassword">
                <component :is="showOldPassword ? View : Hide"/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="新密码" prop="newPassword">
          <el-input
              v-model="formData.newPassword"
              :type="showNewPassword ? 'text' : 'password'"
              clearable
              placeholder="8-20位包含字母和数字的组合"
          >
            <template #suffix>
              <el-icon @click="showNewPassword = !showNewPassword">
                <component :is="showNewPassword ? View : Hide"/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
              v-model="formData.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              clearable
              placeholder="请再次输入新密码"
          >
            <template #suffix>
              <el-icon @click="showConfirmPassword = !showConfirmPassword">
                <component :is="showConfirmPassword ? View : Hide"/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button
              :loading="submitting"
              type="primary"
              @click="handleSubmit"
          >
            提交修改
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import {reactive, ref} from 'vue'
import {ElMessage} from 'element-plus'
import {Hide, View} from '@element-plus/icons-vue'
import http from "../api/index.js"
import {useRouter} from 'vue-router'

const router = useRouter()
// 表单数据
const formData = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 显示密码状态
const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

// 表单引用
const passwordFormRef = ref(null)

// 提交状态
const submitting = ref(false)

// 密码复杂度验证
const validatePassword = (rule, value, callback) => {
  if (!/(?=.*[a-zA-Z])(?=.*\d).{8,20}/.test(value)) {
    callback(new Error('需8-20位字母+数字组合'))
  } else {
    callback()
  }
}

// 确认密码验证
const validateConfirm = (rule, value, callback) => {
  if (value !== formData.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 表单验证规则
const formRules = reactive({
  oldPassword: [
    {required: true, message: '请输入原密码', trigger: 'blur'}
  ],
  newPassword: [
    {required: true, message: '请输入新密码', trigger: 'blur'},
    {validator: validatePassword, trigger: 'blur'}
  ],
  confirmPassword: [
    {required: true, message: '请确认新密码', trigger: 'blur'},
    {validator: validateConfirm, trigger: 'blur'}
  ]
})

// 提交处理
const handleSubmit = async () => {
  try {
    submitting.value = true
    await passwordFormRef.value.validate()

    // 这里添加实际API调用
    // 示例：await updatePasswordAPI(formData)
    let user = JSON.parse(localStorage.getItem('user'))
    let data = {
      id: user.id,
      ...formData,
    }
    // 模拟API调用
    let res = await http.repassword(data);
    if (res.code != 200) {
      ElMessage.error(res.message)
      return
    }
    ElMessage.success('密码修改成功')
    handleReset()
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (error) {
    ElMessage.error(error.message || '修改失败')
  } finally {
    submitting.value = false
  }
}

// 重置表单
const handleReset = () => {
  passwordFormRef.value.resetFields()
  showOldPassword.value = false
  showNewPassword.value = false
  showConfirmPassword.value = false
}
</script>

<style scoped>
.password-container {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.box-card {
  width: 600px;
  margin-top: 50px;
}

.el-form-item {
  margin-bottom: 22px;
}

.el-icon {
  cursor: pointer;
  color: #909399;
  vertical-align: middle;
}

.el-button {
  margin-right: 15px;
}
</style>