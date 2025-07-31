<template>
  <div class="app-container">
    <el-form :inline="true" :model="searchFormData" class="demo-form-inline" size="mini">


      <el-form-item
          label="检测结果"
      >
        <el-select v-model="searchFormData.result" clearable placeholder="请选择" style="width: 250px;">
          <el-option label="成熟" value="0"></el-option>
          <el-option label="未成熟" value="1"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button :icon="Search" type="primary" @click="loadTable">查询</el-button>
      </el-form-item>
      <el-form-item>
        <el-button :icon="Plus" type="primary" @click="onAdd">检测</el-button>
      </el-form-item>
      <el-form-item>
        <el-button :icon="Download" @click="exportExcel">导出Excel</el-button>
      </el-form-item>
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
          label="检测用户"
          prop="userid"
      >
        <template #default="{ row }">
          {{ row.name }}
        </template>
      </el-table-column>
      <el-table-column
          label="图片"
          prop="imageurl"
      >
        <template #default="{ row }">
          <el-image
              :preview-src-list="[row.imageurl]"
              :src="row.imageurl"
              fit="fill"
              preview-teleported
              style="width: 100px; height: 100px"
          />
        </template>
      </el-table-column>
      <el-table-column
          label="检测结果"
          prop="result"
      >
        <template #default="{ row }">
          {{ row.result === 0 ? '成熟' : '未成熟' }}
        </template>
      </el-table-column>
      <el-table-column
          label="置信度"
          prop="confidence"
      />
      <el-table-column
          label="耗时"
          prop="timeconsuming"
      />
      <el-table-column
          label="检测时间"
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
            label="图片"
            prop="imageurl"
        >
          <el-upload
              :on-success="handleImageChange"
              :show-file-list="false"
              action="http://localhost/api/upload"
              class="upload-demo"
          >
            <el-image v-if="dialogFormData.imageurl" :src="dialogFormData.imageurl"></el-image>
            <el-icon v-else>
              <Plus></Plus>
            </el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleDialogSubmit">检测</el-button>
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
import {utils, writeFile} from 'xlsx';

const handleImageChange = (res, file) => {
  dialogFormData.imageurl = res.data
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
  userid: '',
  imageurl: '',
  result: '',
  confidence: '',
  timeconsuming: '',
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
  , userid: ''
  , imageurl: ''
  , result: ''
  , confidence: ''
  , timeconsuming: ''
  , createtime: ''
})
// 验证规则
const dialogRules = reactive({
  id: [{required: true, message: '不能为空', trigger: 'blur'}]
  , userid: [{required: true, message: '不能为空', trigger: 'blur'}]
  , imageurl: [{required: true, message: '不能为空', trigger: 'blur'}]
  , result: [{required: true, message: '不能为空', trigger: 'blur'}]
  , confidence: [{required: true, message: '不能为空', trigger: 'blur'}]
  , timeconsuming: [{required: true, message: '不能为空', trigger: 'blur'}]
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
    if (userInfo.value.role !== '管理员')
      searchFormData.userid = userInfo.value.id
    const data = await http.getRecordList(searchFormData)
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
        ? http.updateRecord
        : http.createRecord
    if (dialogTitle.value !== '修改信息') {
      dialogFormData.userid = userInfo.value.id
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

    await http.deleteRecord(row.id)
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