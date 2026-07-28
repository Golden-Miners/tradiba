from typing import Dict, Any

class MultimodalTelemetry:
    """
    Multimodal telemetry for observability.
    """
    def __init__(self):
        self.metrics: Dict[str, Any] = {"processed_bytes": 0}

    def record_processing(self, size_bytes: int) -> None:
        self.metrics["processed_bytes"] += size_bytes
