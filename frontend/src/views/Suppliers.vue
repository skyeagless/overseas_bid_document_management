<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>供应商/厂家信息库</span>
          <el-button type="primary" @click="showDialog()">新增记录</el-button>
        </div>
      </template>
      <el-table :data="tableData" stripe style="width: 100%">
        <el-table-column prop="name" label="供应商名称" min-width="180" />
        <el-table-column prop="contact_person" label="联系人" width="100" />
        <el-table-column prop="phone" label="电话" width="130" />
        <el-table-column prop="product_specs" label="产品规格" min-width="200" show-overflow-tooltip />
        <el-table-column prop="certifications" label="认证情况" width="150" />
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
        <el-form-item label="供应商名称" required>
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="联系人">
          <el-input v-model="form.contact_person" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.address" />
        </el-form-item>
        <el-form-item label="产品规格">
          <el-input v-model="form.product_specs" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="认证情况">
          <el-input v-model="form.certifications" placeholder="如：ISO9001、CE认证" />
        </el-form-item>
        <el-form-item label="合作历史">
          <el-input v-model="form.cooperation_history" type="textarea" :rows="2" />
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
  contact_person: '',
  phone: '',
  email: '',
  address: '',
  product_specs: '',
  certifications: '',
  cooperation_history: ''
})

const loadData = async () => {
  const res = await api.getSuppliers()
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
      contact_person: '',
      phone: '',
      email: '',
      address: '',
      product_specs: '',
      certifications: '',
      cooperation_history: ''
    }
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.value.name) {
    ElMessage.warning('请填写供应商名称')
    return
  }
  if (isEdit.value) {
    await api.updateSupplier(editId.value, form.value)
    ElMessage.success('更新成功')
  } else {
    await api.createSupplier(form.value)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
  loadData()
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该记录？', '提示', { type: 'warning' })
  await api.deleteSupplier(id)
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
