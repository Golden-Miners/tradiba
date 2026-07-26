from dataclasses import dataclass
from enum import Enum, auto
from typing import List

class StrategyStatus(Enum):
    EXPERIMENTAL = auto()
    CANDIDATE = auto()
    VALIDATED = auto()
    PAPER_TRADING = auto()
    PRODUCTION = auto()
    RETIRED = auto()

@dataclass
class StrategyDescriptor:
    """
    Reference Implementation: Strategy Descriptor.
    Treats every strategy as a managed asset within the Portfolio Intelligence layer.
    """
    id: str
    name: str
    version: str
    author: str
    risk_profile: str  # e.g., 'aggressive', 'conservative'
    asset_classes: List[str]
    timeframes: List[str]
    status: StrategyStatus = StrategyStatus.EXPERIMENTAL
