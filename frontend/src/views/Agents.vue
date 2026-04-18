<template>
  <div class="agents-container">
    <el-card>
      <template #header>
        <h2>智能体集群管理</h2>
      </template>
      <el-row :gutter="20">
        <el-col :span="8" v-for="agent in agents" :key="agent.name">
          <el-card shadow="hover" class="agent-card">
            <div class="agent-header">
              <el-icon class="agent-icon" :size="40"><Cpu /></el-icon>
              <el-tag :type="agent.status === 'online' ? 'success' : 'danger'">
                {{ agent.status === 'online' ? '运行中' : '已停止' }}
              </el-tag>
            </div>
            <h3>{{ agent.name }}</h3>
            <p class="agent-desc">{{ agent.description }}</p>
            <div class="agent-capabilities">
              <el-tag v-for="cap in agent.capabilities" :key="cap" size="small" style="margin: 4px;">
                {{ cap }}
              </el-tag>
            </div>
            <div class="agent-stats">
              <div class="stat">
                <div class="stat-value">{{ agent.tasksToday }}</div>
                <div class="stat-label">今日任务</div>
              </div>
              <div class="stat">
                <div class="stat-value">{{ agent.successRate }}%</div>
                <div class="stat-label">成功率</div>
              </div>
              <div class="stat">
                <div class="stat-value">{{ agent.avgTime }}s</div>
                <div class="stat-label">平均响应</div>
              </div>
            </div>
            <div class="agent-actions">
              <el-button type="primary" size="small">查看详情</el-button>
              <el-button size="small">测试对话</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Cpu } from '@element-plus/icons-vue'

const agents = ref([
  {
    name: '环境控制 Agent',
    description: '负责温度、湿度、光照、通风等环境参数调控',
    capabilities: ['温湿度监测', '光照管理', '通风控制', 'CO2调节', '极端天气预警'],
    status: 'online',
    tasksToday: 24,
    successRate: 99.2,
    avgTime: 1.2,
  },
  {
    name: '病虫害识别 Agent',
    description: '基于图像识别技术检测和诊断猕猴桃病虫害',
    capabilities: ['图像识别', '病害诊断', '虫害识别', '防治推荐'],
    status: 'online',
    tasksToday: 8,
    successRate: 95.6,
    avgTime: 2.8,
  },
  {
    name: '水肥决策 Agent',
    description: '根据土壤墒情、作物生长阶段制定水肥方案',
    capabilities: ['土壤分析', '灌溉计划', '施肥方案', '水肥配比'],
    status: 'online',
    tasksToday: 12,
    successRate: 98.1,
    avgTime: 1.5,
  },
  {
    name: '物候预测 Agent',
    description: '预测猕猴桃物候期和采收时间',
    capabilities: ['物候期预测', '采收期预测', '产量预估'],
    status: 'online',
    tasksToday: 3,
    successRate: 92.4,
    avgTime: 3.1,
  },
  {
    name: '农事问答 Agent',
    description: '回答猕猴桃种植相关的农业技术问题',
    capabilities: ['技术咨询', '修剪指导', '病虫害问答', '品种建议'],
    status: 'online',
    tasksToday: 156,
    successRate: 97.8,
    avgTime: 0.8,
  },
  {
    name: '订单履约 Agent',
    description: '处理猕猴桃销售订单和物流配送',
    capabilities: ['订单处理', '库存管理', '物流规划', '售后处理'],
    status: 'online',
    tasksToday: 45,
    successRate: 99.5,
    avgTime: 0.5,
  },
  {
    name: '客户运营 Agent',
    description: '客户关系管理和营销运营',
    capabilities: ['客户管理', '精准营销', '社群运营', '会员体系'],
    status: 'online',
    tasksToday: 28,
    successRate: 96.3,
    avgTime: 1.0,
  },
])
</script>

<style scoped>
.agents-container {
  padding: 0;
}
.agent-card {
  margin-bottom: 20px;
}
.agent-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.agent-icon {
  color: #409EFF;
}
.agent-card h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
}
.agent-desc {
  color: #909399;
  font-size: 14px;
  margin: 0 0 12px 0;
  line-height: 1.5;
}
.agent-capabilities {
  margin-bottom: 16px;
}
.agent-stats {
  display: flex;
  justify-content: space-around;
  padding: 12px 0;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 12px;
}
.stat {
  text-align: center;
}
.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}
.stat-label {
  font-size: 12px;
  color: #909399;
}
.agent-actions {
  display: flex;
  gap: 8px;
}
.agent-actions .el-button {
  flex: 1;
}
</style>
