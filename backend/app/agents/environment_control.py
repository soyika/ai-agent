from typing import Optional, Any
from app.agents.base_agent import BaseAgent
from app.core.llm_client import llm_client
from loguru import logger


class EnvironmentControlAgent(BaseAgent):
    SYSTEM_PROMPT = """你是猕猴桃种植园环境控制专家。你的职责包括：
1. 监测和分析温湿度、光照、CO2浓度、土壤墒情等环境参数
2. 根据猕猴桃生长阶段（萌芽期、开花期、果实膨大期、成熟期）推荐最佳环境参数
3. 控制温室、大棚的通风、遮阳、灌溉设备
4. 预警极端天气和异常环境状况

猕猴桃生长适宜环境参考：
- 温度：15-25°C（最适生长），冬季休眠可耐-10°C
- 湿度：60-80%
- 光照：充足但避免强光直射，夏季需遮阳
- 土壤 pH：5.5-6.5（微酸性）

请根据用户提供的环境数据和任务，给出具体的控制建议和方案。"""

    def __init__(self):
        super().__init__(
            name="environment_control",
            description="环境控制 Agent：负责温度、湿度、光照、通风等环境参数调控",
            capabilities=[
                "温湿度监测与调控",
                "光照管理",
                "通风控制",
                "CO2浓度调节",
                "极端天气预警",
                "设备联动控制",
            ],
        )

    async def execute(self, task: str, context: Optional[dict] = None) -> Any:
        context = context or {}
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": f"环境数据: {context.get('sensor_data', '无')}\n任务: {task}"},
        ]
        response = await llm_client.chat(messages)
        logger.info(f"EnvironmentControlAgent 执行完成: task='{task[:50]}...'")
        return response
