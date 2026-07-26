from typing import Dict
from tradiba.evolution.rollout import RollingUpgradeManager
from tradiba.evolution.exceptions import RollbackFailedError
import logging

logger = logging.getLogger(__name__)

class RollbackOrchestrator:
    """Coordinates automatic rollback when validation fails."""
    
    def __init__(self, rollout_manager: RollingUpgradeManager) -> None:
        self.rollout_manager = rollout_manager
        self._previous_versions: Dict[str, str] = {}
        
    def register_safe_state(self, service: str, version: str) -> None:
        self._previous_versions[service] = version
        
    def trigger_rollback(self, service: str, reason: str) -> None:
        safe_version = self._previous_versions.get(service)
        if not safe_version:
            raise RollbackFailedError(f"No safe version to rollback to for {service}")
            
        logger.warning(f"Rolling back {service} to {safe_version}. Reason: {reason}")
        self.rollout_manager.promote_to_production(service, safe_version)
