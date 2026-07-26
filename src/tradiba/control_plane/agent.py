import time
from uuid import UUID
from tradiba.control_plane.exceptions import AgentConnectionError

class TradibaAgent:
    """Lightweight edge agent running on the nodes."""
    def __init__(self, cluster_id: UUID) -> None:
        self.cluster_id = cluster_id
        self.last_heartbeat: float = 0.0
        self.connected: bool = False

    def connect(self) -> None:
        """Simulates connecting to the control plane."""
        self.connected = True
        self.ping()

    def ping(self) -> None:
        if not self.connected:
            raise AgentConnectionError(f"Agent for cluster {self.cluster_id} is disconnected.")
        self.last_heartbeat = time.time()
        
    def disconnect(self) -> None:
        self.connected = False
