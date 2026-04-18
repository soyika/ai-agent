from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class TaskRequest(BaseModel):
    intent: str = Field(..., description="用户意图描述")
    task: str = Field(..., description="具体任务描述")
    context: dict = Field(default_factory=dict, description="任务上下文")
    priority: str = Field(default="normal", description="任务优先级")


@router.post("/dispatch")
async def dispatch_task(request: TaskRequest):
    from app.core.agent_orchestrator import AgentOrchestrator
    orchestrator = AgentOrchestrator()
    result = await orchestrator.dispatch_task(request)
    return result


@router.post("/dispatch/stream")
async def dispatch_task_stream(request: TaskRequest):
    from fastapi.responses import StreamingResponse
    from app.core.agent_orchestrator import AgentOrchestrator

    orchestrator = AgentOrchestrator()

    async def generate():
        async for chunk in orchestrator.dispatch_task_stream(request):
            yield chunk

    return StreamingResponse(generate(), media_type="text/event-stream")
