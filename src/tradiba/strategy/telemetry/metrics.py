from typing import Dict, Any

class StrategicMetrics:
    """
    Provides analytics on forecast accuracy, scenario success, and strategic ROI.
    """
    def __init__(self):
        self.metrics: Dict[str, Any] = {"roi": 0.0, "success_rate": 0.0}

    def update(self, roi: float, success_rate: float) -> None:
        self.metrics["roi"] = roi
        self.metrics["success_rate"] = success_rate
