<template>
  <div class="bg">
    <div class="login-container">
      <el-card class="login-card">
        <h2 class="login-title">用户登录</h2>
        <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="80px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="loginForm.password" placeholder="请输入密码" type="password"></el-input>
          </el-form-item>
          <el-form-item label="角色" prop="role">
            <el-radio-group v-model="loginForm.role">
              <el-radio size="default" value="管理员">管理员</el-radio>
              <el-radio size="default" value="用户">用户</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="login">登录</el-button>
          </el-form-item>
          <el-form-item>
            <div>没有账号？<span style="color: blue;" @click="goRegister">点我注册！</span></div>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import {reactive, ref} from 'vue';
import {ElMessage} from 'element-plus';
import request from '../utils/http.js';
import {useRouter} from 'vue-router';

// 获取路由实例
const router = useRouter();
const goRegister = () => {
  router.push('/register')
}
// 登录表单数据
const loginForm = reactive({
  username: '',
  password: '',
  //role: '',
});

// 表单验证规则
const loginRules = reactive({
  username: [{
    required: true,
    message: '请输入用户名',
    trigger: 'blur'
  },],
  password: [{
    required: true,
    message: '请输入密码',
    trigger: 'blur'
  },],
  role: [{
    required: true,
    message: '请选择角色',
    trigger: 'blur'
  },],
});

// 登录表单引用
const loginFormRef = ref(null);

// 登录方法
let login = () => {
  loginFormRef.value.validate(async (valid) => {
    if (valid) {
      let resp = await request.post('user/login', loginForm);
      if (resp.data) {
        ElMessage.success('登录成功');
        console.log(resp)
        localStorage.setItem('user', JSON.stringify(resp.data));
        router.push('/home')
      } else {
        ElMessage.error('用户名和密码错误')
      }

    } else {
      ElMessage.error('请输入用户名和密码');
      return false;
    }
  });
};
</script>

<style scoped>
.bg {
  width: 100%;
}

.login-container {
  width: 100%;
  background-image: url('/bj.jpg');
  background-size: 100% 100%;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.login-card {
  width: 450px;
  padding: 30px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  background-color: rgba(255, 255, 255, 0.7);
  color: #000;
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
  color: #000;
}
</style>