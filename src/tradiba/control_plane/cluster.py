from dataclasses import dataclass
from enum import Enum
from uuid import UUID

class Environment(Enum):
    DEVELOPMENT = "dev"
    TEST = "test"
    PAPER_TRADING = "paper"
    STAGING = "staging"
    PRODUCTION = "prod"

class ClusterStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    UPGRADING = "upgrading"

@dataclass(slots=True)
class Cluster:
    """Represents a deployed Tradiba node/cluster within the fleet."""
    cluster_id: UUID
    name: str
    environment: Environment
    region: str
    version: str
    status: ClusterStatus
