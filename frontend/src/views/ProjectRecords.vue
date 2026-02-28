<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>工程业绩档案</span>
          <el-button type="primary" @click="showDialog()">新增记录</el-button>
        </div>
      </template>
      <el-table :data="tableData" stripe style="width: 100%">
        <el-table-column prop="project_name" label="项目名称" min-width="200" />
        <el-table-column prop="scale" label="项目规模" width="120" />
        <el-table-column prop="industry" label="行业" width="120" />
        <el-table-column prop="completion_date" label="完成时间" width="120" />
        <el-table-column prop="contract_value" label="合同金额" width="120" />
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑记录' : '新增记录'" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="项目名称" required>
          <el-input v-model="form.project_name" />
        </el-form-item>
        <el-form-item label="项目规模">
          <el-input v-model="form.scale" placeholder="如：大型、中型、小型" />
        </el-form-item>
        <el-form-item label="行业">
          <el-input v-model="form.industry" placeholder="如：电力、交通、建筑" />
        </el-form-item>
        <el-form-item label="完成时间">
          <el-input v-model="form.completion_date" placeholder="如：2024-06" />
        </el-form-item>
        <el-form-item label="合同金额">
          <el-input v-model="form.contract_value" placeholder="如：5000万元" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
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
const form = ref({
  project_name: '',
  scale: '',
  industry: '',
  completion_date: '',
  contract_value: '',
  description: ''
})

const loadData = async () => {
  const res = await api.getProjectRecords()
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
      scale: '',
      industry: '',
      completion_date: '',
      contract_value: '',
      description: ''
    }
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.value.project_name) {
    ElMessage.warning('请填写项目名称')
    return
  }
  if (isEdit.value) {
    await api.updateProjectRecord(editId.value, form.value)
    ElMessage.success('更新成功')
  } else {
    await api.createProjectRecord(form.value)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
  loadData()
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该记录？', '提示', { type: 'warning' })
  await api.deleteProjectRecord(id)
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
</style>
