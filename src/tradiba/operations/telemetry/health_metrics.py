from typing import Dict, Any

class HealthMetrics:
    """
    Live operational state and reliability trends.
    """
    def __init__(self):
        self.metrics: Dict[str, Any] = {"score": 100}

    def update_score(self, new_score: int) -> None:
        self.metrics["score"] = new_score
