from app.agents.environment_control import EnvironmentControlAgent
from app.agents.pest_detection import PestDetectionAgent
from app.agents.irrigation_fertilizer import IrrigationFertilizerAgent
from app.agents.phenology_prediction import PhenologyPredictionAgent
from app.agents.farming_qa import FarmingQAAgent
from app.agents.order_fulfillment import OrderFulfillmentAgent
from app.agents.customer_service import CustomerServiceAgent
from app.core.agent_registry import AgentRegistry


def register_all_agents(registry: AgentRegistry):
    registry.register(EnvironmentControlAgent())
    registry.register(PestDetectionAgent())
    registry.register(IrrigationFertilizerAgent())
    registry.register(PhenologyPredictionAgent())
    registry.register(FarmingQAAgent())
    registry.register(OrderFulfillmentAgent())
    registry.register(CustomerServiceAgent())
