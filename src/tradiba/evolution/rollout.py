from typing import Dict

class RollingUpgradeManager:
    """Supports deployment strategies like Blue/Green, Canary, and Rolling."""
    
    def __init__(self) -> None:
        self._deployments: Dict[str, str] = {}
        
    def start_canary(self, service: str, new_version: str) -> None:
        self._deployments[service] = f"{new_version}_canary"
        
    def promote_to_production(self, service: str, version: str) -> None:
        self._deployments[service] = version
        
    def get_deployment_status(self, service: str) -> str | None:
        return self._deployments.get(service)
