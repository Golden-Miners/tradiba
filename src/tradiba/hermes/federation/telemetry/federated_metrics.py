from typing import Dict, Any

class FederatedTelemetry:
    """
    Observability for the federation operations center.
    """
    def __init__(self):
        self.metrics: Dict[str, Any] = {"cross_org_requests": 0}

    def record_request(self) -> None:
        self.metrics["cross_org_requests"] += 1
