<template>
  <div class="bg">
    <div class="login-container">
      <el-card class="login-card">
        <h2 class="login-title">用户注册</h2>
        <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="80px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="loginForm.password" placeholder="请输入密码" type="password"></el-input>
          </el-form-item>
          <el-form-item label="姓名" prop="name">
            <el-input v-model="loginForm.name" placeholder="请输入姓名"></el-input>
          </el-form-item>
          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="loginForm.gender">
              <el-radio size="default" value="男">男</el-radio>
              <el-radio size="default" value="女">女</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="loginForm.email" placeholder="请输入邮箱"></el-input>
          </el-form-item>
          <el-form-item label="联系方式" prop="phone">
            <el-input v-model="loginForm.phone" placeholder="请输入联系方式"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="login">注册</el-button>
          </el-form-item>
          <el-form-item>
            <div>已有账号？<span style="color: blue;" @click="goRegister">点我登录！</span></div>
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
  router.push('/login')
}
// 登录表单数据
const loginForm = reactive({
  username: '',
  password: '',
  name: '',
  gender: '',
  email: '',
  phone: '',
  //role: '',
});

// 表单验证规则
const loginRules = reactive({
  gender: [{required: true, message: '用户名不能为空', trigger: ['blur', 'change']},],
  username: [
    // 必填校验
    {required: true, message: '用户名不能为空', trigger: ['blur', 'change']},

    // 格式校验
    {
      pattern: /^[a-zA-Z0-9_]{3,20}$/,
      message: '用户名需为3-20位字母/数字/下划线组合',
      trigger: 'blur'
    },

    // 空格校验
    {
      validator: (rule, value, callback) => {
        if (value.trim().length === 0) {
          callback(new Error('用户名不能为纯空格'))
        } else if (value.includes('  ')) {
          callback(new Error('用户名不能包含连续空格'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  password: [
    // 必填校验
    {required: true, message: '密码不能为空', trigger: 'blur'},

    // 基础格式校验
    {min: 8, max: 16, message: '密码长度需为8-16位', trigger: 'blur'},

    // 复杂度校验
    {
      validator: (rule, value, callback) => {
        const regExp = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,16}$/
        if (!regExp.test(value)) {
          callback(new Error('需包含数字、大小写字母和特殊符号(!@#$%^&*)'))
        } else {
          callback()
        }
      },
      trigger: ['blur', 'change']
    }
  ],
  role: [{
    required: true,
    message: '请选择角色',
    trigger: 'blur'
  },],
  email: [{
    required: true,
    message: '请输入邮箱',
    trigger: 'blur'
  }, {
    type: 'email',
    message: '请输入有效的邮箱地址',
    trigger: ['blur', 'change']
  }, {
    pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
    message: '邮箱格式不合法（示例：user@example.com）',
    trigger: 'blur'
  }],
  phone: [{
    required: true,
    message: '请输入手机号',
    trigger: 'blur'
  }, {
    pattern: /^(?:(?:\+|00)86)?1[3-9]\d{9}$/,
    message: '手机号格式错误（示例：13800138000）',
    trigger: 'blur'
  }, {
    validator: (rule, value, callback) => {
      if (value && value.replace(/\D/g, '').length !== 11) {
        callback(new Error('手机号应为11位数字'));
      } else {
        callback();
      }
    },
    trigger: 'blur'
  }],
  name: [{
    required: true,
    message: '请输入姓名',
    trigger: 'blur'
  }, {
    pattern: /^[\u4e00-\u9fa5]{2,20}$/,
    message: '姓名应为2-20个汉字',
    trigger: 'blur'
  }, {
    validator: (rule, value, callback) => {
      if (value.trim().length < 2) {
        callback(new Error('姓名不能为空或纯空格'));
      } else {
        callback();
      }
    },
    trigger: 'blur'
  }]
});

// 登录表单引用
const loginFormRef = ref(null);

// 登录方法
let login = () => {
  loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loginForm.role = '用户'
      console.log(loginForm)
      let resp = await request.post('user/add', loginForm);
      if (resp) {
        ElMessage.success('注册成功');
        router.push('/login')
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