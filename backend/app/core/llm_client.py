from abc import ABC, abstractmethod
from typing import Optional, AsyncGenerator
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = "user"
    content: str


class ChatCompletionRequest(BaseModel):
    messages: list[Message] = Field(default_factory=list)
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class ChatCompletionResponse(BaseModel):
    content: str
    model: str
    usage: Optional[dict] = None


class BaseLLMClient(ABC):
    @abstractmethod
    async def chat(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        pass

    @abstractmethod
    async def chat_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncGenerator[str, None]:
        pass


class LLMClient:
    def __init__(self):
        self._provider = None
        self._client = None

    def _initialize_provider(self, provider: str):
        if self._provider == provider:
            return

        if provider == "openai":
            from langchain_openai import ChatOpenAI
            from app.core.config import settings

            self._client = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                base_url=settings.OPENAI_BASE_URL,
                api_key=settings.OPENAI_API_KEY,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                streaming=False,
            )
        elif provider == "dashscope":
            from langchain_openai import ChatOpenAI
            from app.core.config import settings

            self._client = ChatOpenAI(
                model=settings.DASHSCOPE_MODEL,
                base_url=settings.DASHSCOPE_BASE_URL,
                api_key=settings.DASHSCOPE_API_KEY,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                streaming=False,
            )
        elif provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            from app.core.config import settings

            self._client = ChatAnthropic(
                model=settings.ANTHROPIC_MODEL,
                api_key=settings.ANTHROPIC_API_KEY,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                streaming=False,
            )
        elif provider == "ollama":
            from langchain_ollama import ChatOllama
            from app.core.config import settings

            self._client = ChatOllama(
                model=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL,
                temperature=settings.LLM_TEMPERATURE,
                num_predict=settings.LLM_MAX_TOKENS,
                streaming=False,
            )
        else:
            raise ValueError(f"不支持的 LLM 提供商: {provider}")

        self._provider = provider

    async def chat(
        self,
        messages: list[dict[str, str]],
        provider: Optional[str] = None,
    ) -> str:
        from app.core.config import settings

        provider = provider or settings.LLM_PROVIDER
        self._initialize_provider(provider)

        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

        lc_messages = []
        for msg in messages:
            if msg["role"] == "system":
                lc_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))

        response = await self._client.ainvoke(lc_messages)
        return response.content

    async def chat_stream(
        self,
        messages: list[dict[str, str]],
        provider: Optional[str] = None,
    ):
        from app.core.config import settings
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

        provider = provider or settings.LLM_PROVIDER
        self._initialize_provider(provider)

        lc_messages = []
        for msg in messages:
            if msg["role"] == "system":
                lc_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))

        async for chunk in self._client.astream(lc_messages):
            yield chunk.content


# 全局 LLM 客户端实例
llm_client = LLMClient()
