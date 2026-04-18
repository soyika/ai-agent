from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.core.config import settings
from app.core.event_bus import event_bus
from app.core.agent_registry import agent_registry

# 配置日志
logger.remove()
logger.add(
    sys.stderr,
    level=settings.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    description="猕猴桃智慧种植与产销一体化 AI Agent 平台",
    version="1.0.0",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 生命周期事件
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info(f"启动 {settings.APP_NAME}")
    logger.info(f"环境: {settings.APP_ENV}")
    logger.info(f"LLM 提供商: {settings.LLM_PROVIDER}")
    logger.info(f"LLM 模型: {settings.LLM_MODEL}")
    logger.info("=" * 60)

    from app.core.agent_orchestrator import AgentOrchestrator
    from app.agents import register_all_agents

    # 注册所有 Agent
    register_all_agents(agent_registry)

    # 初始化核心调度器
    orchestrator = AgentOrchestrator()
    await orchestrator.initialize()
    logger.info("核心调度器初始化完成")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("正在关闭应用...")

# 健康检查
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "llm_provider": settings.LLM_PROVIDER,
    }

# 注册路由
from app.api import router as api_router
app.include_router(api_router, prefix=settings.API_PREFIX)
