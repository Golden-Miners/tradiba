from dataclasses import dataclass
from uuid import UUID
from enum import Enum
from typing import List

class CapabilityStatus(Enum):
    EXPERIMENTAL = "EXPERIMENTAL"
    SUPPORTED = "SUPPORTED"
    DEPRECATED = "DEPRECATED"
    REMOVED = "REMOVED"

@dataclass(frozen=True)
class Capability:
    id: UUID
    name: str
    version: str
    status: CapabilityStatus
    owner: str
    dependencies: List[str]
