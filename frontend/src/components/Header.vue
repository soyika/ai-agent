<template>
  <el-header class="header">
    <div class="header-left">
      <img src="/logo.svg" alt="Logo" class="logo" />
      <h1>猕猴桃智慧种植与产销一体化 AI Agent 平台</h1>
    </div>
    <div class="header-right">
      <el-badge :value="alerts" class="notification">
        <el-icon><Bell /></el-icon>
      </el-badge>
      <el-avatar :size="32" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
      <span>管理员</span>
    </div>
  </el-header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Bell } from '@element-plus/icons-vue'

const alerts = ref(3)
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px !important;
  height: 60px !important;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.logo {
  height: 32px;
}
.header h1 {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
  margin: 0;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
}
.notification {
  font-size: 18px;
}
</style>
