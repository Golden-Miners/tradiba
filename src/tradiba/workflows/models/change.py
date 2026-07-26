from dataclasses import dataclass
from enum import Enum

class ChangeStatus(Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"
    ROLLED_BACK = "rolled_back"

@dataclass(slots=True)
class ChangeRecord:
    id: str
    description: str
    justification: str
    approvers: list[str]
    implementation_plan: str
    rollback_plan: str
    verification_checklist: list[str]
    status: ChangeStatus
