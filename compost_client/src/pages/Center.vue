<template>
  <el-card class="profile-container">
    <!-- 基本信息展示与编辑区 -->
    <el-form ref="formRef" :model="formData" :rules="rules" label-width="120px">
      <el-row :gutter="20">
        <!-- 左侧头像展示区 -->
        <el-col :span="8">
          <div class="avatar-section">
            <el-avatar :size="120" :src="formData.avatar">{{ getFirst(formData.name) }}</el-avatar>
            <div class="username">{{ formData.username }}</div>
          </div>
        </el-col>

        <!-- 右侧表单编辑区 -->
        <el-col :span="16">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="formData.name"/>
          </el-form-item>

          <el-form-item label="邮箱" prop="email">
            <el-input v-model="formData.email"/>
          </el-form-item>

          <el-form-item label="手机号" prop="phone">
            <el-input v-model="formData.phone"/>
          </el-form-item>

          <!--          <el-form-item label="地址" prop="address">-->
          <!--            <el-input v-model="formData.address" :rows="2" type="textarea"/>-->
          <!--          </el-form-item>-->

          <!-- 不可修改字段 -->
          <el-form-item label="角色">
            <el-input :value="formData.role" disabled/>
          </el-form-item>

          <el-form-item label="创建时间">
            <el-input :value="formatDate(formData.createtime)" disabled/>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleSubmit">保存修改</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
  </el-card>
</template>
<script setup>
import {onMounted, reactive, ref} from 'vue'
import {ElMessage} from 'element-plus'
import http from "@/utils/http.js";

const getFirst = (str) => {
  if (str) {
    return str.substring(0, 1)
  }
  return ' '
}
onMounted(() => {
  let userInfo = JSON.parse(localStorage.getItem('user'))
  formData.value = userInfo;
})
// 表单数据
const formData = ref({
  username: 'admin',
  name: '张三',
  email: 'zhangsan@example.com',
  phone: '13800138000',
  address: '北京市朝阳区',
  role: '管理员',
  createTime: '2024-01-01 10:00:00'
})

// 表单验证规则
const rules = reactive({
  name: [
    {required: true, message: '请输入姓名', trigger: 'blur'},
    {min: 2, max: 10, message: '长度在2到10个字符', trigger: 'blur'}
  ],
  email: [
    {required: true, message: '请输入邮箱', trigger: 'blur'},
    {type: 'email', message: '邮箱格式不正确', trigger: 'blur'}
  ],
  phone: [
    {pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur'}
  ],
  address: [
    {max: 100, message: '地址不能超过100个字符', trigger: 'blur'}
  ]
})

// 日期格式化
const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString()
}

// 提交处理
const formRef = ref(null)
const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    // 调用更新接口（示例）
    http.post('user/update', {
      id: formData.value.id,
      name: formData.value.name,
      email: formData.value.email,
      phone: formData.value.phone
    }).then(res => {
      ElMessage.success('修改成功...')
    })
  } catch (error) {
    ElMessage.error('表单验证失败')
  }
}
</script>
<style scoped>
.profile-container {
  max-width: 1000px;
  margin: 20px auto;
}

.avatar-section {
  text-align: center;
  padding: 20px;
  border-right: 1px solid #eee;
}

.username {
  margin-top: 15px;
  font-size: 16px;
  color: #606266;
}

.el-avatar {
  font-size: 70px;
  font-family: '华文行楷';
}
</style>