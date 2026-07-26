from typing import Dict, Any, Optional
import random

class FeatureFlagManager:
    """Manages rollout logic for feature flags."""
    
    def __init__(self) -> None:
        self._flags: Dict[str, Dict[str, Any]] = {}
        
    def configure_flag(self, flag_name: str, enabled: bool = False, percentage: float = 0.0) -> None:
        self._flags[flag_name] = {
            "enabled": enabled,
            "percentage": percentage
        }
        
    def is_enabled(self, flag_name: str, context: Optional[Dict[str, Any]] = None) -> bool:
        flag = self._flags.get(flag_name)
        if not flag:
            return False
            
        if flag["enabled"]:
            return True
            
        if flag["percentage"] > 0.0:
            # Simple mock evaluation
            return random.random() < flag["percentage"]
            
        return False
