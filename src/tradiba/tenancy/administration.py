from typing import Dict

class PlatformAdministration:
    """Administrative capabilities for managing global platform state."""
    
    def __init__(self) -> None:
        self._global_flags: Dict[str, bool] = {}
        
    def set_feature_flag(self, feature: str, enabled: bool) -> None:
        self._global_flags[feature] = enabled
        
    def is_feature_enabled(self, feature: str) -> bool:
        return self._global_flags.get(feature, False)
