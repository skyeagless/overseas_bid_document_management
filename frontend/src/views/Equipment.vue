<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>关键设备信息库</span>
          <el-button type="primary" @click="showDialog()">新增记录</el-button>
        </div>
      </template>
      <el-table :data="tableData" stripe style="width: 100%">
        <el-table-column prop="name" label="设备名称" min-width="150" />
        <el-table-column prop="model" label="型号" width="120" />
        <el-table-column prop="brand" label="品牌" width="100" />
        <el-table-column prop="tech_params" label="技术参数" min-width="200" show-overflow-tooltip />
        <el-table-column prop="supplier_name" label="供应商" width="150" />
        <el-table-column prop="price" label="价格" width="100" />
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
        <el-form-item label="设备名称" required>
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="型号">
          <el-input v-model="form.model" />
        </el-form-item>
        <el-form-item label="品牌">
          <el-input v-model="form.brand" />
        </el-form-item>
        <el-form-item label="技术参数">
          <el-input v-model="form.tech_params" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="性能指标">
          <el-input v-model="form.performance" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="供应商">
          <el-select v-model="form.supplier_id" placeholder="请选择供应商" style="width: 100%">
            <el-option
              v-for="item in suppliers"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="价格">
          <el-input v-model="form.price" />
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
const suppliers = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const form = ref({
  name: '',
  model: '',
  brand: '',
  tech_params: '',
  performance: '',
  supplier_id: null,
  price: ''
})

const loadData = async () => {
  const res = await api.getEquipment()
  tableData.value = res.data
}

const loadSuppliers = async () => {
  const res = await api.getSuppliers()
  suppliers.value = res.data
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
      model: '',
      brand: '',
      tech_params: '',
      performance: '',
      supplier_id: null,
      price: ''
    }
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.value.name) {
    ElMessage.warning('请填写设备名称')
    return
  }
  if (isEdit.value) {
    await api.updateEquipment(editId.value, form.value)
    ElMessage.success('更新成功')
  } else {
    await api.createEquipment(form.value)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
  loadData()
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该记录？', '提示', { type: 'warning' })
  await api.deleteEquipment(id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(() => {
  loadData()
  loadSuppliers()
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
