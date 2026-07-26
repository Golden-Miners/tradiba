from dataclasses import dataclass
from typing import List
from uuid import UUID

@dataclass
class StrategyCandidate:
    id: UUID
    entry_conditions: List[str]
    exit_rules: List[str]
    risk_rules: List[str]
    time_filters: List[str]
    regime_filters: List[str]
    status: str = "EXPERIMENTAL"

class StrategyGenerator:
    """Generates candidate strategies based on generation templates."""
    def generate(self, hypothesis_id: UUID) -> StrategyCandidate:
        # Mock strategy generation
        import uuid
        return StrategyCandidate(
            id=uuid.uuid4(),
            entry_conditions=["fvg_formed", "liquidity_swept"],
            exit_rules=["target_liquidity"],
            risk_rules=["max_risk_1_percent"],
            time_filters=["killzone_ny"],
            regime_filters=["trending"]
        )
