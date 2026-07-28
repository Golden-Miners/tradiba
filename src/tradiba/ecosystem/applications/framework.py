from typing import Dict, Any

class ApplicationFramework:
    """
    Application model definitions (manifest, capabilities, dependencies).
    """
    def __init__(self):
        self.applications: Dict[str, Dict[str, Any]] = {}

    def register_app(self, app_id: str, manifest: Dict[str, Any]) -> None:
        self.applications[app_id] = manifest

    def get_app(self, app_id: str) -> Dict[str, Any]:
        return self.applications.get(app_id, {})
