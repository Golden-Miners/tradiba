from typing import Dict

class AIQualityGates:
    """
    Enforces strict thresholds for accuracy, safety, and latency.
    """
    def __init__(self):
        self.thresholds = {
            "accuracy": 0.90,
            "hallucination": 0.05,
            "latency": 500.0
        }
        
    def evaluate_gates(self, metrics: Dict[str, float]) -> bool:
        if metrics.get("accuracy", 0) < self.thresholds["accuracy"]:
            return False
        if metrics.get("hallucination", 1) > self.thresholds["hallucination"]:
            return False
        if metrics.get("latency", 9999) > self.thresholds["latency"]:
            return False
        return True
