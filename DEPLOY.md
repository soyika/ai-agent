# 猕猴桃智慧种植与产销一体化 AI Agent 平台 - 部署指南

> 本文档详细说明如何从零开始部署本系统，推荐使用 **阿里百炼 DashScope API**，无需本地部署大模型。

---

## 目录

1. [前置准备](#1-前置准备)
2. [获取阿里百炼 API Key](#2-获取阿里百炼-api-key)
3. [方式一：Docker Compose 一键部署（推荐）](#3-方式一docker-compose-一键部署推荐)
4. [方式二：本地开发模式部署](#4-方式二本地开发模式部署)
5. [验证部署](#5-验证部署)
6. [可选：切换其他 LLM 提供商](#6-可选切换其他-llm-提供商)
7. [常见问题](#7-常见问题)

---

## 1. 前置准备

### 系统要求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| CPU | 2 核 | 4 核+ |
| 内存 | 4 GB | 8 GB+ |
| 磁盘 | 20 GB | 50 GB+ |
| 操作系统 | Windows 10/11, macOS, Linux | Ubuntu 22.04 LTS |

### 必装软件

- **Docker** (20.10+) 及 **Docker Compose** (2.0+)
- **Git** (2.30+)
- **浏览器** (Chrome/Edge/Firefox 最新版)

### 选装软件（本地开发模式）

- **Python** 3.11+
- **Node.js** 18+

---

## 2. 获取阿里百炼 API Key

### 2.1 注册/登录阿里云

访问 [阿里云百炼平台](https://bailian.console.aliyun.com/)，使用阿里云账号登录。

### 2.2 开通百炼服务

1. 进入 **百炼控制台**
2. 点击 **模型服务** > **模型列表**
3. 找到 `qwen-plus` 或 `qwen-max` 模型，点击 **开通**

### 2.3 创建 API Key

1. 在百炼控制台左侧导航栏，找到 **API Key 管理**
2. 点击 **创建 API Key**
3. 复制生成的 Key（格式类似 `sk-xxxxxxxxxxxxxxxxxxxxxxxx`）

> **注意**: API Key 仅显示一次，请妥善保存！

### 2.4 模型选择建议

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| `qwen-turbo` | 速度快，成本低 | 简单问答、快速响应 |
| `qwen-plus` (推荐) | 性能均衡 | 日常对话、任务调度 |
| `qwen-max` | 能力最强 | 复杂推理、深度分析 |

---

## 3. 方式一：Docker Compose 一键部署（推荐）

### 3.1 克隆项目

```bash
git clone https://github.com/soyika/ai-agent.git
cd ai-agent
```

### 3.2 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env
```

编辑 `.env` 文件，修改以下配置：

```env
# 修改 LLM 提供商为 dashscope（默认已是 dashscope）
LLM_PROVIDER=dashscope

# 填入你的阿里百炼 API Key
DASHSCOPE_API_KEY=sk-你的API密钥

# 可选：修改模型（推荐 qwen-plus）
DASHSCOPE_MODEL=qwen-plus
```

其他配置保持默认即可。

### 3.3 启动服务

```bash
docker-compose up -d
```

首次启动会下载镜像并构建，大约需要 5-10 分钟。

### 3.4 查看服务状态

```bash
docker-compose ps
```

预期输出：

```
NAME                   STATUS          PORTS
ai-agent-postgres-1    Up (healthy)    0.0.0.0:5432->5432/tcp
ai-agent-influxdb-1    Up              0.0.0.0:8086->8086/tcp
ai-agent-redis-1       Up              0.0.0.0:6379->6379/tcp
ai-agent-mqtt-1        Up              0.0.0.0:1883->1883/tcp
ai-agent-backend-1     Up              0.0.0.0:8000->8000/tcp
ai-agent-frontend-1    Up              0.0.0.0:3000->80/tcp
```

### 3.5 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 仅查看后端日志
docker-compose logs -f backend
```

### 3.6 停止服务

```bash
docker-compose down

# 如需清除数据卷
docker-compose down -v
```

---

## 4. 方式二：本地开发模式部署

如果您需要开发或调试，可以使用本地开发模式。

### 4.1 克隆项目

```bash
git clone https://github.com/soyika/ai-agent.git
cd ai-agent
```

### 4.2 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
LLM_PROVIDER=dashscope
DASHSCOPE_API_KEY=sk-你的API密钥
DASHSCOPE_MODEL=qwen-plus

# 数据库保持默认 localhost 配置
POSTGRES_HOST=localhost
```

### 4.3 启动基础设施（Docker）

仅需启动数据库和中间件：

```bash
docker-compose up -d postgres influxdb redis mqtt
```

### 4.4 启动后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端将运行在 `http://localhost:8000`

### 4.5 启动前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将运行在 `http://localhost:5173`

### 4.6 启动 IoT 网关（可选）

```bash
cd iot-gateway
npm install
node index.js
```

---

## 5. 验证部署

### 5.1 健康检查

访问 `http://localhost:8000/health`，应返回：

```json
{
  "status": "ok",
  "app": "kiwi-ai-platform",
  "version": "1.0.0",
  "llm_provider": "dashscope"
}
```

### 5.2 API 文档

访问 `http://localhost:8000/api/v1/docs` 查看 Swagger API 文档。

### 5.3 测试对话

使用 curl 测试 AI 对话：

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "你好，请介绍一下猕猴桃种植的注意事项"}
    ]
  }'
```

### 5.4 访问管理驾驶舱

在浏览器中打开 `http://localhost:5173`（本地开发）或 `http://localhost:3000`（Docker 部署）。

---

## 6. 可选：切换其他 LLM 提供商

### 切换到 OpenAI

修改 `.env`：

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-你的OpenAI密钥
OPENAI_MODEL=gpt-4o
```

### 切换到 Ollama（本地部署）

如果您有 GPU 或希望离线运行：

1. 安装 Ollama：https://ollama.com/

2. 拉取模型：

```bash
ollama pull qwen2.5:7b
```

3. 修改 `.env`：

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:7b
```

### 切换到 Anthropic Claude

修改 `.env`：

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-你的Claude密钥
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

---

## 7. 常见问题

### Q1: Docker 启动后后端报错 "LLM provider not configured"

**原因**: 未正确配置 DashScope API Key。

**解决**: 检查 `.env` 文件中 `DASHSCOPE_API_KEY` 是否已正确填写。

```bash
docker-compose restart backend
```

### Q2: 前端页面无法访问

**原因**: 前端未正确构建或端口冲突。

**解决**:

```bash
# Docker 模式
docker-compose logs frontend

# 本地模式
# 确认 5173 端口未被占用
netstat -an | grep 5173
```

### Q3: 数据库连接失败

**原因**: PostgreSQL 未启动或端口冲突。

**解决**:

```bash
# 检查 PostgreSQL 状态
docker-compose ps postgres

# 重启数据库
docker-compose restart postgres
```

### Q4: 如何重置数据库数据

```bash
docker-compose down -v
docker-compose up -d
```

> **警告**: 此操作将清除所有数据库数据！

### Q5: 如何更新到最新版本

```bash
git pull origin main
docker-compose up -d --build
```

### Q6: 生产环境部署注意事项

1. **修改 SECRET_KEY** 为随机强密码
2. **设置 APP_ENV=production**
3. **配置 HTTPS**（使用 Nginx 反向代理）
4. **修改数据库密码** 为强密码
5. **关闭 DEBUG 模式**（设置 DEBUG=False）
6. **配置 CORS_ORIGINS** 为实际域名

### Q7: DashScope 模型调用报错

**可能原因**:
- API Key 无效或已过期
- 模型未开通
- 余额不足

**排查步骤**:
1. 登录 [百炼控制台](https://bailian.console.aliyun.com/) 检查 API Key 状态
2. 确认模型已开通
3. 检查账户余额

### Q8: 如何查看 RAG 知识库状态

```bash
# 查看 ChromaDB 日志
docker-compose logs backend | grep RAG

# 或通过 API 查询
curl http://localhost:8000/api/v1/agents/farming_qa
```

---

## 附录：服务端口一览

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 (Web) | 3000 (Docker) / 5173 (本地) | 管理驾驶舱 |
| 后端 API | 8000 | FastAPI 服务 |
| API 文档 | 8000/api/v1/docs | Swagger UI |
| PostgreSQL | 5432 | 业务数据库 |
| InfluxDB | 8086 | IoT 时序数据库 |
| Redis | 6379 | 缓存/消息队列 |
| MQTT | 1883 | IoT 消息代理 |

---

## 技术支持

- GitHub Issues: https://github.com/soyika/ai-agent/issues
- 阿里百炼文档: https://help.aliyun.com/zh/model-studio/
