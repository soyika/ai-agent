from typing import Optional, AsyncGenerator
from pydantic import BaseModel, Field
from loguru import logger


class TaskRequest(BaseModel):
    intent: str
    task: str
    context: dict = Field(default_factory=dict)
    priority: str = "normal"


class TaskResponse(BaseModel):
    agent_name: str
    result: str
    status: str = "success"
    metadata: dict = Field(default_factory=dict)


class AgentOrchestrator:
    INTENT_MAPPING_PROMPT = """你是一个农业 AI 调度助手。根据用户的意图，判断应该调用哪个子智能体。

可用的智能体列表：
1. environment_control - 环境控制 Agent：负责温度、湿度、光照、通风等环境参数调控
2. pest_detection - 病虫害识别 Agent：基于图像识别技术检测和诊断猕猴桃病虫害
3. irrigation_fertilizer - 水肥决策 Agent：根据土壤墒情、作物生长阶段制定水肥方案
4. phenology_prediction - 物候预测 Agent：预测猕猴桃物候期和采收时间
5. farming_qa - 农事问答 Agent：回答猕猴桃种植相关的农业技术问题
6. order_fulfillment - 订单履约 Agent：处理猕猴桃销售订单和物流配送
7. customer_service - 客户运营 Agent：客户关系管理和营销运营

请仅返回 JSON 格式，包含以下字段：
{
    "agent_name": "选择的智能体名称",
    "confidence": 0.0-1.0,
    "reason": "选择理由"
}

用户意图: {intent}
任务描述: {task}
"""

    def __init__(self):
        self._initialized = False
        from app.core.llm_client import llm_client
        from app.core.agent_registry import agent_registry
        from app.core.event_bus import event_bus

        self.llm_client = llm_client
        self.agent_registry = agent_registry
        self.event_bus = event_bus

    async def initialize(self):
        if not self._initialized:
            logger.info("AgentOrchestrator 初始化完成")
            self._initialized = True

    async def analyze_intent(self, intent: str, task: str) -> dict:
        prompt = self.INTENT_MAPPING_PROMPT.format(intent=intent, task=task)
        messages = [{"role": "user", "content": prompt}]
        response = await self.llm_client.chat(messages)
        import json
        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            logger.warning(f"意图识别 JSON 解析失败，使用默认值: {response}")
            return {
                "agent_name": "farming_qa",
                "confidence": 0.5,
                "reason": "默认使用农事问答 Agent"
            }

    async def dispatch_task(self, request: TaskRequest) -> TaskResponse:
        intent_result = await self.analyze_intent(request.intent, request.task)
        agent_name = intent_result.get("agent_name", "farming_qa")
        confidence = intent_result.get("confidence", 0.0)

        logger.info(f"任务调度: intent='{request.intent}' -> agent={agent_name} (confidence={confidence})")

        await self.event_bus.publish("task.dispatched", {
            "agent_name": agent_name,
            "task": request.task,
            "context": request.context,
        })

        try:
            result = await self.agent_registry.dispatch(
                agent_name=agent_name,
                task=request.task,
                context=request.context,
            )

            response = TaskResponse(
                agent_name=agent_name,
                result=str(result),
                status="success",
                metadata={"confidence": confidence},
            )

            await self.event_bus.publish("task.completed", {
                "agent_name": agent_name,
                "result": str(result),
            })

            return response
        except Exception as e:
            logger.error(f"任务执行失败: {e}")
            return TaskResponse(
                agent_name=agent_name,
                result=f"执行失败: {str(e)}",
                status="error",
            )

    async def dispatch_task_stream(self, request: TaskRequest) -> AsyncGenerator[str, None]:
        import json
        intent_result = await self.analyze_intent(request.intent, request.task)
        agent_name = intent_result.get("agent_name", "farming_qa")

        yield json.dumps({"type": "intent_analysis", "data": intent_result}, ensure_ascii=False) + "\n"

        yield json.dumps({"type": "agent_selected", "data": {"agent_name": agent_name}}, ensure_ascii=False) + "\n"

        try:
            result = await self.agent_registry.dispatch(
                agent_name=agent_name,
                task=request.task,
                context=request.context,
            )
            yield json.dumps({
                "type": "result",
                "data": {"agent_name": agent_name, "result": str(result)},
            }, ensure_ascii=False) + "\n"
        except Exception as e:
            yield json.dumps({
                "type": "error",
                "data": {"error": str(e)},
            }, ensure_ascii=False) + "\n"
