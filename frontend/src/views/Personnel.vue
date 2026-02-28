<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>人员信息库</span>
          <el-button type="primary" @click="showDialog()">新增记录</el-button>
        </div>
      </template>
      <el-table :data="tableData" stripe style="width: 100%">
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="company" label="所在单位" min-width="150" />
        <el-table-column prop="position" label="职位" width="100" />
        <el-table-column prop="qualification" label="资质证书" min-width="150" show-overflow-tooltip />
        <el-table-column prop="specialty" label="专业背景" width="120" />
        <el-table-column prop="phone" label="电话" width="130" />
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
        <el-form-item label="姓名" required>
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="所在单位">
          <el-input v-model="form.company" />
        </el-form-item>
        <el-form-item label="职位">
          <el-input v-model="form.position" />
        </el-form-item>
        <el-form-item label="资质证书">
          <el-input v-model="form.qualification" placeholder="如：一级建造师、高级工程师" />
        </el-form-item>
        <el-form-item label="专业背景">
          <el-input v-model="form.specialty" placeholder="如：电气工程、土木工程" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="项目经验">
          <el-input v-model="form.experience" type="textarea" :rows="3" />
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
  name: '',
  company: '',
  position: '',
  qualification: '',
  specialty: '',
  phone: '',
  email: '',
  experience: ''
})

const loadData = async () => {
  const res = await api.getPersonnel()
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
      name: '',
      company: '',
      position: '',
      qualification: '',
      specialty: '',
      phone: '',
      email: '',
      experience: ''
    }
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.value.name) {
    ElMessage.warning('请填写姓名')
    return
  }
  if (isEdit.value) {
    await api.updatePerson(editId.value, form.value)
    ElMessage.success('更新成功')
  } else {
    await api.createPersonnel(form.value)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
  loadData()
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该记录？', '提示', { type: 'warning' })
  await api.deletePerson(id)
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
