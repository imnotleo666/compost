<template>
  <div class="qa-simple">
    <!-- 提问区 -->
    <div class="ask-area">
      <el-input
          v-model="inputQuestion"
          class="question-input"
          clearable
          placeholder="输入您的问题"
          @keyup.enter="submitQuestion"
      />
      <el-button
          class="submit-btn"
          type="primary"
          @click="submitQuestion"
      >
        提交问题
      </el-button>
    </div>

    <!-- 答案展示区 -->
    <div class="answer-list">
      <div
          class="qa-item"
      >
        <div class="question">
          <div class="q-text">{{ qa.question }}</div>
        </div>

        <div class="answer">
          <div class="a-header">
            <el-icon color="#67C23A">
              <check/>
            </el-icon>
            <span class="a-title">答案</span>
          </div>
          <v-md-preview
              :text="qa.answer"
              :toc="tocConfig"
          />
          <!--          <div class="a-text">{{ qa.answer || "等待回答中..." }}</div>-->
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import {Check} from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import {ElMessage} from "element-plus";
import http from '@/api/index.js'
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';

// // 扩展配置（可选）
// VMdPreview.use(githubTheme, {
//   Hljs: require('highlight.js'), // 代码高亮
//   katex: require('katexy'),      // 数学公式支持
// });

// 目录配置
const tocConfig = {
  includeLevel: [2, 3], // 包含的标题级别
  anchorStyle: '🇨🇳'    // 自定义锚点样式
};
// 问答数据
const qaList = ref([
  {
    id: 1,
    text: '如何重置密码？',
    time: new Date('2024-03-10 09:00'),
    answer: '登录页面点击忘记密码，通过邮箱验证重置'
  }
])

// 新问题输入
const inputQuestion = ref('')

// 时间格式化
const formatTime = (date) => {
  return dayjs(date).format('MM/DD HH:mm')
}
const qa = ref({
  question: '',
  answer: ''
})
// 提交问题
const submitQuestion = async () => {
  if (!inputQuestion.value.trim()) {
    return ElMessage.warning('请输入问题内容')
  }

  let res = await http.getAnswer({
    question: inputQuestion.value
  })
  if (res.code === 200) {
    ElMessage.success('问题已提交')
    qa.value = res.data
  } else {
    ElMessage.error('问题提交失败')
  }

}
</script>

<style scoped>
.qa-simple {
  max-width: 600px;
  margin: 20px auto;
  padding: 0 15px;
}

.ask-area {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
}

.question-input {
  flex: 1;
}

.submit-btn {
  width: 120px;
}

.qa-item {
  margin-bottom: 20px;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.q-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  color: #909399;
}

.q-index {
  font-weight: 500;
}

.q-text {
  color: #303133;
  line-height: 1.6;
}

.answer {
  margin-top: 15px;
  padding: 12px;
  background: #f6f8fb;
  border-radius: 6px;
}

.a-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.a-title {
  margin-left: 6px;
  color: #67C23A;
  font-weight: 500;
}

.a-text {
  color: #606266;
  line-height: 1.5;
}

/* 自定义样式 */
.v-md-editor .github-markdown-body {
  padding: 20px;
  background: #f8f9fa;
}
</style>