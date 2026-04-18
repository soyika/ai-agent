# 猕猴桃智慧种植与产销一体化 AI Agent 平台

> 面向猕猴桃种植园的、基于大语言模型调度与多 Agent 协同的 **"感知-决策-执行-经营"** 全链路智能平台

## 项目简介

本平台深度融合农业物联网、机器视觉、作物生长模型与电商 CRM 逻辑，采用 **"一核多星、数据总线、事件驱动"** 的微服务架构，为猕猴桃种植园提供智能化的种植管理与产销经营解决方案。

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        交互端                                    │
│   ┌──────────┐    ┌──────────────┐    ┌──────────────────┐       │
│   │ 管理驾驶舱│    │ 农户助手小程序│    │ 物联网设备网关    │       │
│   │ (PC Web) │    │ (微信小程序)  │    │ (MQTT Gateway)   │       │
│   └──────────┘    └──────────────┘    └──────────────────┘       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                      核心调度层                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Agent Orchestrator                          │    │
│  │   ┌───────────┐  ┌───────────┐  ┌────────────────────┐  │    │
│  │   │意图识别   │  │任务拆解   │  │Agent 路由调度      │  │    │
│  │   └───────────┘  └───────────┘  └────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                      智能体集群                                  │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │
│  │环境控制│ │病虫害  │ │水肥    │ │物候    │ │农事    │        │
│  │Agent   │ │识别    │ │决策    │ │预测    │ │问答    │        │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘        │
│  ┌────────┐ ┌────────┐                                          │
│  │订单    │ │客户    │                                          │
│  │履约    │ │运营    │                                          │
│  └────────┘ └────────┘                                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                      数据总线                                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐        │
│  │ PostgreSQL │  │ InfluxDB   │  │ Chroma/Milvus      │        │
│  │ (业务数据) │  │ (IoT 时序) │  │ (向量知识库)       │        │
│  └────────────┘  └────────────┘  └────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

## 7 大核心智能体

| Agent | 描述 | 核心能力 |
|-------|------|----------|
| **环境控制 Agent** | 温度、湿度、光照、通风等环境参数调控 | 温湿度监测、光照管理、通风控制、极端天气预警 |
| **病虫害识别 Agent** | 基于图像识别技术检测和诊断猕猴桃病虫害 | 图像识别、病害诊断、虫害识别、防治推荐 |
| **水肥决策 Agent** | 根据土壤墒情、作物生长阶段制定水肥方案 | 土壤分析、灌溉计划、施肥方案、水肥配比 |
| **物候预测 Agent** | 预测猕猴桃物候期和采收时间 | 物候期预测、采收期预测、产量预估 |
| **农事问答 Agent** | 回答猕猴桃种植相关的农业技术问题 | 技术咨询、修剪指导、病虫害问答、品种建议 |
| **订单履约 Agent** | 处理猕猴桃销售订单和物流配送 | 订单处理、库存管理、物流规划、售后处理 |
| **客户运营 Agent** | 客户关系管理和营销运营 | 客户管理、精准营销、社群运营、会员体系 |

## 技术栈

| 层级 | 技术选型 |
|------|----------|
| **后端框架** | Python 3.11+ / FastAPI |
| **AI/LLM** | LangChain + Ollama/OpenAI/Claude |
| **RAG 架构** | ChromaDB + Sentence Transformers |
| **关系数据库** | PostgreSQL + SQLAlchemy + AsyncPG |
| **时序数据库** | InfluxDB 2.x |
| **消息队列** | Redis + Celery + MQTT |
| **前端框架** | Vue 3 + Vite + Element Plus |
| **数据可视化** | ECharts (果园数字孪生地图) |
| **容器化** | Docker + Docker Compose |

## 快速开始

### 前置要求

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- (可选) Ollama 本地模型部署

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd kiwi-ai-platform
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 配置你的 LLM API 密钥和数据库连接
```

### 3. Docker 一键启动

```bash
docker-compose up -d
```

### 4. 本地开发模式

**后端：**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

**IoT 网关：**
```bash
cd iot-gateway
npm install
node index.js
```

### 5. 访问应用

- 管理驾驶舱: http://localhost:5173
- API 文档: http://localhost:8000/api/v1/docs
- InfluxDB 管理: http://localhost:8086

## API 接口

### 核心接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/api/v1/chat` | AI 对话 |
| POST | `/api/v1/chat/stream` | AI 对话（流式） |
| POST | `/api/v1/orchestrator/dispatch` | 任务调度 |
| POST | `/api/v1/orchestrator/dispatch/stream` | 任务调度（流式） |
| GET | `/api/v1/agents` | 列出所有 Agent |
| POST | `/api/v1/iot/sensor` | 接收传感器数据 |
| GET | `/api/v1/iot/sensor/{device_id}` | 查询传感器历史数据 |

### 任务调度示例

```bash
curl -X POST http://localhost:8000/api/v1/orchestrator/dispatch \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "查询当前环境状态并判断是否需要浇水",
    "task": "根据土壤湿度和天气预报，制定今日灌溉计划",
    "context": {
      "soil_moisture": 35,
      "weather": "晴",
      "growth_stage": "果实膨大期"
    }
  }'
```

## 项目结构

```
kiwi-ai-platform/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── api/               # API 路由
│   │   ├── core/              # 核心模块 (配置/调度/事件总线)
│   │   ├── agents/            # 7 个子 Agent 实现
│   │   ├── services/          # 业务服务 (RAG 等)
│   │   ├── database/          # 数据库适配层
│   │   └── models/            # 数据模型
│   ├── main.py                # 应用入口
│   ├── requirements.txt       # Python 依赖
│   └── Dockerfile
├── frontend/                   # Vue 3 前端
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   ├── components/        # 通用组件
│   │   ├── api/               # API 调用
│   │   ├── store/             # Pinia 状态管理
│   │   └── router/            # 路由配置
│   ├── package.json
│   └── Dockerfile
├── iot-gateway/               # 物联网网关
│   ├── index.js
│   └── package.json
├── config/                    # 配置文件
├── deploy/                    # 部署配置
├── tests/                     # 测试
├── docker-compose.yml         # Docker 编排
├── .env.example               # 环境变量模板
└── README.md
```

## LLM 配置说明

### Ollama 本地部署 (推荐)

```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull qwen2.5:7b

# 启动服务
ollama serve
```

### OpenAI

在 `.env` 中配置：
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4o
```

### Anthropic Claude

在 `.env` 中配置：
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-xxx
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

## License

MIT License
