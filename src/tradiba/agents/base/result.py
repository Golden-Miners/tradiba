from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class AgentResult:
    """Standardized output container for agents."""
    agent_name: str
    status: str
    output: Dict[str, Any]
    confidence: float
