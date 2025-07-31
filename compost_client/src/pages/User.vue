<template>
  <div class="app-container">
    <el-form :inline="true" :model="searchFormData" class="demo-form-inline" size="mini">
      <el-form-item
          label="用户名"
      >
        <el-input v-model="searchFormData.username" :clearable="true" placeholder="用户名" style="width: 250px;"/>
      </el-form-item>
      <el-form-item
          label="电话号码"
      >
        <el-input v-model="searchFormData.phone" :clearable="true" placeholder="电话号码" style="width: 250px;"/>
      </el-form-item>
      <el-form-item
          label="邮箱"
      >
        <el-input v-model="searchFormData.email" :clearable="true" placeholder="邮箱" style="width: 250px;"/>
      </el-form-item>
      <el-form-item
          label="姓名"
      >
        <el-input v-model="searchFormData.name" :clearable="true" placeholder="姓名" style="width: 250px;"/>
      </el-form-item>
      <el-form-item
          label="角色"
      >
        <el-select v-model="searchFormData.role" clearable placeholder="请选择..." style="width: 250px;">
          <el-option label="管理员" value="管理员"/>
          <el-option label="用户" value="用户"/>
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button :icon="Search" type="primary" @click="loadTable">查询</el-button>
      </el-form-item>
      <el-form-item>
        <el-button :icon="Plus" type="primary" @click="onAdd">新增</el-button>
      </el-form-item>
      <el-form-item>
        <el-button :icon="Download" type="primary" @click="exportExcel">导出Excel</el-button>
      </el-form-item>
      <!--      <el-form-item>-->
      <!--        &lt;!&ndash; 文件上传组件 &ndash;&gt;-->
      <!--        <el-upload-->
      <!--            :auto-upload="false"-->
      <!--            :on-change="handleFileChange"-->
      <!--            :show-file-list="false"-->
      <!--            accept=".xlsx,.xls"-->
      <!--            action=""-->
      <!--        >-->
      <!--          <template #trigger>-->
      <!--            <el-button :icon="Upload" type="primary">选择Excel文件</el-button>-->
      <!--          </template>-->
      <!--        </el-upload>-->
      <!--      </el-form-item>-->
    </el-form>

    <el-table
        v-loading="loading"
        :data="pageInfo.rows"
        border
        highlight-current-row
    >
      <el-table-column
          label="ID"
          prop="id"
      />
      <el-table-column
          label="用户名"
          prop="username"
      />
      <el-table-column
          label="电话号码"
          prop="phone"
      />
      <el-table-column
          label="邮箱"
          prop="email"
      />
      <el-table-column
          label="头像"
          prop="avatar"
      >
        <template #default="{ row }">
          <img :src="row.avatar" style="width: 100px; height: 100px;"/>
        </template>
      </el-table-column>
      <el-table-column
          label="姓名"
          prop="name"
      />
      <el-table-column
          label="性别"
          prop="gender"
      />
      <el-table-column
          label="角色"
          prop="role"
      />
      <el-table-column
          label="创建时间"
          prop="createtime"
      >
        <template #default="{ row }">
          {{ formatTime(row.createtime) }}
        </template>
      </el-table-column>
      <el-table-column>
        <template #default="{ row }">
          <el-tooltip
              class="box-item"
              content="修改"
              effect="dark"
              placement="top"
          >
            <el-button size="mini" type="text" @click="handleUpdate(row)">
              <el-icon>
                <Edit/>
              </el-icon>
            </el-button>
          </el-tooltip>
          <el-tooltip
              class="box-item"
              content="删除"
              effect="dark"
              placement="top"
          >
            <el-button size="mini" type="text" @click="handleDelete(row)">
              <el-icon>
                <Delete/>
              </el-icon>
            </el-button>
          </el-tooltip>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <el-pagination
        :current-page="searchFormData.pageIndex"
        :page-size="searchFormData.pageSize"
        :page-sizes="[5, 10, 20, 40]"
        :total="pageInfo.total"
        background
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
    />


    <!--dialog-->
    <el-dialog
        v-model="dialogVisible"
        :close-on-click-modal="false"
        :title="dialogTitle"
    >
      <el-form
          ref="dialogFormRef"
          :model="dialogFormData"
          :rules="dialogRules"
          label-width="120px"
      >
        <el-form-item
            label="用户名"
            prop="username"
        >
          <el-input v-model="dialogFormData.username"/>
        </el-form-item>
        <el-form-item
            label="电话号码"
            prop="phone"
        >
          <el-input v-model="dialogFormData.phone"/>
        </el-form-item>
        <el-form-item
            label="邮箱"
            prop="email"
        >
          <el-input v-model="dialogFormData.email"/>
        </el-form-item>
        <el-form-item
            label="头像"
            prop="avatar"
        >
          <el-upload
              :on-success="handleAvatarSuccess"
              :show-file-list="false"
              action="http://localhost/upload"
          >
            <img v-if="dialogFormData.avatar" :src="dialogFormData.avatar" class="avatar" style="max-width: 100%">
            <el-icon v-else class="avatar-uploader-icon">
              <Plus/>
            </el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item
            label="姓名"
            prop="name"
        >
          <el-input v-model="dialogFormData.name"/>
        </el-form-item>
        <el-form-item
            label="性别"
            prop="gender"
        >
          <el-select v-model="dialogFormData.gender" placeholder="请选择...">
            <el-option label="男" value="男"/>
            <el-option label="女" value="女"/>
          </el-select>
        </el-form-item>
        <el-form-item v-if="dialogTitle  === '新增信息'"
                      label="密码"
                      prop="password"
        >
          <el-input v-model="dialogFormData.password"/>
        </el-form-item>
        <el-form-item
            label="角色"
            prop="role"
        >
          <el-select v-model="dialogFormData.role" placeholder="请选择...">
            <el-option label="管理员" value="管理员"/>
            <el-option label="用户" value="用户"/>
          </el-select>
        </el-form-item>

      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleDialogSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import {onMounted, reactive, ref} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Delete, Download, Edit, Plus, Search} from '@element-plus/icons-vue'
import moment from 'moment'
import http from '@/api/index'
import * as XLSX from 'xlsx';
import {utils, writeFile} from 'xlsx';

// 文件变化回调
const handleFileChange = async (uploadFile) => {
  try {
    // 1. 文件类型校验
    if (!['xlsx', 'xls'].includes(uploadFile.name.split('.').pop().toLowerCase())) {
      throw new Error('仅支持.xlsx/.xls格式文件')
    }

    // 2. 读取文件内容
    const reader = new FileReader()
    reader.onload = (e) => {
      const data = new Uint8Array(e.target.result)
      const workbook = XLSX.read(data, {type: 'array'})

      // 3. 获取第一张工作表
      const worksheet = workbook.Sheets[workbook.SheetNames[0]]

      // 4. 转换JSON数据
      const jsonData = XLSX.utils.sheet_to_json(worksheet, {header: 1})
      let tableHeader = []
      let tableData = []
      // 5. 处理表头和数据
      if (jsonData.length > 0) {
        tableHeader = jsonData[0] // 第一行为表头
        tableData = jsonData.slice(1).map(row => {
          return tableHeader.reduce((obj, key, index) => {
            obj[key] = row[index] || ''
            return obj
          }, {})
        })
      }
      if (tableData.length > 0) {
        // 6. 创建请求体
        tableData.forEach(item => {
          http.createUser(item)
        })

      }
    }
    reader.readAsArrayBuffer(uploadFile.raw)

  } catch (error) {
    ElMessage.error(`文件解析失败: ${error.message}`)
  }
}

const handleAvatarSuccess = (res) => {
  dialogFormData.avatar = res.data
}
const exportExcel = async () => {
  // 数据转工作表
  const worksheet = utils.json_to_sheet(pageInfo.rows);
  // 创建工作簿
  const workbook = utils.book_new();
  utils.book_append_sheet(workbook, worksheet, 'Sheet1');
  // 生成文件并保存
  let times = new Date().getTime()
  const excelBuffer = writeFile(workbook, times + '.xlsx');
  // const blob = new Blob([excelBuffer], {type: 'application/octet-stream'});
  // saveAs(blob, '用户数据.xlsx');
};
// 响应式状态
const searchFormData = reactive({
  id: '',
  username: '',
  phone: '',
  email: '',
  avatar: '',
  name: '',
  password: '',
  role: '',
  pageIndex: 1,
  pageSize: 10
})
const pageInfo = reactive({
  rows: [],
  total: 0
})
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const dialogFormRef = ref(null)
const dialogFormData = reactive({
  id: ''
  , username: ''
  , phone: ''
  , email: ''
  , avatar: ''
  , name: ''
  , gender: ''
  , departmentid: ''
  , password: ''
  , role: ''
  , createtime: ''
})
// 验证规则
const dialogRules = reactive({
  id: [{required: true, message: '不能为空', trigger: 'blur'}]
  , username: [{required: true, message: '不能为空', trigger: 'blur'}]
  , phone: [{required: true, message: '不能为空', trigger: 'blur'}]
  , email: [{required: true, message: '不能为空', trigger: 'blur'}]
  , avatar: [{required: true, message: '不能为空', trigger: 'blur'}]
  , name: [{required: true, message: '不能为空', trigger: 'blur'}]
  , gender: [{required: true, message: '不能为空', trigger: 'blur'}]
  , password: [{required: true, message: '不能为空', trigger: 'blur'}]
  , role: [{required: true, message: '不能为空', trigger: 'blur'}]
  , createtime: [{required: true, message: '不能为空', trigger: 'blur'}]
})
let userInfo = ref({})
// 生命周期
onMounted(() => {
  userInfo.value = JSON.parse(localStorage.getItem('user'))
  loadTable()
})
// 数据加载
const loadTable = async () => {
  try {
    loading.value = true
    const data = await http.getUserList(searchFormData)
    pageInfo.rows = data.list
    pageInfo.total = data.total
  } catch (error) {
    console.log(error)
    ElMessage.error('数据加载失败')
  } finally {
    loading.value = false
  }
}
// 分页处理
const handleSizeChange = (size) => {
  searchFormData.pageSize = size
  loadTable()
}

const handlePageChange = (page) => {
  searchFormData.pageIndex = page
  loadTable()
}

// 对话框操作
const onAdd = () => {
  dialogTitle.value = '新增信息'
  Object.keys(dialogFormData).forEach((key) => {
    dialogFormData[key] = ''
  })
  dialogVisible.value = true
}
const handleUpdate = (row) => {
  dialogTitle.value = '修改信息'
  dialogVisible.value = true
  Object.assign(dialogFormData, {
    ...row
  })
}
const handleDialogSubmit = async () => {
  try {
    await dialogFormRef.value.validate()
    const api = dialogTitle.value == '修改信息'
        ? http.updateUser
        : http.createUser
    if (dialogTitle.value == '修改信息') {
      delete dialogFormData.password
      delete dialogFormData.department
    }
    await api(dialogFormData)
    ElMessage.success('操作成功')
    dialogVisible.value = false
    loadTable()
    Object.keys(dialogFormData).forEach((key) => {
      dialogFormData[key] = ''
    })
  } catch (error) {
    ElMessage.error("操作失败...")
  }
}

// 删除操作
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除该条记录吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await http.deleteUser(row.id)
    ElMessage.success('删除成功')
    loadTable()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 时间格式化
const formatTime = (value) => {
  if (!value) return ''
  return moment(value).format('YYYY-MM-DD HH:mm:ss')
}
</script>
<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

/* 深度选择器更新 */
:deep(.el-pagination) {
  margin-top: 15px;
}
</style>