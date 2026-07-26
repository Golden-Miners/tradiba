from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass(slots=True)
class PlatformSnapshot:
    """Immutable snapshot of the platform state for AI analysis."""
    timestamp: datetime
    cluster_status: str
    brokers: list[dict[str, Any]]
    portfolio: dict[str, Any]
    strategies: list[dict[str, Any]]
    alerts: list[dict[str, Any]]
    metrics: dict[str, Any]

@dataclass
class AISafetyPolicy:
    """Configurable boundaries for AI operations."""
    can_submit_orders: bool = False
    can_disable_risk_controls: bool = False
    can_bypass_approvals: bool = False
    require_human_in_the_loop: bool = True
