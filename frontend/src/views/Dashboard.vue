<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6" v-for="stat in stats" :key="stat.title">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon class="stat-icon" :style="{ color: stat.color }"><component :is="stat.icon" /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-title">{{ stat.title }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <template #header>果园数字孪生地图</template>
          <div ref="chartRef" style="height: 400px;"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>实时环境数据</template>
          <div class="sensor-data">
            <div v-for="sensor in sensors" :key="sensor.name" class="sensor-item">
              <div class="sensor-label">{{ sensor.name }}</div>
              <div class="sensor-value">{{ sensor.value }} {{ sensor.unit }}</div>
              <el-progress :percentage="sensor.percent" :color="sensor.color" />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>智能体状态</template>
          <el-table :data="agents" style="width: 100%">
            <el-table-column prop="name" label="智能体" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'online' ? 'success' : 'danger'">{{ row.status === 'online' ? '在线' : '离线' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="tasks" label="今日任务" width="100" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>最近告警</template>
          <el-timeline>
            <el-timeline-item v-for="alert in alerts" :key="alert.time" :timestamp="alert.time" placement="top" :type="alert.type">
              {{ alert.message }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref<HTMLElement | null>(null)

const stats = ref([
  { title: '果园面积', value: '500 亩', icon: 'Sunny', color: '#409EFF' },
  { title: '传感器数量', value: '128', icon: 'Cpu', color: '#67C23A' },
  { title: '今日订单', value: '45', icon: 'Watermelon', color: '#E6A23C' },
  { title: '活跃告警', value: '3', icon: 'Bell', color: '#F56C6C' },
])

const sensors = ref([
  { name: '温度', value: 22.5, unit: '°C', percent: 75, color: '#E6A23C' },
  { name: '湿度', value: 68, unit: '%', percent: 68, color: '#409EFF' },
  { name: '土壤湿度', value: 45, unit: '%', percent: 45, color: '#67C23A' },
  { name: '光照强度', value: 12500, unit: 'lux', percent: 62, color: '#E6A23C' },
])

const agents = ref([
  { name: '环境控制 Agent', status: 'online', tasks: 24 },
  { name: '病虫害识别 Agent', status: 'online', tasks: 8 },
  { name: '水肥决策 Agent', status: 'online', tasks: 12 },
  { name: '物候预测 Agent', status: 'online', tasks: 3 },
  { name: '农事问答 Agent', status: 'online', tasks: 156 },
  { name: '订单履约 Agent', status: 'online', tasks: 45 },
  { name: '客户运营 Agent', status: 'online', tasks: 28 },
])

const alerts = ref([
  { time: '10:23', message: '3号大棚温度偏高 (28°C)', type: 'warning' },
  { time: '09:45', message: '土壤湿度低于阈值', type: 'danger' },
  { time: '08:12', message: '订单 #20241201 待发货', type: 'primary' },
])

onMounted(() => {
  if (chartRef.value) {
    const chart = echarts.init(chartRef.value)
    const option = {
      tooltip: {},
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: { data: ['A区', 'B区', 'C区', 'D区', 'E区', 'F区'] },
      yAxis: {},
      series: [{
        name: '产量 (kg)',
        type: 'bar',
        data: [4500, 5200, 4800, 6100, 5500, 4900],
        itemStyle: { color: '#67C23A' },
      }],
    }
    chart.setOption(option)
  }
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}
.stats-row {
  margin-bottom: 20px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
}
.stat-icon {
  font-size: 40px;
}
.stat-info {
  flex: 1;
}
.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}
.stat-title {
  font-size: 14px;
  color: #909399;
}
.sensor-data {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.sensor-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.sensor-label {
  font-size: 14px;
  color: #606266;
}
.sensor-value {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}
</style>
