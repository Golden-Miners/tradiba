from typing import Dict, Any, List

class ReleaseManager:
    """
    Tracks candidate releases, approval histories, and canary deployments.
    """
    def __init__(self):
        self.releases: Dict[str, Dict[str, Any]] = {}
        
    def create_release(self, version: str, artifacts: List[str]):
        self.releases[version] = {
            "artifacts": artifacts,
            "status": "CANDIDATE",
            "approvals": []
        }
        
    def approve_release(self, version: str, approver: str):
        if version in self.releases:
            self.releases[version]["approvals"].append(approver)
            self.releases[version]["status"] = "APPROVED"
