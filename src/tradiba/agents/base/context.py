from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class AgentContext:
    """Provides a controlled execution context for agents."""
    market_snapshot: Dict[str, Any]
    portfolio_snapshot: Dict[str, Any]
    research_results: Dict[str, Any]
    risk_limits: Dict[str, Any]
    configuration: Dict[str, Any]
    clock: Any
    logger: Any
