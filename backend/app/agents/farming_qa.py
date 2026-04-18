from typing import Optional, Any
from app.agents.base_agent import BaseAgent
from app.core.llm_client import llm_client
from app.services.rag_service import RAGService
from loguru import logger


class FarmingQAAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="farming_qa",
            description="农事问答 Agent：回答猕猴桃种植相关的农业技术问题",
            capabilities=[
                "种植技术咨询",
                "修剪技术指导",
                "病虫害防治问答",
                "品种选择建议",
                "土壤管理建议",
                "农业政策解读",
            ],
        )
        self.rag_service = RAGService()

    async def execute(self, task: str, context: Optional[dict] = None) -> Any:
        context = context or {}

        relevant_docs = await self.rag_service.search(query=task, top_k=3)

        system_prompt = """你是猕猴桃种植技术专家，拥有丰富的猕猴桃种植知识和实践经验。
请基于检索到的专业知识库，准确回答用户关于猕猴桃种植的技术问题。
如果知识库中的信息不足以回答，请基于你的专业知识给出合理的建议。"""

        context_str = "\n\n相关知识参考:\n" + "\n---\n".join(relevant_docs) if relevant_docs else ""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{context_str}\n\n问题: {task}"},
        ]
        response = await llm_client.chat(messages)
        logger.info(f"FarmingQAAgent 执行完成: task='{task[:50]}...'")
        return response
