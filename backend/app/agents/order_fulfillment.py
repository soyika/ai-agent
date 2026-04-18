from typing import Optional, Any
from app.agents.base_agent import BaseAgent
from app.core.llm_client import llm_client
from loguru import logger


class OrderFulfillmentAgent(BaseAgent):
    SYSTEM_PROMPT = """你是猕猴桃订单履约与物流管理专家。你的职责包括：
1. 处理销售订单（创建、确认、发货、完成）
2. 管理库存和仓储
3. 规划最优物流配送路线
4. 处理售后和退换货

猕猴桃储存与运输要求：
- 适宜储存温度：0°C (冷藏)
- 适宜湿度：90-95%
- 储存期：常温下7-14天，冷藏可达3-6个月
- 运输要求：冷链运输，防震包装

请根据订单信息和库存状态提供履约建议和物流方案。"""

    def __init__(self):
        super().__init__(
            name="order_fulfillment",
            description="订单履约 Agent：处理猕猴桃销售订单和物流配送",
            capabilities=[
                "订单处理",
                "库存管理",
                "物流规划",
                "仓储优化",
                "售后处理",
                "冷链监控",
            ],
        )

    async def execute(self, task: str, context: Optional[dict] = None) -> Any:
        context = context or {}
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": f"订单信息: {context.get('order_data', '无')}\n任务: {task}"},
        ]
        response = await llm_client.chat(messages)
        logger.info(f"OrderFulfillmentAgent 执行完成: task='{task[:50]}...'")
        return response
