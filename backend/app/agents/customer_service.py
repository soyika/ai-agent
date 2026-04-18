from typing import Optional, Any
from app.agents.base_agent import BaseAgent
from app.core.llm_client import llm_client
from loguru import logger


class CustomerServiceAgent(BaseAgent):
    SYSTEM_PROMPT = """你是猕猴桃品牌客户关系运营专家。你的职责包括：
1. 客户关系管理(CRM)与会员营销
2. 客户咨询与投诉处理
3. 基于客户画像的精准营销
4. 社群运营与内容营销
5. 客户忠诚度管理与复购促进

猕猴桃客户运营策略：
- 新客：提供试吃装、首单优惠、种植知识科普
- 老客：会员积分、复购折扣、节日礼品
- 企业客户：定制礼盒、大宗采购优惠
- 渠道客户：批发价格体系、合作政策

请根据客户信息和运营需求，提供客户关系管理建议和营销方案。"""

    def __init__(self):
        super().__init__(
            name="customer_service",
            description="客户运营 Agent：客户关系管理和营销运营",
            capabilities=[
                "客户关系管理",
                "精准营销",
                "社群运营",
                "会员体系管理",
                "投诉处理",
                "复购促进",
            ],
        )

    async def execute(self, task: str, context: Optional[dict] = None) -> Any:
        context = context or {}
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": f"客户信息: {context.get('customer_data', '无')}\n任务: {task}"},
        ]
        response = await llm_client.chat(messages)
        logger.info(f"CustomerServiceAgent 执行完成: task='{task[:50]}...'")
        return response
