from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_agents():
    from app.core.agent_registry import agent_registry
    return agent_registry.list_agents()


@router.get("/{agent_name}")
async def get_agent(agent_name: str):
    from app.core.agent_registry import agent_registry
    agent = agent_registry.get_agent(agent_name)
    if not agent:
        return {"error": f"未找到智能体: {agent_name}"}
    return {
        "name": agent.name,
        "description": agent.description,
        "capabilities": agent.capabilities,
    }
