from typing import Dict, Any

class CognitiveMesh:
    """
    Connect multiple Hermes platforms into a governed mesh.
    """
    def __init__(self):
        self.peers: Dict[str, Dict[str, Any]] = {}

    def join(self, peer_url: str, identity: str) -> bool:
        self.peers[identity] = {"url": peer_url, "status": "active"}
        return True

    def leave(self, identity: str) -> bool:
        if identity in self.peers:
            del self.peers[identity]
            return True
        return False

    def get_topology(self) -> Dict[str, Any]:
        return {"peers": self.peers}
