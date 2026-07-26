from dataclasses import dataclass
from enum import Enum
from typing import Any

class IncidentSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentStatus(Enum):
    DETECTED = "detected"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    MITIGATED = "mitigated"
    RESOLVED = "resolved"
    POSTMORTEM = "postmortem"

@dataclass(slots=True)
class Incident:
    id: str
    severity: IncidentSeverity
    status: IncidentStatus
    impact: str
    timeline: list[dict[str, Any]]
    owner: str | None
