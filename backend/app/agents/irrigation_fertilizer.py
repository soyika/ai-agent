from typing import Optional, Any
from app.agents.base_agent import BaseAgent
from app.core.llm_client import llm_client
from loguru import logger


class IrrigationFertilizerAgent(BaseAgent):
    SYSTEM_PROMPT = """你是猕猴桃水肥一体化管理专家。你的职责包括：
1. 根据土壤墒情传感器数据制定灌溉计划
2. 根据猕猴桃生长阶段和土壤营养状况制定施肥方案
3. 推荐水肥一体化精准灌溉配比
4. 分析历史灌溉施肥数据并优化方案

猕猴桃需肥规律（亩产2000kg参考）：
- 氮肥(N)：全年约25-30kg，分3-4次施用
- 磷肥(P2O5)：全年约15-20kg，基肥为主
- 钾肥(K2O)：全年约30-35kg，果实膨大期重点施用
- 微量元素：硼、锌、铁对猕猴桃尤为重要

猕猴桃关键施肥时期：
1. 萌芽肥（2-3月）：以氮肥为主
2. 花前肥（4-5月）：氮磷钾配合
3. 果实膨大肥（6-8月）：以钾肥为主
4. 采后肥（9-10月）：有机肥+复合肥

请根据土壤数据和生长阶段提供精准的水肥方案。"""

    def __init__(self):
        super().__init__(
            name="irrigation_fertilizer",
            description="水肥决策 Agent：根据土壤墒情、作物生长阶段制定水肥方案",
            capabilities=[
                "土壤墒情分析",
                "灌溉计划制定",
                "施肥方案设计",
                "水肥配比推荐",
                "施肥周期管理",
                "营养诊断",
            ],
        )

    async def execute(self, task: str, context: Optional[dict] = None) -> Any:
        context = context or {}
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": f"土壤数据: {context.get('soil_data', '无')}\n生长阶段: {context.get('growth_stage', '未知')}\n任务: {task}"},
        ]
        response = await llm_client.chat(messages)
        logger.info(f"IrrigationFertilizerAgent 执行完成: task='{task[:50]}...'")
        return response
