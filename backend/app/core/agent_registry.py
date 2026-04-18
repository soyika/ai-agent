from typing import Optional, Any
from app.agents.base_agent import BaseAgent
from loguru import logger


class AgentRegistry:
    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent):
        self._agents[agent.name] = agent
        logger.info(f"注册智能体: {agent.name} ({agent.description})")

    def get_agent(self, name: str) -> Optional[BaseAgent]:
        return self._agents.get(name)

    def list_agents(self) -> dict[str, dict]:
        return {
            name: {
                "description": agent.description,
                "capabilities": agent.capabilities,
            }
            for name, agent in self._agents.items()
        }

    async def dispatch(
        self, agent_name: str, task: str, context: Optional[dict] = None
    ) -> Any:
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"未找到智能体: {agent_name}")
        return await agent.execute(task, context or {})


# 全局智能体注册表
agent_registry = AgentRegistry()
