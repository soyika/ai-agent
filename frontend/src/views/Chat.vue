<template>
  <div class="chat-container">
    <el-card class="chat-card">
      <template #header>
        <div class="chat-header">
          <h2>AI 农事助手</h2>
          <el-select v-model="selectedAgent" placeholder="选择智能体" style="width: 200px;">
            <el-option label="智能调度" value="orchestrator" />
            <el-option label="环境控制" value="environment_control" />
            <el-option label="病虫害识别" value="pest_detection" />
            <el-option label="水肥决策" value="irrigation_fertilizer" />
            <el-option label="物候预测" value="phenology_prediction" />
            <el-option label="农事问答" value="farming_qa" />
            <el-option label="订单履约" value="order_fulfillment" />
            <el-option label="客户运营" value="customer_service" />
          </el-select>
        </div>
      </template>
      <div class="chat-messages" ref="messagesRef">
        <div v-for="(msg, index) in messages" :key="index" class="message" :class="msg.role">
          <el-avatar :size="32" :src="msg.role === 'user' ? userAvatar : agentAvatar" />
          <div class="message-content">
            <div class="message-text">{{ msg.content }}</div>
            <div class="message-time">{{ msg.time }}</div>
          </div>
        </div>
        <div v-if="isLoading" class="message agent">
          <el-avatar :size="32" :src="agentAvatar" />
          <div class="message-content">
            <div class="message-text typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>
      <div class="chat-input">
        <el-input
          v-model="inputMessage"
          placeholder="请输入您的问题，如：猕猴桃现在需要浇水吗？"
          @keyup.enter="sendMessage"
          :disabled="isLoading"
        >
          <template #append>
            <el-button @click="sendMessage" :loading="isLoading">
              <el-icon><Promotion /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { Promotion } from '@element-plus/icons-vue'

const selectedAgent = ref('orchestrator')
const inputMessage = ref('')
const messages = ref<Array<{ role: string, content: string, time: string }>>([])
const isLoading = ref(false)
const messagesRef = ref<HTMLElement | null>(null)

const userAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
const agentAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value) return

  const now = new Date()
  const time = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`

  messages.value.push({
    role: 'user',
    content: inputMessage.value,
    time,
  })

  const userInput = inputMessage.value
  inputMessage.value = ''
  isLoading.value = true

  await nextTick()
  scrollToBottom()

  try {
    const response = await fetch('/api/v1/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: [{ role: 'user', content: userInput }],
      }),
    })
    const data = await response.json()

    messages.value.push({
      role: 'agent',
      content: data.content,
      time: `${new Date().getHours()}:${new Date().getMinutes().toString().padStart(2, '0')}`,
    })
  } catch (error) {
    messages.value.push({
      role: 'agent',
      content: '抱歉，AI 服务暂时不可用，请稍后再试。',
      time: `${new Date().getHours()}:${new Date().getMinutes().toString().padStart(2, '0')}`,
    })
  } finally {
    isLoading.value = false
    await nextTick()
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}
</script>

<style scoped>
.chat-container {
  height: calc(100vh - 120px);
}
.chat-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chat-header h2 {
  margin: 0;
  font-size: 18px;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.message {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}
.message.user {
  flex-direction: row-reverse;
}
.message-content {
  max-width: 70%;
}
.message-text {
  background: #f0f2f5;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.6;
}
.message.user .message-text {
  background: #409EFF;
  color: #fff;
}
.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
.message.user .message-time {
  text-align: right;
}
.typing span {
  display: inline-block;
  width: 6px;
  height: 6px;
  background: #909399;
  border-radius: 50%;
  margin: 0 2px;
  animation: typing 1.4s infinite;
}
.typing span:nth-child(2) {
  animation-delay: 0.2s;
}
.typing span:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}
.chat-input {
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
}
</style>
