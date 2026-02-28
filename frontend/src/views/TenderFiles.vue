<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>招标项目存档</span>
          <el-button type="primary" @click="showDialog()">新增记录</el-button>
        </div>
      </template>
      <el-table :data="tableData" stripe style="width: 100%">
        <el-table-column prop="project_name" label="招标项目名称" min-width="200" />
        <el-table-column prop="project_type" label="项目类型" width="120" />
        <el-table-column prop="region" label="地区" width="120" />
        <el-table-column prop="owner_name" label="业主名称" width="150" />
        <el-table-column prop="tender_date" label="招标日期" width="120" />
        <el-table-column label="招标文件" width="100">
          <template #default="{ row }">
            <el-link v-if="row.tender_file_path" type="primary" @click="downloadFile(row.tender_file_path)">下载</el-link>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="投标文件" width="100">
          <template #default="{ row }">
            <el-link v-if="row.bid_file_path" type="primary" @click="downloadFile(row.bid_file_path)">下载</el-link>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑记录' : '新增记录'" width="700px">
      <el-form :model="form" label-width="120px" class="dialog-form">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="招标项目名称" required>
              <el-input v-model="form.project_name" placeholder="请输入招标项目名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="项目类型">
              <el-input v-model="form.project_type" placeholder="如：电力工程" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="地区">
              <el-input v-model="form.region" placeholder="如：东南亚" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="业主名称">
              <el-input v-model="form.owner_name" placeholder="请输入业主名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="招标日期">
              <el-input v-model="form.tender_date" placeholder="如：2024-01" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="招标文件">
              <el-upload
                :action="uploadUrl"
                :on-success="handleTenderFileSuccess"
                :show-file-list="false"
                accept=".zip,.rar,.pdf,.doc,.docx"
                style="width: 100%"
              >
                <el-button size="small">选择文件</el-button>
                <span v-if="form.tender_file_path" style="margin-left: 10px; color: #67c23a">已上传</span>
              </el-upload>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="投标文件">
              <el-upload
                :action="uploadUrl"
                :on-success="handleBidFileSuccess"
                :show-file-list="false"
                accept=".zip,.rar,.pdf,.doc,.docx"
                style="width: 100%"
              >
                <el-button size="small">选择文件</el-button>
                <span v-if="form.bid_file_path" style="margin-left: 10px; color: #67c23a">已上传</span>
              </el-upload>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="描述">
              <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入项目描述" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const tableData = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const uploadUrl = '/api/upload'

const form = ref({
  project_name: '',
  project_type: '',
  region: '',
  owner_name: '',
  tender_date: '',
  tender_file_path: '',
  bid_file_path: '',
  description: ''
})

const loadData = async () => {
  const res = await api.getTenderFiles()
  tableData.value = res.data
}

const showDialog = (row) => {
  if (row) {
    isEdit.value = true
    editId.value = row.id
    form.value = { ...row }
  } else {
    isEdit.value = false
    editId.value = null
    form.value = {
      project_name: '',
      project_type: '',
      region: '',
      owner_name: '',
      tender_date: '',
      tender_file_path: '',
      bid_file_path: '',
      description: ''
    }
  }
  dialogVisible.value = true
}

const handleTenderFileSuccess = (res) => {
  form.value.tender_file_path = res.filename
  ElMessage.success('招标文件上传成功')
}

const handleBidFileSuccess = (res) => {
  form.value.bid_file_path = res.filename
  ElMessage.success('投标文件上传成功')
}

const downloadFile = (filename) => {
  window.open(`/api/uploads/${filename}`)
}

const handleSubmit = async () => {
  if (!form.value.project_name) {
    ElMessage.warning('请填写招标项目名称')
    return
  }
  if (isEdit.value) {
    await api.updateTenderFile(editId.value, form.value)
    ElMessage.success('更新成功')
  } else {
    await api.createTenderFile(form.value)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
  loadData()
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该记录？', '提示', { type: 'warning' })
  await api.deleteTenderFile(id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page-container {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-form :deep(.el-form-item__label) {
  text-align: right;
  padding-right: 12px;
}
</style>
