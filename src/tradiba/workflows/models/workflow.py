from dataclasses import dataclass
from uuid import UUID

@dataclass(slots=True)
class WorkflowStep:
    step_id: str
    name: str
    action_type: str
    dependencies: list[str]

@dataclass(slots=True)
class Workflow:
    id: UUID
    name: str
    version: str
    steps: list[WorkflowStep]
