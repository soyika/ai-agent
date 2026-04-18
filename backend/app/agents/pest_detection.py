from typing import Optional, Any
from app.agents.base_agent import BaseAgent
from app.core.llm_client import llm_client
from loguru import logger


class PestDetectionAgent(BaseAgent):
    SYSTEM_PROMPT = """你是猕猴桃病虫害识别与诊断专家。你的职责包括：
1. 基于图像识别技术分析叶片、果实、枝干的病虫害症状
2. 识别常见猕猴桃病害：褐斑病、炭疽病、根腐病、花叶病、软腐病等
3. 识别常见虫害：叶蝉、介壳虫、红蜘蛛、蚜虫、金龟子等
4. 提供综合防治方案和农药使用建议

猕猴桃常见病虫害特征：
- 褐斑病：叶片出现褐色圆形或不规则形病斑，后期病斑扩大
- 炭疽病：果实出现褐色凹陷病斑，潮湿时产生粉红色分生孢子
- 根腐病：根部腐烂，植株生长衰弱，叶片发黄
- 叶蝉：刺吸汁液，叶片出现白色斑点

请根据用户提供的图像描述或症状描述，进行病虫害诊断并提供防治建议。"""

    def __init__(self):
        super().__init__(
            name="pest_detection",
            description="病虫害识别 Agent：基于图像识别技术检测和诊断猕猴桃病虫害",
            capabilities=[
                "图像病虫害识别",
                "病害类型诊断",
                "虫害类型识别",
                "防治方案推荐",
                "农药使用指导",
                "病虫害预警",
            ],
        )

    async def execute(self, task: str, context: Optional[dict] = None) -> Any:
        context = context or {}
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": f"图像/症状描述: {context.get('image_desc', '无')}\n任务: {task}"},
        ]
        response = await llm_client.chat(messages)
        logger.info(f"PestDetectionAgent 执行完成: task='{task[:50]}...'")
        return response
