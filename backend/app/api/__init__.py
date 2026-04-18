from fastapi import APIRouter

router = APIRouter()

from .health import router as health_router
from .chat import router as chat_router
from .agents import router as agents_router
from .iot import router as iot_router
from .orchestrator import router as orchestrator_router

router.include_router(health_router, prefix="/health", tags=["Health"])
router.include_router(chat_router, prefix="/chat", tags=["Chat"])
router.include_router(agents_router, prefix="/agents", tags=["Agents"])
router.include_router(iot_router, prefix="/iot", tags=["IoT"])
router.include_router(orchestrator_router, prefix="/orchestrator", tags=["Orchestrator"])
