from typing import Dict, List

class CognitiveObservability:
    """
    Monitors latency, throughput, and success rates for cognitive workflows.
    """
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
        
    def record_latency(self, component: str, latency_ms: float):
        if component not in self.metrics:
            self.metrics[component] = []
        self.metrics[component].append(latency_ms)
        
    def get_average_latency(self, component: str) -> float:
        times = self.metrics.get(component, [])
        if not times:
            return 0.0
        return sum(times) / len(times)
