from typing import Dict, Any

class PlatformEndpoints:
    """
    REST endpoints for platform diagnostics.
    """
    def health(self) -> Dict[str, Any]:
        return {"status": "ok"}
