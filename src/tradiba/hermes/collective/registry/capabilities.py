from typing import Dict, Any, List

class CapabilityRegistry:
    """
    Agent Registry for Hermes Collective.
    Each agent advertises:
    - Supported tools
    - Skills
    - Required permissions
    - Performance metrics
    - Health status
    """
    
    def __init__(self):
        self._agents: Dict[str, Dict[str, Any]] = {}

    def register_agent(self, agent_id: str, capabilities: Dict[str, Any]):
        self._agents[agent_id] = {
            "capabilities": capabilities,
            "health_status": "ONLINE",
            "performance_metrics": {}
        }

    def unregister_agent(self, agent_id: str):
        if agent_id in self._agents:
            del self._agents[agent_id]

    def update_health(self, agent_id: str, status: str):
        if agent_id in self._agents:
            self._agents[agent_id]["health_status"] = status

    def get_agent_capabilities(self, agent_id: str) -> Dict[str, Any]:
        if agent_id in self._agents:
            return self._agents[agent_id]["capabilities"]
        return {}

    def find_agents_by_skill(self, skill: str) -> List[str]:
        matching_agents = []
        for agent_id, data in self._agents.items():
            if data["health_status"] == "ONLINE":
                skills = data["capabilities"].get("skills", [])
                if skill in skills:
                    matching_agents.append(agent_id)
        return matching_agents

    def get_all_agents(self) -> Dict[str, Dict[str, Any]]:
        return self._agents
