from dataclasses import dataclass, field
import os

@dataclass
class DistributedConfig:
    node_id: str = field(default_factory=lambda: os.getenv("NODE_ID", "local-node"))
    messaging_type: str = field(default_factory=lambda: os.getenv("MESSAGING_TYPE", "in_memory"))
    broker_url: str = field(default_factory=lambda: os.getenv("BROKER_URL", ""))
    heartbeat_interval_seconds: int = field(default_factory=lambda: int(os.getenv("HEARTBEAT_INTERVAL", "5")))
    election_lease_ttl: int = field(default_factory=lambda: int(os.getenv("ELECTION_LEASE_TTL", "15")))
