from typing import Optional, Any
from app.agents.base_agent import BaseAgent
from app.core.llm_client import llm_client
from loguru import logger


class PhenologyPredictionAgent(BaseAgent):
    SYSTEM_PROMPT = """你是猕猴桃物候期预测专家。你的职责包括：
1. 根据气象数据和历史物候记录预测猕猴桃各物候期
2. 预测最佳采收期
3. 评估气候对物候期的影响
4. 提供物候期管理建议

猕猴桃主要物候期：
1. 休眠期：12月-次年2月
2. 伤流期：2月下旬-3月上旬
3. 萌芽期：3月中下旬
4. 展叶期：4月上中旬
5. 开花期：5月上中旬（花期约7-10天）
6. 果实膨大期：5月下旬-8月
7. 果实成熟期：8月下旬-10月（因品种而异）
   - 早熟品种：8月中下旬
   - 中熟品种：9月上中旬
   - 晚熟品种（海沃德）：10月上中旬

请根据气象数据和当前物候状态预测后续物候期及采收时间。"""

    def __init__(self):
        super().__init__(
            name="phenology_prediction",
            description="物候预测 Agent：预测猕猴桃物候期和采收时间",
            capabilities=[
                "物候期预测",
                "采收期预测",
                "气候变化影响评估",
                "物候期管理建议",
                "产量预估",
            ],
        )

    async def execute(self, task: str, context: Optional[dict] = None) -> Any:
        context = context or {}
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": f"气象数据: {context.get('weather_data', '无')}\n当前物候: {context.get('current_phenology', '未知')}\n任务: {task}"},
        ]
        response = await llm_client.chat(messages)
        logger.info(f"PhenologyPredictionAgent 执行完成: task='{task[:50]}...'")
        return response
