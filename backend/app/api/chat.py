from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class ChatRequest(BaseModel):
    messages: list[dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    content: str


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    from app.core.llm_client import llm_client

    response = await llm_client.chat(request.messages)
    return ChatResponse(content=response)


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    from fastapi.responses import StreamingResponse
    from app.core.llm_client import llm_client

    async def generate():
        async for chunk in llm_client.chat_stream(request.messages):
            yield chunk

    return StreamingResponse(generate(), media_type="text/event-stream")
