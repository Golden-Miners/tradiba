from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import List

class DecisionCategory(Enum):
    DEPLOY_STRATEGY = "DEPLOY_STRATEGY"
    REJECT_STRATEGY = "REJECT_STRATEGY"
    INCREASE_ALLOCATION = "INCREASE_ALLOCATION"
    REDUCE_EXPOSURE = "REDUCE_EXPOSURE"
    SWITCH_EXECUTION_ALGO = "SWITCH_EXECUTION_ALGO"
    PAUSE_BROKER = "PAUSE_BROKER"
    PROMOTE_MODEL = "PROMOTE_MODEL"

class DecisionStatus(Enum):
    PROPOSED = "PROPOSED"
    SIMULATING = "SIMULATING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"
    SUPERSEDED = "SUPERSEDED"

@dataclass(frozen=True)
class Decision:
    """Represents a significant platform decision."""
    decision_id: UUID
    category: DecisionCategory
    created_at: datetime
    status: DecisionStatus
    objective: str
    confidence: float
    evidence_ids: List[UUID]
    policy_results: List[UUID]
