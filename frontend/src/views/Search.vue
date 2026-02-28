<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>全局搜索</span>
        </div>
      </template>
      <div class="search-box">
        <el-input
          v-model="keyword"
          placeholder="请输入关键字搜索"
          style="width: 400px"
          @keyup.enter="handleSearch"
        />
        <el-select v-model="category" placeholder="选择类别" style="width: 150px; margin-left: 10px">
          <el-option label="全部" value="all" />
          <el-option label="招标项目存档" value="tender" />
          <el-option label="工程业绩" value="project" />
          <el-option label="人员信息" value="personnel" />
          <el-option label="供应商" value="supplier" />
          <el-option label="设备" value="equipment" />
        </el-select>
        <el-button type="primary" @click="handleSearch" style="margin-left: 10px">搜索</el-button>
      </div>
    </el-card>

    <div v-if="searched" class="search-results">
      <el-card v-if="results.tender_files && results.tender_files.length" class="result-card">
        <template #header>
          <span>招标项目存档 ({{ results.tender_files.length }}条)</span>
        </template>
        <el-table :data="results.tender_files" stripe size="small">
          <el-table-column prop="project_name" label="招标项目名称" min-width="200" />
          <el-table-column prop="project_type" label="项目类型" width="120" />
          <el-table-column prop="region" label="地区" width="100" />
          <el-table-column prop="owner_name" label="业主名称" width="150" />
          <el-table-column prop="tender_date" label="招标日期" width="120" />
        </el-table>
      </el-card>

      <el-card v-if="results.project_records && results.project_records.length" class="result-card">
        <template #header>
          <span>工程业绩 ({{ results.project_records.length }}条)</span>
        </template>
        <el-table :data="results.project_records" stripe size="small">
          <el-table-column prop="project_name" label="项目名称" min-width="200" />
          <el-table-column prop="scale" label="规模" width="100" />
          <el-table-column prop="industry" label="行业" width="100" />
          <el-table-column prop="completion_date" label="完成时间" width="120" />
        </el-table>
      </el-card>

      <el-card v-if="results.personnel && results.personnel.length" class="result-card">
        <template #header>
          <span>人员信息 ({{ results.personnel.length }}条)</span>
        </template>
        <el-table :data="results.personnel" stripe size="small">
          <el-table-column prop="name" label="姓名" width="100" />
          <el-table-column prop="company" label="单位" min-width="150" />
          <el-table-column prop="position" label="职位" width="100" />
          <el-table-column prop="qualification" label="资质" min-width="150" />
          <el-table-column prop="specialty" label="专业" width="100" />
        </el-table>
      </el-card>

      <el-card v-if="results.suppliers && results.suppliers.length" class="result-card">
        <template #header>
          <span>供应商 ({{ results.suppliers.length }}条)</span>
        </template>
        <el-table :data="results.suppliers" stripe size="small">
          <el-table-column prop="name" label="供应商名称" min-width="180" />
          <el-table-column prop="contact_person" label="联系人" width="100" />
          <el-table-column prop="phone" label="电话" width="130" />
          <el-table-column prop="certifications" label="认证" width="150" />
        </el-table>
      </el-card>

      <el-card v-if="results.equipment && results.equipment.length" class="result-card">
        <template #header>
          <span>设备 ({{ results.equipment.length }}条)</span>
        </template>
        <el-table :data="results.equipment" stripe size="small">
          <el-table-column prop="name" label="设备名称" min-width="150" />
          <el-table-column prop="model" label="型号" width="120" />
          <el-table-column prop="brand" label="品牌" width="100" />
          <el-table-column prop="price" label="价格" width="100" />
        </el-table>
      </el-card>

      <el-empty v-if="isEmpty" description="未找到相关记录" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '../api'

const keyword = ref('')
const category = ref('all')
const searched = ref(false)
const results = ref({})

const isEmpty = computed(() => {
  if (!searched.value) return false
  const r = results.value
  return (!r.tender_files || !r.tender_files.length) &&
         (!r.project_records || !r.project_records.length) &&
         (!r.personnel || !r.personnel.length) &&
         (!r.suppliers || !r.suppliers.length) &&
         (!r.equipment || !r.equipment.length)
})

const handleSearch = async () => {
  if (!keyword.value.trim()) return
  const res = await api.search(keyword.value, category.value)
  results.value = res.data
  searched.value = true
}
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

.search-box {
  display: flex;
  align-items: center;
}

.search-results {
  margin-top: 20px;
}

.result-card {
  margin-bottom: 15px;
}
</style>
