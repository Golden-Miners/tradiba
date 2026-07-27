from typing import Dict

class LearningAnalytics:
    """
    Tracks knowledge growth, calibration accuracy, and learning velocity.
    """
    def __init__(self):
        self.metrics: Dict[str, float] = {
            "knowledge_items": 0,
            "calibration_error": 0.0,
            "human_acceptance_rate": 1.0
        }
        
    def record_metric(self, key: str, value: float):
        self.metrics[key] = value
        
    def get_metrics(self) -> Dict[str, float]:
        return self.metrics
