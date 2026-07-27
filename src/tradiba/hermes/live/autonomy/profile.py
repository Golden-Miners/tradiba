from enum import IntEnum
from typing import Dict, Any

class AutonomyLevel(IntEnum):
    OBSERVE_ONLY = 0
    RECOMMENDATIONS_ONLY = 1
    PAPER_TRADING = 2
    LIVE_WITH_APPROVAL = 3
    LIVE_AUTONOMOUS = 4
    ORGANIZATION_DEFINED = 5

class AutonomyProfile:
    """
    Manages the autonomy configuration for Hermes.
    Can be configured per tenant, portfolio, strategy, and account.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.level = AutonomyLevel(config.get("autonomy_level", 0))

    def get_level(self) -> AutonomyLevel:
        return self.level

    def set_level(self, level: AutonomyLevel):
        self.level = level

    def can_execute_live(self) -> bool:
        return self.level >= AutonomyLevel.LIVE_WITH_APPROVAL

    def requires_human_approval(self) -> bool:
        return self.level == AutonomyLevel.LIVE_WITH_APPROVAL
