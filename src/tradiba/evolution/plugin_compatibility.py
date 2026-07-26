from typing import Dict, List

class PluginCompatibility:
    """Validates SDK and Platform versions against plugin requirements."""
    
    def __init__(self, platform_version: str) -> None:
        self.platform_version = platform_version
        self._compatible_plugins: Dict[str, List[str]] = {}
        
    def register_compatibility(self, plugin_name: str, supported_versions: List[str]) -> None:
        self._compatible_plugins[plugin_name] = supported_versions
        
    def is_compatible(self, plugin_name: str) -> bool:
        supported = self._compatible_plugins.get(plugin_name, [])
        return self.platform_version in supported
