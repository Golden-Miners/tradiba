from dataclasses import dataclass
from uuid import UUID

@dataclass
class DeploymentRecord:
    deployment_id: UUID
    cluster_id: UUID
    version: str
    status: str

class DeploymentOrchestrator:
    """Coordinates remote deployments to clusters."""
    def __init__(self) -> None:
        self._history: list[DeploymentRecord] = []

    def schedule(self, cluster_id: UUID, version: str) -> DeploymentRecord:
        import uuid
        record = DeploymentRecord(
            deployment_id=uuid.uuid4(),
            cluster_id=cluster_id,
            version=version,
            status="scheduled"
        )
        self._history.append(record)
        return record

    def complete(self, deployment_id: UUID) -> None:
        for record in self._history:
            if record.deployment_id == deployment_id:
                record.status = "completed"
                
    def rollback(self, deployment_id: UUID) -> None:
        for record in self._history:
            if record.deployment_id == deployment_id:
                record.status = "rolled_back"
