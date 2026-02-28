<template>
  <el-container class="app-container">
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <h2>招投标资料管理</h2>
      </div>
      <el-menu
        :default-active="$route.path"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/tender-files">
          <el-icon><Document /></el-icon>
          <span>招标项目存档</span>
        </el-menu-item>
        <el-menu-item index="/project-records">
          <el-icon><Folder /></el-icon>
          <span>工程业绩档案</span>
        </el-menu-item>
        <el-menu-item index="/personnel">
          <el-icon><User /></el-icon>
          <span>人员信息库</span>
        </el-menu-item>
        <el-menu-item index="/suppliers">
          <el-icon><Shop /></el-icon>
          <span>供应商信息库</span>
        </el-menu-item>
        <el-menu-item index="/equipment">
          <el-icon><Tools /></el-icon>
          <span>设备信息库</span>
        </el-menu-item>
        <el-menu-item index="/search">
          <el-icon><Search /></el-icon>
          <span>全局搜索</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main class="main-content">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { Document, Folder, User, Shop, Tools, Search } from '@element-plus/icons-vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  font-family: 'Microsoft YaHei', sans-serif;
}

.app-container {
  height: 100%;
}

.sidebar {
  background-color: #304156;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #263445;
}

.logo h2 {
  color: #fff;
  font-size: 16px;
}

.el-menu {
  border-right: none;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
