from typing import List

class APIVersioning:
    """Stubs for tracking supported API versions and their lifecycles."""
    
    def __init__(self) -> None:
        self._supported_versions: List[str] = ["v1", "v2"]
        
    def is_supported(self, version: str) -> bool:
        return version in self._supported_versions
        
    def deprecate_version(self, version: str) -> None:
        if version in self._supported_versions:
            self._supported_versions.remove(version)
