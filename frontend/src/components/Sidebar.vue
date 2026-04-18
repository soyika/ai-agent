<template>
  <el-menu
    :default-active="activeMenu"
    class="sidebar-menu"
    router
  >
    <el-menu-item index="/">
      <el-icon><HomeFilled /></el-icon>
      <span>管理驾驶舱</span>
    </el-menu-item>
    <el-menu-item index="/chat">
      <el-icon><ChatDotRound /></el-icon>
      <span>AI 农事助手</span>
    </el-menu-item>
    <el-menu-item index="/agents">
      <el-icon><Cpu /></el-icon>
      <span>智能体集群</span>
    </el-menu-item>
    <el-sub-menu index="/iot">
      <template #title>
        <el-icon><Connection /></el-icon>
        <span>物联网监控</span>
      </template>
      <el-menu-item index="/iot/sensors">传感器数据</el-menu-item>
      <el-menu-item index="/iot/devices">设备管理</el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/farm">
      <template #title>
        <el-icon><Sunny /></el-icon>
        <span>果园管理</span>
      </template>
      <el-menu-item index="/farm/environment">环境控制</el-menu-item>
      <el-menu-item index="/farm/pest">病虫害管理</el-menu-item>
      <el-menu-item index="/farm/water-fertilizer">水肥决策</el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/business">
      <template #title>
        <el-icon><ShoppingCart /></el-icon>
        <span>产销经营</span>
      </template>
      <el-menu-item index="/business/orders">订单管理</el-menu-item>
      <el-menu-item index="/business/customers">客户管理</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled, ChatDotRound, Cpu, Connection, Sunny, ShoppingCart } from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.sidebar-menu {
  border-right: none;
  height: 100%;
}
</style>
